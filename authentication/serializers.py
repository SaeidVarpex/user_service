from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
import jwt
from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # اینجا می‌تونی ادعاهای سفارشی داخل خود توکن بذاری
        token['username'] = user.username
        token['user_id'] = str(user.id)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number
        # token['is_staff'] = user.is_staff  # مثال

        return token

    def validate(self, attrs):
        data = super().validate(attrs)  # اینجا {'refresh': ..., 'access': ...} برمی‌گرده

        # اطلاعات اضافی که می‌خوای کنار توکن‌ها توی JSON برگرده
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # هر فیلد دیگه‌ای که لازم داری
        }

        return data

class TokenDecodeSerializer(serializers.Serializer):
    token = serializers.CharField(
        required=True,
        label="JWT Token",
        help_text="Paste your JWT token here",
        style={'base_template': 'textarea.html', 'rows': 5, 'placeholder': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...'},
        write_only=True
    )
    
    verify_exp = serializers.BooleanField(
        required=False,
        default=True,
        label="Verify Expiration",
        help_text="Check if token has expired"
    )
    
    verify_aud = serializers.BooleanField(
        required=False,
        default=True,
        label="Verify Audience",
        help_text="Validate token audience"
    )
    
    verify_iss = serializers.BooleanField(
        required=False,
        default=True,
        label="Verify Issuer",
        help_text="Validate token issuer"
    )
