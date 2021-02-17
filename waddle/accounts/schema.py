import graphene
import graphql_jwt
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .mutations import UserCreate
from .types import UserType


class Query(graphene.ObjectType):
    user_profile = graphene.Field(
        UserType,
        description="Get profile of authenticated user."
    )

    @login_required
    def resolve_user_profile(self, info):
        return info.context.user


class Mutation(graphene.ObjectType):
    create_user = UserCreate.Field(description="Create a user account.")
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_auth = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
