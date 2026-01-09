import random
from django.core.mail import send_mail
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp = generate_otp()
    user.otp = otp
    user.save()
    send_mail(
        subject="AgriBoost Email Verification",
        message=f"Hello {user.username},\n\nYour OTP is: {otp}",
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        recipient_list=[user.email],
    )