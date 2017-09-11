# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from . import items
from scrapy.exceptions import DropItem
from mongoengine import connect

connect('local')

class DuplicatesRecipesPipeline(object):

    def __init__(self):
        super().__init__()
        self.recipes = set()

    def process_item(self, item: items.RecipeItem, spider):

        existing_item = items.Recipe.objects(origin_url=item['origin_url'])
        existing_item = existing_item and existing_item[0]
        if existing_item and existing_item == item:
            raise DropItem('Recipe already in database: {}'.format(item))
        elif item['origin_url'] not in self.recipes:
            self.recipes.add(item['origin_url'])
        else:
            raise DropItem('Received duplicate recipe: {}'.format(item))

        return item


class StorePipeline(object):

    def process_item(self, item: items.RecipeItem, spider):
        recipe = items.Recipe.objects(origin_url=item['origin_url'])
        recipe = recipe and recipe[0]
        if recipe:
            recipe.update(**item)
        else:
            recipe = items.Recipe.from_item(item)
        recipe.save()
        return item