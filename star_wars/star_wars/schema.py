import graphene

import star_universe.schema
import users.schema


class Query(star_universe.schema.Query, graphene.ObjectType):
    pass


class Mutation(star_universe.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
