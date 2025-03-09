# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    """
    item definition for data from IMDB
    """
    title = scrapy.Field()
    rating = scrapy.Field()
    popularity = scrapy.Field()
    year = scrapy.Field()
    meta_score = scrapy.Field()
    tags = scrapy.Field()
    budget = scrapy.Field()
    first_us_ca = scrapy.Field()
