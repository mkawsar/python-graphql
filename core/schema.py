import graphene
import authentication.schema


class Query(authentication.schema.Query, graphene.ObjectType):
    pass


class Mutation(authentication.schema.Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
