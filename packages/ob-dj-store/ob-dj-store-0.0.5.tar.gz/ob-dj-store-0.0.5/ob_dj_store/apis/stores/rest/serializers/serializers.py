import contextlib
import typing
from datetime import time

from django.contrib.gis.geos import Point
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ob_dj_store.core.stores.models import (
    Attribute,
    AttributeChoice,
    Cart,
    CartItem,
    Category,
    Favorite,
    Feedback,
    FeedbackAttribute,
    FeedbackConfig,
    OpeningHours,
    Order,
    OrderHistory,
    OrderItem,
    Product,
    ProductAttribute,
    ProductMedia,
    ProductTag,
    ProductVariant,
    ShippingMethod,
    Store,
)
from ob_dj_store.core.stores.utils import distance


class AttributeChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeChoice
        fields = (
            "id",
            "name",
            "price",
        )


class AttributeSerializer(serializers.ModelSerializer):
    attribute_choices = AttributeChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            "id",
            "name",
            "attribute_choices",
        )


class InventoryValidationMixin:
    def validate(self, attrs: typing.Dict) -> typing.Dict:
        if attrs["product_variant"].has_inventory and attrs["quantity"] < 1:
            raise serializers.ValidationError(_("Quantity must be greater than 0."))
        # validate quantity in inventory
        stock_quantity = (
            attrs["product_variant"]
            .inventories.get(store=attrs["product_variant"].product.store)
            .quantity
        )
        if (
            attrs["product_variant"].has_inventory
            and attrs["quantity"] > stock_quantity
        ):
            raise serializers.ValidationError(
                _("Quantity is greater than the stock quantity.")
            )
        return super().validate(attrs)


class CartItemSerializer(InventoryValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            "id",
            "cart",
            "product_variant",
            "quantity",
            "unit_price",
            "total_price",
            "notes",
            "attribute_choices",
        )

    def create(self, validated_data):
        return super().create(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "customer",
            "items",
            "total_price",
        )
        read_only_fields = ("id", "total_price")

    def update(self, instance, validated_data):
        instance.items.all().delete()
        # update or create instance items
        for item in validated_data["items"]:
            cart_item = CartItem.objects.create(
                cart=instance,
                product_variant=item["product_variant"],
                quantity=item["quantity"],
                notes=item["notes"],
            )
            cart_item.attribute_choices.set(item["attribute_choices"])
            cart_item.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description", "is_active")


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = "__all__"


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):

    opening_hours = OpeningHourSerializer(many=True, read_only=True)
    in_range_delivery = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    address_line = serializers.SerializerMethodField()
    shipping_methods = ShippingMethodSerializer(many=True, read_only=True)
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "address",
            "address_line",
            "location",
            "distance",
            "is_active",
            "currency",
            "minimum_order_amount",
            "delivery_charges",
            "shipping_methods",
            "min_free_delivery_amount",
            "opening_hours",
            "in_range_delivery",
            "is_favorite",
            "created_at",
            "updated_at",
        )

    def get_in_range_delivery(self, obj):
        user_location = self.context["request"].query_params.get("point")
        if user_location and obj.poly:
            long, lat = user_location.split(",")
            return obj.poly.contains(Point(float(long), float(lat)))
        return False

    def get_is_favorite(self, obj):
        if user := self.context["request"].user:
            # The context manager slightly shortens the code and significantly clarifies the author's intention to ignore the specific errors.
            # The standard library feature was introduced following a [discussion](https://bugs.python.org/issue15806), where the consensus was that
            # A key benefit here is in the priming effect for readers...
            # The with statement form makes it clear before you start reading the code that certain exceptions won't propagate.
            # https://docs.python.org/3/library/contextlib.html
            with contextlib.suppress(Favorite.DoesNotExist):
                Favorite.objects.favorite_for_user(obj, user)
                return True
        return False

    def get_address_line(self, obj):
        return obj.address.address_line

    def get_distance(self, obj):
        # get the distance between the user location and store location
        user_location = self.context["request"].query_params.get("point")
        if user_location and obj.location:

            lat, long = user_location.split(",")
            store_lat, store_long = obj.location.x, obj.location.y
            return round(
                distance((float(lat), float(long)), (store_lat, store_long)), 1
            )


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = (
            "id",
            "order",
            "status",
            "created_at",
        )


