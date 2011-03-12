from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from cookbook.recipe.models import Recipe


def user_homepage(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user.username)

    context = dict(user=user, recipes=recipes)
    return TemplateResponse(request, 'user/homepage.html', context)
