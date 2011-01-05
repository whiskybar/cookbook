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
    language = mongoengine.StringField()
    owners = mongoengine.ListField(
        mongoengine.IntField()
    )

    def per_user(self, user_id):
        return mongoengine.QuerySet().find(owners__contains=user_id)


