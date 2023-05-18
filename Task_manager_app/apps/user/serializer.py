from apps.user.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.utils.enum import UserType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_type"] = user.user_type
        token['email']     = user.email
        return token


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    email = serializers.EmailField(required=True)
    user_type = serializers.ChoiceField(choices=UserType.choices())

    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        label=_("confirm_password"), style={"input_type": "password"}, write_only=True
        
    )
    

    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exits")
        return value
    



    def validate_password(self, value):
        data = self.get_initial()
        password = data.get("confirm_password")
        confirm_password = value
        if password != confirm_password:
            raise ValidationError("Passwords and Confirm password not  matching")
        return value
    
 
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    