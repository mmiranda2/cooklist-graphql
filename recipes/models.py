from django.db import models
from ingredients.models import Ingredient


### TODO: If you see models and data sources growing (in length or in depth), one may consider 
###       - creating a small Factory pattern to list and handle the models dynamically
###       - feed the Factory from an external config resource defining all relevant
###             metadata and conversion maps between different data sources/destinations
###       - With the nested, graph/object oriented nature of the served data,
###             it may become regressive/difficult to modify models in code--
###             like changing "instructions" from field to a model--if there were many relations


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=False, blank=True)
    instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='amounts', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='used_by', on_delete=models.CASCADE)

    ### Conceptual
    amount = models.FloatField()
    unit = models.CharField(
        max_length=20,
        choices=(
            ("unit", "Units"),
            ("tsp", "Teaspoons"),
            ("tbsp", "Tablespoons"),
            ("cup", "Cups"),
            ("lb", "Pounds"),
        ),
    )
    ###
