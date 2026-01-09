from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Remove username

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ("farmer", "Farmer"),
            ("researcher", "Researcher"),
            ("admin", "Admin"),
        ],
        default="farmer",
    )
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "role"]

    def __str__(self):
        return self.email


class UserHistory(models.Model):
    ACTION_CHOICES = [
        ("register", "Register"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("update_profile", "Profile Update"),
        ("change_password", "Change Password"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, null=True)
    # Optional details payload for extra context (e.g., changed fields)
    # Using TextField to avoid DB-specific JSON dependencies; store JSON-serialized text
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.created_at}"
    

