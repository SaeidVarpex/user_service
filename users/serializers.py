from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False, allow_empty_file=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'avatar',
            'password',
            'password_confirm',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        avatar = validated_data.pop('avatar', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
            password=validated_data['password'],
        )
        if avatar:
            user.avatar = avatar
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(allow_empty_file=True, required=False, use_url=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'avatar',
            'date_joined',
            'is_staff',
            'is_active',
        ]
        read_only_fields = ['id', 'date_joined', 'is_staff', 'is_active']

    def update(self, instance, validated_data):
        # مدیریت آپلود آواتار
        if 'avatar' in validated_data:
            # اگر کاربر avatar رو خالی کرد (None یا فایل خالی)
            if validated_data['avatar'] is None or validated_data['avatar'] == '':
                if instance.avatar:
                    instance.avatar.delete(save=False)  # حذف فایل قبلی
                instance.avatar = None
        return super().update(instance, validated_data)


class UserAdminSerializer(serializers.ModelSerializer):
    """فقط برای ادمین - نمایش کامل‌تر"""
    avatar = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'avatar',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Passwords do not match."})
        return attrs
