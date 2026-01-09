from rest_framework import serializers
from django.db.models import Q
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .models import UserHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "address", "role"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "address", "password", "confirm_password"]

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Full name is required.")
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
            address=validated_data.get("address", ""),
            role="farmer",
        )
        return user

# For updating profile
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "address"]

    def validate_email(self, value):
        user = self.context["request"].user if "request" in self.context else None
        # Ensure email is unique across users excluding current user
        if CustomUser.objects.filter(Q(email__iexact=value) & ~Q(pk=getattr(user, "pk", None))).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

# For changing password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class UserHistorySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserHistory
        fields = ["id", "user_email", "user_name", "action", "description", "details", "created_at"]