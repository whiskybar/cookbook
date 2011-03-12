from django.template.response import TemplateResponse
from django.http import Http404

from cookbook.recipe.models import Recipe
from cookbook.recipe.forms import RecipeForm


def recipe_detail(request, username, recipe_slug):
    try:
        recipe = Recipe.objects.get(owner=username, slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404('No recipe matches the given query.')

    context = dict(recipe=recipe)
    return TemplateResponse(request, 'recipe/detail.html', context)


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
    else:
        form = RecipeForm()
    return TemplateResponse(
        request,
        'recipe/add.html',
        { 'form': form, }
    )
