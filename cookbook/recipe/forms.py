from django.conf import settings
from django import forms

from cookbook.recipe.models import Recipe


class RecipeForm(forms.Form):
    name = forms.CharField()
    slug = forms.CharField()
    perex = forms.CharField(required=False, widget=forms.Textarea)
    ingredients = forms.CharField(required=False, widget=forms.Textarea)
    procedure = forms.CharField(required=False, widget=forms.Textarea)
    notes = forms.CharField(required=False, widget=forms.Textarea)
    source = forms.CharField(required=False)
    tags = forms.CharField(required=False, widget=forms.Textarea)
    language = forms.ChoiceField(choices=zip(settings.LANGUAGES, settings.LANGUAGES))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', Recipe())
        self.instance.owner = self.user = kwargs.pop('user', self.instance.owner)
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
            'language': self.instance.language or settings.LANGUAGES[0],
        }
        for key in initial:
            if key is None:
                initial[key] = ''
        kwargs['initial'] = initial
        super(RecipeForm, self).__init__(*args, **kwargs)

    def save(self):
        self.instance.save()
