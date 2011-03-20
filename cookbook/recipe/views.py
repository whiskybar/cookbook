#! -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cookbook.recipe.models import Recipe
from cookbook.recipe.forms import RecipeForm


def recipe_detail(request, author, slug):
    try:
        recipe = Recipe.objects.get(author=author, slug=slug)
    except Recipe.DoesNotExist:
        raise Http404('No recipe matches the given query.')
    if request.user and request.user.username == author:
        owner = True
    else:
        owner = False
    context = dict(recipe=recipe, owner=owner)
    return TemplateResponse(request, 'recipe/detail.html', context)


@login_required
def recipe_edit(request, author, slug=None):
    if User.objects.get(username=author) != request.user:
        raise Http404()

    if request.method == 'POST':
        form = RecipeForm(request.POST, author=author, slug=slug)
        if form.is_valid():
            form.save()
            messages.success(request, "Recept byl úspěšně uložen.")
            url_kwargs = dict(author=request.user.username, slug=form.cleaned_data['slug'])
            redirect(reverse('recipe_edit', kwargs=url_kwargs))
        else:
            messages.error(request, "Opravte chyby.")
    else:
        form = RecipeForm(author=author, slug=slug)

    return TemplateResponse(request, 'recipe/edit.html', {
        'form': form,
        'editing': bool(slug)
    })
