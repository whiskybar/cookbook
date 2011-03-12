from django.db import models
from django.conf import settings

import mongoengine

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
    language = mongoengine.StringField(choices=settings.LANGUAGES)
    owner = mongoengine.StringField()

    def per_user(self, username):
        return mongoengine.QuerySet().find(owner=username)


