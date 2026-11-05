import requests
from django.conf import settings


def _get(base_url, path):
    try:
        return requests.get(f"{base_url}{path}", timeout=settings.SERVICE_TIMEOUT)
    except (requests.ConnectionError, requests.Timeout):
        return None


def get_user(user_id):
    return _get(settings.USER_SERVICE_URL, f"/users/{user_id}/")


def get_product(product_id):
    return _get(settings.PRODUCT_SERVICE_URL, f"/products/{product_id}/")