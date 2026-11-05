from rest_framework import serializers
from .models import AppUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "first_name", "last_name", "email",
                  "phone", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]