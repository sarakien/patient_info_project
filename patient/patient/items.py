# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PatientItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    group  = scrapy.Field()
    post_title = scrapy.Field()
    post_user = scrapy.Field()
    post_likes = scrapy.Field()
    num_replies = scrapy.Field()
    post_date = scrapy.Field()
    num_following = scrapy.Field()
    post_text = scrapy.Field()
    reply_user = scrapy.Field()
    reply_text = scrapy.Field()
