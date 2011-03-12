from django.conf import settings
from django import forms

from cookbook.recipe.models import Recipe, IngredientGroup


class RecipeForm(forms.Form):
    name = forms.CharField()
    slug = forms.CharField()
    perex = forms.CharField(required=False, widget=forms.Textarea)
    ingredients = forms.CharField(required=False, widget=forms.Textarea)
    procedure = forms.CharField(required=False, widget=forms.Textarea)
    notes = forms.CharField(required=False, widget=forms.Textarea)
    source = forms.CharField(required=False)
    tags = forms.CharField(required=False, widget=forms.Textarea)
    language = forms.ChoiceField(choices=settings.LANGUAGES)

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
            'ingredients': ''.join('\n'.join(group.ingredients for group in self.instance.ingredients)),
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
        ingredientgroup.ingredients = self.cleaned_data.get('ingredients', '').split('\n')
        self.instance.ingredients = [ingredientgroup]
        self.instance.tags = self.cleaned_data.get('tags', '').split('\n')
        self.instance.save()
