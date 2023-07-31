import graphene
from authentication.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile
        fields = "__all__"


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType, user_id=graphene.Int())

    def resolve_user(self, info, user_id):
        return User.objects.get(pk=user_id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user_instance = User.objects.get(pk=user_data.id)
        if user_instance:
            user_instance.first_name = user_data.first_name
            user_instance.last_name = user_data.last_name
            user_instance.save()
            return UpdateUser(user=user_instance)
        return UpdateUser(user=None)


class CreateUserInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    username = graphene.String()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(UserProfile)

    class Arguments:
        user_data = CreateUserInput(required=True)

    @staticmethod
    def mutate(self, info, user_data=None):
        user = User(first_name=user_data.first_name, last_name=user_data.last_name,
                                   email=user_data.email, username=user_data.username)
        user.set_password(user_data.password)
        user.save()
        profile = Profile.objects.get(user=user.id)
        return CreateUser(user=user, profile=profile)


class Mutation(graphene.ObjectType):
    UpdateUser = UpdateUser.Field()
    CreateUser = CreateUser.Field()
