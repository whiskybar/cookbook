from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response

from cookbook.recipe.models import Recipe
from cookbook.recipe.forms import RecipeForm


def recipe_detail(request, username, recipe_slug):
    recipe = Recipe.objects.get(owner=username, slug=recipe_slug)
    context = dict(recipe=recipe)
    return direct_to_template(request, 'recipe/recipe_detail.html', context)


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save
    else:
        form = RecipeForm()
    return render_to_response('recipe/recipe_add.html', {
        'form': form,
    })
