from rest_framework import permissions, generics
from django.contrib.auth import get_user_model
from .serializers import UserAdminSerializer

User = get_user_model()


class UserListView(generics.ListAPIView):
    """
    لیست تمام کاربران - فقط برای ادمین
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    جزئیات، ویرایش و حذف یک کاربر - فقط برای ادمین
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'
