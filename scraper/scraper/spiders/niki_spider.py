import scrapy
from scrapy.loader import ItemLoader
from ..items import RecipeItem

class NikiSpider(scrapy.Spider):
    name = 'nikib'
    start_urls = [
        'http://www.nikib.co.il'
    ]

    def parse(self, response: scrapy.http.HtmlResponse):
        # master_categories = response.css('ul#5 > li > a')
        master_categories = response.xpath('//ul[@id=5]/li/a')
        for category in master_categories:
            href = category.xpath('self::a/@href').get()
            yield scrapy.Request(href, callback=self.parse_category)

    def parse_category(self, response: scrapy.http.HtmlResponse):
        category_url = response.url
        urls_in_category = [category_url]
        try:
            last_page_in_category = int(response.xpath('//li[@class=\'first_last_page\']/a/text()').extract()[0])
            for page_no in range(1, last_page_in_category):
                urls_in_category.append(category_url + 'page/{}/'.format(page_no))
        except IndexError:
            print('Category {} has only one page'.format(category_url))

        for url in urls_in_category:
            yield scrapy.Request(url, callback=self.parse_category_page)


    def parse_category_page(self, response: scrapy.http.HtmlResponse):
        items = []
        all_recipes_in_page = response.xpath('//article')
        for recipe in all_recipes_in_page:
            num_of_child_p = len(recipe.xpath('div/div[@class=\'pf-content\']/p'))
            loader = ItemLoader(item=RecipeItem(), selector=recipe)
            loader.add_xpath('title', 'h1/a/text()')
            loader.add_xpath('origin_url', 'h1/a/@href')
            # loader.add_xpath('id', 'self::a/@href')
            item = loader.load_item()
            if not item.get('short_description') or not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/p/text()')
                item = loader.load_item()
            if not item.get('short_description') or  not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/p/span/text()')
                item = loader.load_item()
            if not item.get('short_description') or  not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/div/p/text()')
                item = loader.load_item()
            if not item.get('short_description') or not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/div/span/text()')
                item = loader.load_item()
            if not item.get('short_description') or not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/div/text()')
                item = loader.load_item()
            if not item.get('short_description') or not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/div/p/span/text()')
                item = loader.load_item()
            if not item.get('short_description') or not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/div/div/p/text()')
                item = loader.load_item()
            if not item.get('short_description') or not item['short_description'].strip().rstrip('\n').strip('\xa0'):
                loader.add_xpath('short_description', 'div/div[@class=\'pf-content\']/p/strong/text()')
                item = loader.load_item()
            # item['id'] = item['origin_url'].split('/')[-2]
            items.append(item)
        return items


# class NikiRecipeSpider(scrapy.Spider):
#
#     def parse(self, response: scrapy.http.HtmlResponse):
