
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import TakeFirst, Join
from mongoengine import *

class ItemModel(Document):

    @classmethod
    def from_item(cls, item: scrapy.Item):
        inst = cls()
        for k, v in item.items():
            setattr(inst, k, v)
        return inst

    meta = {
        'abstract': True
    }


class RecipeItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    origin_url = scrapy.Field(output_processor=TakeFirst())
    image_url = scrapy.Field(output_processor=TakeFirst())
    short_description = scrapy.Field(output_processor=Join())
    raw_content = scrapy.Field(output_processor=TakeFirst())


class Feature(EmbeddedDocument):
    name = StringField(required=True)
    exists = BooleanField()


class Recipe(ItemModel):
    title = StringField(required=True)
    origin_url = URLField(required=True)
    image_url = URLField()
    short_description = StringField()
    content_cheksum = StringField()
    raw_content = StringField()
    features = EmbeddedDocumentListField(Feature)

    def __eq__(self, other):
        if isinstance(other, RecipeItem):
            return self.title == other['title'] \
                   and self.origin_url == other.get('origin_url', None) \
                   and self.image_url == other.get('image_url', None) \
                   and self.short_description == other.get('short_description', None) \
                   and self.raw_content == other.get('raw_content', None)
        else:
            return super().__eq__(other)




class Ingredient:
    text = scrapy.Field() # Original text as it was seen in the website
    name = scrapy.Field() # The ingredient's name
    amount = scrapy.Field() #
    amount_unit = scrapy.Field()


class Instruction:
    ordinal_number = scrapy.Field()
    text = scrapy.Field()



# region ML entities

class Sentence(ItemModel):

    content = StringField()
    hashcode = StringField()

# endregion