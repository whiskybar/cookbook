#! -*- coding: utf-8 -*-
from django.conf import settings
from django import forms

from cookbook.recipe.models import Recipe, IngredientGroup

class RecipeForm(forms.Form):
    name = forms.CharField(label='Název')
    slug = forms.CharField()
    perex = forms.CharField(label='Podtitul', required=False, widget=forms.Textarea)
    ingredients = forms.CharField(label='Ingredience', required=False, widget=forms.Textarea)
    procedure = forms.CharField(label='Postup', required=False, widget=forms.Textarea)
    notes = forms.CharField(label='Poznámka', required=False, widget=forms.Textarea)
    source = forms.CharField(label='Zdroj', required=False)
    tags = forms.CharField(label='Kategorie', required=False, widget=forms.Textarea)
    language = forms.ChoiceField(label='Jazyk', choices=settings.LANGUAGES)

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.slug = kwargs.pop('slug', None)
        if self.slug:
            self.instance = Recipe.objects.get(author=self.author, slug=self.slug)
        else:
            self.instance = Recipe(author=self.author)

        initial = {
            'name': self.instance.name,
            'slug': self.instance.slug,
            'perex': self.instance.perex,
            'ingredients': '\n'.join(self.instance.ingredients[0].ingredients)
                           if getattr(self.instance, 'ingredients', None) else '',
            'procedure': self.instance.procedure,
            'notes': self.instance.notes,
            'source': self.instance.source,
            'tags': '\n'.join(self.instance.tags),
            'procedure': self.instance.procedure,
            'language': self.instance.language or settings.LANGUAGES[0][0],
        }
        for key in initial:
            if key is None:
                initial[key] = ''
        kwargs['initial'] = initial
        super(RecipeForm, self).__init__(*args, **kwargs)

    def save(self):
        for field in ['name', 'slug', 'perex', 'procedure', 'notes', 'source', 'language']:
            setattr(self.instance, field, self.cleaned_data.get(field, ''))
        if self.slug:
            ingredientgroup = self.instance.ingredients[0]
        else:
            ingredientgroup = IngredientGroup(title='main')
        ingredientgroup.ingredients = filter(bool, self.cleaned_data.get('ingredients', '').split('\n'))
        self.instance.ingredients = [ingredientgroup]
        self.instance.tags = filter(bool, self.cleaned_data.get('tags', '').split('\n'))
        self.instance.save()
