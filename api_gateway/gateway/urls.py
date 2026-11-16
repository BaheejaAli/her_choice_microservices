from django.urls import path, re_path
from .views import ServiceGatewayView

urlpatterns = [
    re_path(
        r'^(?P<service>users|products|orders)/(?P<path>.*)$',
        ServiceGatewayView.as_view()
    ),
]