from decimal import Decimal
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .clients import get_product, get_user
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by("-id")
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_response = get_user(data["user_id"])
        if user_response is None:
            return Response({"error": "user-service is unavailable, try again later"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        product_response = get_product(data["product_id"])
        if product_response is None:
            return Response({"error": "product-service is unavailable, try again later"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if user_response.status_code == 404:
            return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not user_response.json()["is_active"]:
            return Response({"error": "user is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        if product_response.status_code == 404:
            return Response({"error": "product not found"}, status=status.HTTP_400_BAD_REQUEST)

        product = product_response.json()
        if not product["is_active"]:
            return Response({"error": "product is not available"}, status=status.HTTP_400_BAD_REQUEST)
        if product["stock"] < data["quantity"]:
            return Response({"error": f"insufficient stock, only {product['stock']} left"},
                            status=status.HTTP_400_BAD_REQUEST)

        unit_price = Decimal(product["price"])
        quantity = data["quantity"]

        order = Order.objects.create(
            user_id=data["user_id"],
            product_id=data["product_id"],
            product_name=product["name"],
            unit_price=unit_price,
            quantity=quantity,
            total_amount=unit_price * quantity,
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer