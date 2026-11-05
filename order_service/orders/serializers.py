from rest_framework import serializers
from .models import Order


class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user_id", "product_id", "product_name",
                  "unit_price", "quantity", "total_amount",
                  "status", "created_at"]