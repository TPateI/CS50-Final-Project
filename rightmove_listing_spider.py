import json
import scrapy


class RightmoveListingSpider(scrapy.Spider):
    name = 'rightmove_listing'
    start_urls = [
        'https://www.rightmove.co.uk/property-for-sale/London.html'
    ]
    count = 24

    def __extract_rightmove_id(self, listing):
        detail_anchor = listing.css('a::attr(href)').get()
        rightmove_id = None
        if len(detail_anchor) > 0:
            rightmove_id = detail_anchor.split('?')[0].split('/')[2].replace('#','')
            return rightmove_id, detail_anchor

    def parse(self, response):
        for listing in response.css('div.propertyCard-description'):
            rightmove_id, rightmove_detail_href = self.__extract_rightmove_id(listing=listing)

            yield{
                'rightmove_id': rightmove_id,
                'rightmove_detail_href': rightmove_detail_href
            }
        next_page_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E93917&index={}'.format(RightmoveListingSpider.count)
        yield scrapy.Request(next_page_url, callback=self.parse)
        RightmoveListingSpider.count += 24