from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from cookbook.recipe.models import Recipe


def user_homepage(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(owner=user.username)

    context = dict(user=user, recipes=recipes)
    return direct_to_template(request, 'user/user_homepage.html', context)
