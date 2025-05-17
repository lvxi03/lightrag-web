from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.cache import cache
from hashlib import sha256
from .models import Account


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, required=True)  # 添加验证码字段

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password', 'role', 'register_time', 'code']
        extra_kwargs = {
            'password': {'write_only': True},
            'register_time': {'read_only': True},
            'code': {'write_only': True}  # 确保验证码字段不会被返回
        }

    def create(self, validated_data):
        code = validated_data.pop('code')
        try:
            user = Account.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=validated_data.get('role', 'user')
            )
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})
        return user

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        return value

    def validate_code(self, value):
        email = self.initial_data.get('email')
        if not email:
            raise serializers.ValidationError("Email is required to validate the code.")

        cache_key = f'verification_code_{email}'
        cached_code = cache.get(cache_key)
        if not cached_code:
            raise serializers.ValidationError("Verification code has expired.")
        if cached_code != value:
            raise serializers.ValidationError("Invalid verification code.")

        cache.delete(cache_key)  # 删除验证码缓存
        return value