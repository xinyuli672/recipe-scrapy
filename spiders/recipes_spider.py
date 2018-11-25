import scrapy
#from recipes.items import RecipesItem
from scrapy import Request

class RecipesSpider(scrapy.Spider):
    name = "recipes"
    #link = "www.seriouseats.com"

    allowed_domains = ['seriouseats.com']
    start_urls = ['https://www.seriouseats.com/recipes']


    def parse(self, response):
        categories = response.xpath('//header[@class="header-global nav-closed"]/div[@class="header-wrapper"]/nav[@class="nav-global"]/div[@class="nav-global-outer-wrapper"]/div[@class="nav-global-inner-wrapper"]/ul[@class="nav-global-links self-clear"]/li/div[@class="subnav" and @data-subnav-index="0"]/ul[@class="subnav-links self-clear"]/li[@class=""]')
        for linktocategory in categories:
            link = linktocategory.xpath('a/@href').extract_first()
            yield scrapy.Request(link, callback=self.parse_Category)
    
    def parse_Category(self, response):
        allrecipes_list = response.xpath('//section[@class="block block-primary block-no-nav block-has-kicker"]/div[@class="block__wrapper"]/div[@class="module"]/div[@class="module__wrapper"]/div[@class="metadata"]')
        for linktorecipe in allrecipes_list:
            url = linktorecipe.xpath('a[@class="module__link"]/@href').extract_first()
            title = linktorecipe.xpath('a[@class="module__link"]/h4[@class="title"]/text()').extract_first()
            yield scrapy.Request(url, callback=self.parse_Recipe,meta={'URL': url, 'Title': title})

    def parse_Recipe(self, response):
        self.logger.info("Visited %s", response.url)
        url = response.meta.get('URL')
        title = response.meta.get('Title')

        content = "".join(line for line in response.xpath('//script[@type="application/ld+json"]/text()')[-1].extract())

        yield{'URL': url, 'Title': title, 'Content': content}