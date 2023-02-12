from curses import A_CHARTEXT
import scrapy
from scrapy.exceptions import CloseSpider
import re
from re import sub
from decimal import Decimal


class ZooplaListingSpider(scrapy.Spider):
    name = 'zoopla_listing'
    start_urls = [
        'https://www.zoopla.co.uk/for-sale/property/london/',
    ]

    def __extract_zoopla_id(self, listing):
        
        div_id = listing.css('div::attr(id)').get()
        zoopla_id = div_id.replace("listing_", "")
        detail_anchor = listing.css('a::attr(href)').get()
        
        return zoopla_id, detail_anchor


    def parse(self, response):
        #Cycles through each property card 
        for listing in response.xpath('//div[contains(@id, "listing_")]'):

            # get hold of the zoopla ID.
            zoopla_id, zoopla_detail_href = self.__extract_zoopla_id(listing=listing)


            yield {
                'zoopla_id': zoopla_id,
                'zoopla_detail_href': zoopla_detail_href
            }
        get_url = None
        pagination = response.css('div[data-testid="pagination"]')
        a_tag = pagination.css('a::attr(aria-disabled)')[-1].extract()
        if(a_tag == 'true'):
            raise CloseSpider('No more Pages')

        get_url = pagination.css('a::attr(href)')[-1].extract()
        next_page_url = "https://www.zoopla.co.uk" + get_url
        yield scrapy.Request(next_page_url, callback=self.parse)
        
