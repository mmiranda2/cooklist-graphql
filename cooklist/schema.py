import graphene

from graphene_django.debug import DjangoDebug

import ingredients.schema
import recipes.schema


class Query(ingredients.schema.Query, recipes.schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query)