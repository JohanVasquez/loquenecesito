import graphene
from graphene_django import DjangoObjectType

from .models import Character


class CharacterType(DjangoObjectType):
    class Meta:
        model = Character


class Query(graphene.ObjectType):
    character = graphene.List(CharacterType)

    def resolve_character(self, info, **kwargs):
        return Character.objects.all()


class CreateCharacter(graphene.Mutation):
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        character = Character(name=name)
        character.save()

        return CreateCharacter(
            name=character.name,
        )


class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
