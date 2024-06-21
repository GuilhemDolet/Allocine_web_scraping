# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    press_score = scrapy.Field()
    public_score = scrapy.Field()
    mention = scrapy.Field()
    genre = scrapy.Field()
    years = scrapy.Field()
    time = scrapy.Field()
    description = scrapy.Field()
    actors = scrapy.Field()
    realisator = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()

class SerieAllocinescrapperItem(ImdbscrapperItem):
    année_de_diffusion = scrapy.Field()
    status = scrapy.Field()
    nbr_saisons = scrapy.Field()
    nbr_episodes = scrapy.Field()


