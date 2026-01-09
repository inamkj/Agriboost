from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ChangePasswordView, VerifyOTPView
from .views import UserHistoryListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("history/", UserHistoryListView.as_view(), name="user-history"),
]
