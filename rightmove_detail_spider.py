import scrapy
import json
import re
from re import sub
from decimal import Decimal

class RightmoveDetailSpider(scrapy.Spider):
    name = 'rightmove_detail'
    start_urls = []

    with open('rightmove_listing.json', 'r') as file:
        rightmove_listing_entries = json.loads(file.read())
        for rightmove_listing_entry in rightmove_listing_entries:
            start_url = 'https://www.rightmove.co.uk{}'.format(rightmove_listing_entry.get('rightmove_detail_href'))
            start_urls.append(start_url)
            print('added {} to the list of start_urls'.format(start_url))
    

    def parse(self, response):
        raw_data = None
        for i in range(len(response.css('script::text').getall())):
            if('window.PAGE_MODEL' in response.css('script::text').getall()[i]):
                raw_data = response.css('script::text').getall()[i]
        formatted_data = raw_data.replace('    window.PAGE_MODEL = ', '')
        listing_details = json.loads(formatted_data).get('propertyData')
        listing_id = listing_details.get('id')
        title = listing_details.get('text').get('shortDescription')
        detailed_description = listing_details.get('text').get('description')
        meta_title = listing_details.get('text').get('pageTitle')
        meta_description = listing_details.get('text').get('shareDescription')
        display_address = listing_details.get('address').get('displayAddress')
        raw_price = listing_details.get('prices').get('primaryPrice')
        outcode = listing_details.get('address').get('outcode')
        incode = listing_details.get('address').get('incode')
        postalcode = outcode + " " + incode
        latitude = listing_details.get('location').get('latitude')
        longitude = listing_details.get('location').get('longitude')
        price = 'POA'
        if(raw_price != 'POA'):
            price = sub(r'[^\d.]', '', raw_price)

        yield{
            'url': response.request.url,
            'listing_id': listing_id,
            'title': title,
            'detailed_description': detailed_description,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'display_address': display_address,
            'postalcode': postalcode,
            'price': price,
            'latitude': latitude,
            'longitude': longitude,         
        } 

