from .etl import ETLBase
from bs4 import BeautifulSoup
from src.extracts import Scraper 
from src.items import Item, ShallowItem
from src.pipelines import JsonPipeline, CarModelPipeline, CarShallowPipeline

class ETLCarModels():
    def __init__(self):
        self.base_url = 'https://www.marktplaats.nl'
        self.followup_urls = []
        self.extract = Scraper()
        self.pipeline = CarModelPipeline()

    def run(self):
        start_url = "https://www.marktplaats.nl/cp/91/auto-kopen/"
        self.pipeline.open()
        soup = self.extract.get_data(url=start_url)
        for group in soup.find_all('ul', class_='CarsCategoryLinks-subList'):
            brand = group.find(class_='car-brand').text
            for car_model in group.find_all('a', class_='car-model'):
                model = car_model.text
                link = car_model.get("href")
                item = ShallowItem(
                            link=link,
                            model=model,
                            brand=brand,
                        )

                self.pipeline.process(item)
        self.pipeline.close()

    # def parse(self, response):
    #     soup = BeautifulSoup(response, 'html.parser')
    #     for group in soup.find_all('ul', class_='CarsCategoryLinks-subList'):
    #         brand = group.find(class_='car-brand').text
    #         for car_model in group.find_all('a', class_='car-model'):
    #             model = car_model.text
    #             link = car_model.get("href")
    #             item = ShallowItem(
    #                         link=link,
    #                         model=model,
    #                         brand=brand,
    #                     )

    #             yield item


    # def collect(self, start_url):
    #     url_addition = '/l/auto-s/alfa-romeo/f/159/546/'
    #     start_page = 1
    #     end_page = 20 
    #     self.pipeline.open()
    #     for page in range(start_page, end_page + 1):
    #         url = f'{self.base_url}/q/{url_addition}/'
    #         for data in self.extract.get_data(url=url, callback=self.parse):
    #             for item in data:
    #                 self.pipeline.process(url, item)
    #     self.pipeline.close()

    # def parse(self, response):
    #     soup = BeautifulSoup(response, 'html.parser')
    #     for listing in soup.find_all('li', class_='hz-Listing'):
    #         title = listing.find(class_='hz-Listing-title').text
    #         link = listing.find('a', class_='hz-Listing-coverLink').get('href')
    #         description = listing.find(class_='hz-Listing-description').text
    #         price = listing.find(class_='hz-Listing-price').text
    #         date = listing.find(class_='hz-Listing-date').text
    #         priority = listing.find(class_='hz-Listing-priority').text
    #         seller = listing.find(class_='hz-Listing-seller-name').text

    #         item = Item(
    #                     title=title,
    #                     link=link,
    #                     description=description,
    #                     price=price,
    #                     date=date,
    #                     priority=priority,
    #                     seller=seller
    #                 )

    #         yield item



# class CollectCarShallows(ETLBase):
#     def __init__(self):
#         self.base_url = 'https://www.marktplaats.nl'
#         self.followup_urls = []
#         self.extract = Scraper()
#         self.pipeline = CarShallowPipeline()

#     def collect(self):
#         url_addition = '/l/auto-s/toyota/f/aygo/1241/'
#         self.pipeline.open()
#         start_page = 1
#         url = f'{self.base_url}{url_addition}p/{start_page}/'
#         print(url)
#         for data in self.extract.get_data(url=url, callback=self.parse_init):
#             print(data)
#         end_page = 2 
#         for page in range(start_page, end_page + 1):
#             url = f'{self.base_url}{url_addition}p/{page}/'
#             for data in self.extract.get_data(url=url, callback=self.parse):
#                 for item in data:
#                     print(item)
#                     self.pipeline.process(item)
#         self.pipeline.close()
    
#     def parse(self, response):
#         soup = BeautifulSoup(response, 'html.parser')
#         for listing in soup.find_all('li', class_='hz-Listing'):
#             title = listing.find(class_='hz-Listing-title').text
#             link = listing.find('a', class_='hz-Listing-coverLink').get('href')
#             description = listing.find(class_='hz-Listing-description').text
#             price = listing.find(class_='hz-Listing-price').text
#             date = listing.find(class_='hz-Listing-date').text if listing.find(class_='hz-Listing-date') is not None else "N/A"
#             priority = listing.find(class_='hz-Listing-priority').text if listing.find(class_='hz-Listing-priority') is not None else "N/A"
#             seller = listing.find(class_='hz-Listing-seller-name').text

#             item = Item(
#                         title=title,
#                         link=link,
#                         description=description,
#                         price=price,
#                         date=date,
#                         priority=priority,
#                         seller=seller
#                     )

#             yield item

#     def parse_init(self, response):
#         print("hi")
#         soup = BeautifulSoup(response, 'html.parser')
#         resultaat_count = soup.find_all('li', class_='hz-Breadcrumb')[-1]
#         pagina_nav = soup.find('nav', class_='hz-PaginationControls-pagination')
#         print(resultaat_count.text)
#         print(pagina_nav.findChildren(recursive=False)[-1].get("href"))
#         print(pagina_nav)
#         return resultaat_count.text.split(" ")[0]
