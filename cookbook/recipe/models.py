import mongoengine
from mongoengine.queryset import queryset_manager
from photologue.models import Gallery

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404


"""
recipes = [
    {
        'name': ..,
        'ingredients': [
            {
                'title': ...,
                'ingredients': [
                    ...,
                    ...,
                ],
            },
            {
                'title': ...,
                'ingredients': [
                    ...,
                    ...,
                ],
            }
        ],
        'procedure': ...,
        'notes': ...,
        'source': ...,
        'tags': [..., ..., ...]
        'language': ...,
    }
]
"""

mongoengine.connect(settings.MONGO_DB_NAME)

class IngredientGroup(mongoengine.EmbeddedDocument):
    title = mongoengine.StringField()
    ingredients = mongoengine.ListField(
        mongoengine.StringField()
    )



class Recipe(mongoengine.Document):
    name = mongoengine.StringField()
    slug = mongoengine.StringField()
    perex = mongoengine.StringField()
    ingredients = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(IngredientGroup)
    )
    procedure = mongoengine.StringField()
    notes = mongoengine.StringField()
    source  = mongoengine.StringField()
    tags = mongoengine.ListField(
        mongoengine.StringField()
    )
    gallery_id = mongoengine.IntField()
    language = mongoengine.StringField(choices=dict(settings.LANGUAGES).keys())
    author = mongoengine.StringField()

    def __unicode__(self):
        return self.name

    @property
    def gallery(self):
        try:
            return Gallery.objects.get(pk=self.gallery_id)
        except Gallery.DoesNotExist:
            return None

    def get_absolute_url(self):
        url_kwargs = dict(author=self.author, slug=self.slug)
        return reverse('recipe_detail', kwargs=url_kwargs)

    def get_edit_url(self):
        url_kwargs = dict(author=self.author, slug=self.slug)
        return reverse('recipe_edit', kwargs=url_kwargs)
