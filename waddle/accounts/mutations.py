import graphene
from django.contrib.auth import get_user_model

from .types import UserType


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        mobile = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = get_user_model().objects.create_user(
            name=kwargs["name"],
            email=kwargs["email"],
            mobile=kwargs["mobile"],
            password=kwargs["password"],
        )

        return UserCreate(user=user)
