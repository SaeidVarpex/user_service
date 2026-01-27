from rest_framework import status, permissions, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .serializers import CustomTokenObtainPairSerializer, TokenDecodeSerializer
from users.serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    UserAdminSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserProfileSerializer(user, context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        return UserAdminSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        return UserAdminSerializer


# api/token_views.py
from rest_framework.permissions import AllowAny, IsAuthenticated
import jwt
from django.conf import settings


# api/token_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


class TokenDecodeView(GenericAPIView):
    """
    Token decode view with proper form rendering
    """
    permission_classes = [AllowAny]
    serializer_class = TokenDecodeSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def get_serializer_context(self):
        """Add request to serializer context for form rendering"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get(self, request, *args, **kwargs):
        """
        Render form for token input
        """
        serializer = self.get_serializer()
        return Response({
            "instructions": "Enter JWT token and options below",
            "form": {
                "fields": [
                    {
                        "name": "token",
                        "type": "textarea",
                        "required": True,
                        "label": "JWT Token",
                        "help_text": "Paste your complete JWT token"
                    },
                    {
                        "name": "verify_exp",
                        "type": "checkbox",
                        "default": True,
                        "label": "Verify expiration"
                    },
                    {
                        "name": "verify_aud",
                        "type": "checkbox",
                        "default": True,
                        "label": "Verify audience"
                    },
                    {
                        "name": "verify_iss",
                        "type": "checkbox", 
                        "default": True,
                        "label": "Verify issuer"
                    }
                ]
            }
        })
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get validated data
        token = serializer.validated_data['token']
        verify_exp = serializer.validated_data.get('verify_exp', True)
        verify_aud = serializer.validated_data.get('verify_aud', True)
        verify_iss = serializer.validated_data.get('verify_iss', True)
        
        try:
            # Decode options
            options = {
                'verify_exp': verify_exp,
                'verify_aud': verify_aud,
                'verify_iss': verify_iss,
            }
            
            # Decode the token
            decoded_payload = jwt.decode(
                token,
                settings.SIMPLE_JWT["VERIFYING_KEY"],
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
                audience=settings.SIMPLE_JWT["AUDIENCE"] if verify_aud else None,
                issuer=settings.SIMPLE_JWT["ISSUER"] if verify_iss else None,
                options=options
            )
            
            # Prepare response
            response_data = {
                "success": True,
                "token_input": f"{token[:50]}..." if len(token) > 50 else token,
                "payload": decoded_payload,
                "validation_options_used": {
                    "verify_exp": verify_exp,
                    "verify_aud": verify_aud,
                    "verify_iss": verify_iss,
                }
            }
            
            return Response(response_data)
            
        except jwt.InvalidTokenError as e:
            return Response(
                {
                    "success": False,
                    "error": str(e),
                    "error_type": e.__class__.__name__
                },
                status=status.HTTP_400_BAD_REQUEST
            )
