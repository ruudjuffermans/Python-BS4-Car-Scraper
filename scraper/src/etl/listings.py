from .etl import ETLBase
from bs4 import BeautifulSoup
from src.extracts import Scraper, DB
from src.items import Item, ShallowItem
from src.pipelines import JsonPipeline, CarShallowPipeline
import time
from datetime import datetime
import requests
from pymongo import MongoClient

class ETLCarListings():
    def __init__(self):
        self.base_url = 'https://www.marktplaats.nl'
        self.data = None
        self.db = DB()

    def collect(self):
        # with open("scraped.txt", 'r') as file:
        #     self.data = file.read()
        return self.db.get_listing()

    def run(self):
        source = self.collect()
        try:
            data = requests.get(f"https://www.marktplaats.nl{source['link']}").text
            car_dict = dict()
            car_dict['timestamp'] = datetime.now().strftime('%Y-%m-%d')
            soup = BeautifulSoup(data, 'html.parser')
            car_dict['title'] = soup.find(class_='Listing-title').text
            car_dict['description'] = soup.find(class_='Description-root').text
            car_dict['price'] = soup.find(class_='Listing-price').text
            car_dict['visits'], car_dict['likes'], car_dict['date'] = [item.text for item in soup.find_all(class_='Stats-stat')]
            car_keyvals = soup.find_all(class_='CarUspBlocks-block')
            for x in car_keyvals:
                value = x.find(class_='CarUspBlocks-value')
                title = x.find(class_='CarUspBlocks-title')
                try:
                    car_dict[title.text] = value.text
                except:
                    pass
            car_keyvals = soup.find_all(class_='CarAttributes-itemWithIcon')
            for x in car_keyvals:
                value = x.find(class_='CarAttributes-value')
                title = x.find(class_='CarAttributes-label')
                try:
                    car_dict[title.text] = value.text
                except:
                    pass
            car_keyvals = soup.find_all(class_='CarAttributesAccordion-bodyItems')
            for x in car_keyvals:
                value = x.find(class_='CarAttributesAccordion-bodyItemValue')
                title = x.find(class_='CarAttributesAccordion-bodyItemLabel')
                try:
                    car_dict[title.text] = value.text
                except:
                    pass
            client = MongoClient("mongodb://mongodb:27017")
            db = client["db"]
            db.listings.insert_one(car_dict)
            self.db.return_listing(source['link'])
        except Exception as e:
            print(f"Error: {e}")
            self.db.error_listing(source['link'])
            print("exiting this listing!!!")
            return



