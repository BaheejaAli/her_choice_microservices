import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ServiceGatewayView(APIView):

    def dispatch_request(self, request, service_url, path):

        url = f"{service_url}/{path}"

        try:
            response = requests.request(
                method=request.method,
                url=url,
                params=request.query_params,
                json=request.data if request.method in ["POST", "PUT", "PATCH"] else None,
                timeout=settings.SERVICE_TIMEOUT
            )

            try:
                data = response.json()
            except ValueError:
                data = response.text

            return Response(
                data,
                status=response.status_code
            )

        except requests.Timeout:
            return Response(
                {"error": "Service request timed out"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )

        except requests.ConnectionError:
            return Response(
                {"error": "Backend service unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def get(self, request, service, path=""):
        return self.forward(request, service, path)

    def post(self, request, service, path=""):
        return self.forward(request, service, path)

    def put(self, request, service, path=""):
        return self.forward(request, service, path)

    def patch(self, request, service, path=""):
        return self.forward(request, service, path)

    def delete(self, request, service, path=""):
        return self.forward(request, service, path)

    def forward(self, request, service, path):

        service_urls = {
            "users": settings.USER_SERVICE_URL,
            "products": settings.PRODUCT_SERVICE_URL,
            "orders": settings.ORDER_SERVICE_URL,
        }

        service_url = service_urls.get(service)

        if not service_url:
            return Response(
                {"error": "Service not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return self.dispatch_request(
            request,
            service_url,
            f"{service}/{path}".rstrip("/")
        )