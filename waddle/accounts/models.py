from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django_extensions.db.models import TimeStampedModel

from .validators import validate_mobile


class UserManager(BaseUserManager):
    def create_user(self, name, mobile, email, password=None):
        if not email:
            raise ValueError("Users must have a unique email address!")

        user = self.model(
            name=name,
            mobile=mobile,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, mobile, email, password=None):
        user = self.create_user(
            name=name,
            mobile=mobile,
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    name = models.CharField(max_length=200)
    mobile = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_mobile]
    )
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    REQUIRED_FIELDS = ["name", "mobile"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.name}'s account"
