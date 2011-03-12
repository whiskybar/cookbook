from django.conf import settings
from django import forms


class RecipeForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.CharField(max_length=100)
    perex = form.TextField(required=False)
    ingredients = form.TextField(required=False)
    procedure = form.TextField(required=False)
    notes = form.TextField(required=False)
    source = forms.CharField(max_length=100, required=False)
    tags = form.TextField(required=False)
    language = forms.ChoiceField(choices=zip(settings.LANGUAGES, settings.LANGUAGES))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', Recipe())
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
