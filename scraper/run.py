from scraper import parser
from scrapy.cmdline import execute
import itertools

if __name__ == '__main__':
    execute("scrapy crawl {}".format(parser.parse_args().spider).split())

