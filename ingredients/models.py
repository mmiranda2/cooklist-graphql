from django.db import models


### TODO: If you see models and data sources growing, one may consider 
###       - creating a small Factory pattern to list and handle the models dynamically
###       - feed the Factory from an external config resource defining all relevant
###             metadata and conversion maps between different data sources/destinations
###
###       - Create a tokenizer for each ingredient notes, to parse category, amount, notes, etc. for each ingredient
###       - Without this ^ cannot parse category from data sheet


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.notes
