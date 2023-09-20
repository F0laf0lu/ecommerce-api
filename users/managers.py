from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    # Create Custom user with email as username
    def create_user(self, email, password):
        if not email:
            raise ValueError("You need to provide a valid email")
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save()
        return user