from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, UpdateUserSerializer, ChangePasswordSerializer
from .models import UserHistory
from .serializers import UserHistorySerializer
from .utils import send_otp_email
from .utils import generate_otp


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate OTP and save it to user
            otp = generate_otp()
            user.otp = otp
            user.email_verified = False
            user.save()

            # "Send" OTP to email (console for now)
            print(f"[OTP for {user.email}]: {otp}")

            # Log history for registration
            UserHistory.objects.create(
                user=user,
                action="register",
                description="User initiated registration (OTP pending)",
                details=json.dumps({
                    "email": user.email,
                    "role": user.role,
                    "otp": otp  # optional in history
                }),
            )

            #refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully. Check console for OTP to verify email.",
                "user_id": user.id,
                # "access": str(refresh.access_token),
                # "refresh": str(refresh),
                # "user": UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        otp = request.data.get("otp")

        if not user_id or not otp:
            return Response({"error": "user_id and otp are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.is_active = True
            user.email_verified = True
            user.otp = None
            user.save()

            refresh = RefreshToken.for_user(user)

            # Log verification
            UserHistory.objects.create(
                user=user,
                action="verify_otp",
                description="User verified OTP and activated account",
                details=json.dumps({"email": user.email}),
            )

            return Response({
                "message": "Email verified successfully. Account activated.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email:
            return Response({"email": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"password": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.email_verified:
                return Response({"detail": "Please verify your email before logging in."},
                                status=status.HTTP_403_FORBIDDEN)
            refresh = RefreshToken.for_user(user)
            # Log login event
            UserHistory.objects.create(
                user=user,
                action="login",
                description="User logged in",
                details=json.dumps({
                    "ip": request.META.get("REMOTE_ADDR"),
                    "user_agent": request.META.get("HTTP_USER_AGENT"),
                }),
            )
            return Response({
                "user": {
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# 🔹 Get/Update Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UpdateUserSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False, context={"request": request})
        if serializer.is_valid():
            old_email = user.email
            old_name = user.full_name
            self.perform_update(serializer)
            # Determine changed fields for details
            changed = {}
            if old_email != serializer.data.get("email"):
                changed["email"] = {"from": old_email, "to": serializer.data.get("email")}
            if old_name != serializer.data.get("full_name"):
                changed["full_name"] = {"from": old_name, "to": serializer.data.get("full_name")}
            # Log history
            UserHistory.objects.create(
                user=request.user,
                action="update_profile",
                description="Profile updated",
                details=json.dumps({"changed": changed}),
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Change Password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            # Log password change
            UserHistory.objects.create(
                user=request.user,
                action="change_password",
                description="Password changed",
                details=json.dumps({}),
            )
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserHistoryListView(generics.ListAPIView):
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserHistory.objects.filter(user=self.request.user).order_by("-created_at")