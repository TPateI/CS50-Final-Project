import json
import scrapy


class ZooplaDetailSpider(scrapy.Spider):
    name = 'zoopla_detail'
    start_urls = []

    with open('zoopla_listing.json', 'r') as file:
        zoopla_listing_entries = json.loads(file.read())
        for zoopla_listing_entry in zoopla_listing_entries:
            start_url = 'https://www.zoopla.co.uk{}'.format(zoopla_listing_entry.get('zoopla_detail_href'))
            start_urls.append(start_url)
            print('added {} to the list of start_urls'.format(start_url))

    def parse(self, response):

        next_data = response.css('script[id="__NEXT_DATA__"]::text').get()

        listing_details = json.loads(next_data).get('props').get('pageProps').get('listingDetails')

        listing_id = listing_details.get('listingId')
        title = listing_details.get('title')
        detailed_description = listing_details.get('detailedDescription')
        meta_title = listing_details.get('metaTitle')
        meta_description = listing_details.get('metaDescription')
        display_address = listing_details.get('displayAddress')
        postalcode = listing_details.get('location').get('postalCode')    
        latitude = listing_details.get('location').get('coordinates').get('latitude')
        longitude = listing_details.get('location').get('coordinates').get('longitude')
        price = listing_details.get('adTargeting').get('price')

        yield {
            'url': response.request.url,
            'listing_id': listing_id,
            'title': title,
            'detailed_description': detailed_description,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'display_address': display_address,
            'postalcode': postalcode,
            'price': str(price),
            'latitude': latitude,
            'longitude': longitude,
        }
