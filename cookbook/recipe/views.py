from django.template.response import TemplateResponse
from django.http import Http404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User

from cookbook.recipe.models import Recipe
from cookbook.recipe.forms import RecipeForm


def recipe_detail(request, username, recipe_slug):
    try:
        recipe = Recipe.objects.get(owner=username, slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise Http404('No recipe matches the given query.')
    context = dict(recipe=recipe)
    return TemplateResponse(request, 'recipe/detail.html', context)


#@login_required
def recipe_edit(request, author, slug=None):
    if User.objects.get(username=author) != request.user:
        raise Http404()

    if request.method == 'POST':
        form = RecipeForm(request.POST, author=author, slug=slug)
        if form.is_valid():
            form.save()
    else:
        form = RecipeForm(author=author, slug=slug)
    return TemplateResponse(request, 'recipe/edit.html', {
        'form': form,
    })
