#! -*- coding: utf-8 -*-
import os.path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from photologue.models import Gallery, Photo

from cookbook.recipe.models import Recipe
from cookbook.recipe.forms import RecipeForm


def recipe_search(request):
    query = request.GET and request.GET.get('q')
    if query:
        Recipe.objects.filter(name__icontains=query, slug__icontains=query)
    #FIXME: continue


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
@csrf_exempt
def gallery_upload(request, author, slug):
    if not request.FILES:
        return Http404()
    if User.objects.get(username=author) != request.user:
        raise Http404('Toto není váš recept')

    recipe = Recipe.objects.get(author=author, slug=slug)
    gallery = Gallery.objects.get_or_create(
        title='%s (%s)' % (slug, author),
        title_slug='%s-%s' % (author, slug),
    )[0]
    for name, ufile in request.FILES.iteritems():
        #TODO: refactor this ugly code
        count = 1
        while True:
            title = '%s-%s' % (slug, count)
            title_slug = slugify(title)
            try:
                Photo.objects.get(title_slug=title_slug)
            except Photo.DoesNotExist:
                break
            count = count + 1

        photo = Photo(title=title, title_slug=title_slug)
        photo.image.save(ufile.name, ufile)
        gallery.photos.add(photo)

    recipe.gallery_id = gallery.pk
    recipe.save()
    return HttpResponse('ok')

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
            return redirect(reverse('recipe_edit', kwargs=url_kwargs))
        else:
            messages.error(request, "Opravte chyby.")
    else:
        form = RecipeForm(author=author, slug=slug)

    return TemplateResponse(request, 'recipe/edit.html', {
        'form': form,
        'editing': bool(slug)
    })

@login_required
def recipe_delete(request, author, slug):
    if User.objects.get(username=author) != request.user:
        raise Http404('Toto není váš recept')
    recipe = Recipe.objects.get(author=author, slug=slug)

    if request.method == 'POST':
        gallery = recipe.gallery
        if gallery:
            gallery.delete()
        recipe.delete()
        messages.info(request, 'Recept "%s" byl úspěšně smazán.' % recipe)
        return redirect(reverse('user_homepage', kwargs={'username': author}))

    return TemplateResponse(request, 'recipe/delete.html', {
        'recipe': recipe,
    })


