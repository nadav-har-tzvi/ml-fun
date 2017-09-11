import scrapy
import os
from hashlib import md5
from ..items import Sentence

base_dir = '{}/scraper/ml_inputs'.format(os.getcwd())



class MLSpider(scrapy.Spider):
    name = 'ml'
    start_urls = ['file://{}/{}'.format(base_dir, fname) for fname in os.listdir(base_dir)]


    def parse(self, response):

        rows = response.xpath('//div[@class=\'main\']/div[@class=\'mainResults\']/table/tr')
        for row in rows:
            hasher = md5()
            before = row.xpath('td[@class=\'before\']/text()').extract()
            middle = row.xpath('td[@class=\'middle\']/text()').extract()
            after = row.xpath('td[@class=\'after\']/text()').extract()
            b = before and before[0]
            m = middle and middle[0]
            a = after and after[0]
            if not m:
                continue
            content = ' '.join([b or '', m, a or ''])
            hasher.update(content.encode('utf-8'))
            hashcode = hasher.hexdigest()
            if not Sentence.objects(hashcode=hashcode):
                Sentence(content=content, hashcode=hashcode).save()



