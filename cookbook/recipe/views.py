from django.views.generic.simple import direct_to_template

from cookbook.recipe.models import Recipe


def recipe_detail(request, username, recipe_slug):
    recipe = Recipe.objects.get(owner=username, slug=recipe_slug)
    context = dict(recipe=recipe)
    return direct_to_template(request, 'recipe/recipe_detail.html', context)
