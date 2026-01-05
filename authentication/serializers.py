from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # اینجا می‌تونی ادعاهای سفارشی داخل خود توکن بذاری
        token['username'] = user.username
        token['user_id'] = user.id
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
