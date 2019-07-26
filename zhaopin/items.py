# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinItem(scrapy.Item):
    job_url = scrapy.Field()
    job_title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    post_time = scrapy.Field()
    type_of_empl = scrapy.Field()
    work_exp = scrapy.Field()
    min_edu_qual = scrapy.Field()
    num_of_ppl = scrapy.Field()
    occup_type = scrapy.Field()
    job_desc = scrapy.Field()
    co_profile = scrapy.Field()