class OrderItemSerializer(InventoryValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_variant",
            "quantity",
            "total_amount",
            "preparation_time",
            "notes",
            "attribute_choices",
        )

    def create(self, validated_data):
        return super().create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["attribute_choices"] = AttributeChoiceSerializer(
            instance.attribute_choices.all(), many=True
        ).data

        return representation


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    history = OrderHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "store",
            "shipping_method",
            "payment_method",
            "shipping_address",
            "customer",
            "status",
            "items",
            "total_amount",
            "preparation_time",
            "history",
            "pickup_time",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "customer": {"read_only": True},
        }

    def validate(self, attrs):
        # The Cart items must not be empty
        user = self.context["request"].user
        if not user.cart.items.exists():
            raise serializers.ValidationError(_("The Cart must not be empty"))

        if "pickup_time" in attrs:
            # validate that the pickup_time is always in the future
            if attrs["pickup_time"] < now():
                raise serializers.ValidationError(
                    _("Pickup time must be in the future")
                )
            # validate that the pickup_time is part of day (between 00:00 and 23:59)
            if not (
                attrs["pickup_time"].time() >= time(hour=0, minute=0)
                and attrs["pickup_time"].time() <= time(hour=23, minute=59)
            ):
                raise serializers.ValidationError(_("Pickup time must be part of day"))
            # validate that the pickup_time is between store's opening hours and closing hours
            if (
                attrs["store"]
                .opening_hours.filter(weekday=attrs["pickup_time"].weekday())
                .exists()
            ) and (
                attrs["pickup_time"].hour
                > (
                    attrs["store"]
                    .opening_hours.filter(weekday=attrs["pickup_time"].weekday())
                    .first()
                    .to_hour.hour
                )
                or attrs["pickup_time"].hour
                < (
                    attrs["store"]
                    .opening_hours.filter(weekday=attrs["pickup_time"].weekday())
                    .first()
                    .from_hour.hour
                )
            ):
                raise serializers.ValidationError(
                    _("Pickup time must be between store's opening hours")
                )

        return super().validate(attrs)

    def create(self, validated_data: typing.Dict):
        order_items = validated_data.pop("items")

        order = Order.objects.create(**validated_data)
        for item in order_items:
            attribute_choices = item.pop("attribute_choices")
            order_item = OrderItem.objects.create(order=order, **item)
            order_item.attribute_choices.set(attribute_choices)
            order_item.save()
        return order


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            "id",
            "name",
            "text_color",
            "background_color",
        )


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_choices = AttributeChoiceSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "name",
            "attribute_choices",
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    product_attributes = ProductAttributeSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "name",
            "price",
            "quantity",
            "sku",
            "is_deliverable",
            "is_active",
            "product_attributes",
            "is_primary",
        )


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = (
            "id",
            "is_primary",
            "image",
            "order_value",
        )


class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(many=False)
    variants = ProductVariantSerializer(many=True, source="product_variants")
    product_images = ProductMediaSerializer(many=True, source="images")
    is_favorite = serializers.SerializerMethodField()
    default_variant = ProductVariantSerializer(read_only=True, many=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_favorite",
            "product_images",
            "variants",
            "store",
            "default_variant",
        )

    def get_is_favorite(self, obj):
        if user := self.context["request"].user:
            # The context manager slightly shortens the code and significantly clarifies the author's intention to ignore the specific errors.
            # The standard library feature was introduced following a [discussion](https://bugs.python.org/issue15806), where the consensus was that
            # A key benefit here is in the priming effect for readers...
            # The with statement form makes it clear before you start reading the code that certain exceptions won't propagate.
            # https://docs.python.org/3/library/contextlib.html
            with contextlib.suppress(Favorite.DoesNotExist):
                Favorite.objects.favorite_for_user(obj, user)
                return True
        return False

    def to_representation(self, instance: Product):
        data = super().to_representation(instance=instance)
        return data


class ProductListSerializer(ProductSerializer):
    product_variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "product_images",
            "product_variants",
            "default_variant",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "description", "products", "is_active")


class FeedbackConfigSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    attribute = serializers.CharField(read_only=True)

    class Meta:
        model = FeedbackConfig
        fields = ("id", "attribute", "attribute_label", "values")


class FeedbackAttributeSerializer(serializers.ModelSerializer):
    config = FeedbackConfigSerializer(many=False, read_only=True)
    attribute = serializers.CharField(write_only=True)

    class Meta:
        model = FeedbackAttribute
        fields = ("attribute", "config", "value", "review")

    # TODO: do we need validations when creating the value


class FeedbackSerializer(serializers.ModelSerializer):
    attributes = FeedbackAttributeSerializer(many=True, required=False)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "attributes",
            "notes",
            "review",
        )

    def validate(self, attrs: typing.Dict):
        # Validate Order Status
        if self.instance.status not in [
            Order.OrderStatus.PAID,
            Order.OrderStatus.CANCELLED,
        ]:
            raise serializers.ValidationError(
                _("The Order must be PAID or CANCELLED to give a feedback")
            )
        return attrs

    def update(self, instance: Order, validated_data: typing.Dict):
        user = self.context["request"].user
        attributes = validated_data.pop("attributes", [])
        feedback = Feedback.objects.create(
            order=self.instance, user=user, **validated_data
        )

        for attr in attributes:
            feedback.attributes.create(**attr)
        feedback.order.save()
        return feedback
