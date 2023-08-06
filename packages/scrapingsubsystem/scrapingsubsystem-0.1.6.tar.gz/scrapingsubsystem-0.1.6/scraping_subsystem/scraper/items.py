# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Review(scrapy.Item):
    """Класс контейнер для хранения данных скраппинга

    Args:
        scrapy (_type_): _description_
    """
    review_url = scrapy.Field()
    author = scrapy.Field()
    review_date = scrapy.Field()
    text_data = scrapy.Field()

class Product(scrapy.Item):
    product_url = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
