from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        description = "Type definition for a user account."
        exclude = [
            "is_admin",
            "is_staff",
            "is_superuser",
            "last_login",
        ]
