import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from recipes.models import Recipe, RecipeIngredient


class RecipeNode(DjangoObjectType):
    class Meta:
        model = Recipe
        filter_fields = ['title', 'content', 'instructions', 'amounts']
        interfaces = (relay.Node,)


class RecipeIngredientNode(DjangoObjectType):
    class Meta:
        model = RecipeIngredient
        filter_fields = {
            'recipe': ['exact'],
            'recipe__title': ['exact', 'icontains'],
            'ingredient__notes': ['exact', 'icontains', 'istartswith'],
            'amount': ['exact', 'lte', 'gte'],
            'unit': ['exact']
        }
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    recipe = relay.Node.Field(RecipeNode)
    all_recipes = DjangoFilterConnectionField(RecipeNode)

    recipeingredient = relay.Node.Field(RecipeIngredientNode)
    all_recipeingredients = DjangoFilterConnectionField(RecipeIngredientNode)
