import graphene
import graphql_jwt
import authentication.schema


class Query(authentication.schema.Query, graphene.ObjectType):
    pass


class Mutation(authentication.schema.Mutation):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
