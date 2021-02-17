import accounts.schema
import graphene


class Query(accounts.schema.Query):
    pass


class Mutation(accounts.schema.Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
