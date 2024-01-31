from .etl import ETLBase
from bs4 import BeautifulSoup
from src.extracts import Scraper, DB
from src.items import Item, ShallowItem
from src.pipelines import JsonPipeline, CarShallowPipeline
import time

def clean_string(input_str):
    return input_str.replace('"', '').replace(',', '').replace("'", '').replace('.', '')


class ETLCarShallows():
    def __init__(self):
        self.base_url = 'https://www.marktplaats.nl'
        self.model = None
        self.extract = Scraper()
        self.db = DB()
        self.pipeline = CarShallowPipeline()

    def collect(self):
        return self.db.get_data()


    def run(self):
        model =  self.collect()
        try: 
            start_page = 1
            end_page = 10
            self.pipeline.open()
            for page in range(start_page, end_page + 1):
                url = f'{self.base_url}{model['link']}p/{page}/'
                soup = self.extract.get_data(url=url)

                shallow_dict = dict()
                shallows_arr = soup.find_all('li', class_='hz-Listing')
                if len(shallows_arr) == 0:
                    print("no more records, BREAK!")
                    break
                print("sleep... 2s")
                time.sleep(2)
                for listing in shallows_arr:
                    shallow_dict['model'] = model['model']
                    shallow_dict['brand'] = model['brand']
                    shallow_dict['title'] = clean_string(listing.find(class_='hz-Listing-title').text)
                    shallow_dict['link'] = listing.find('a', class_='hz-Listing-coverLink').get('href')
                    shallow_dict['description'] = clean_string(listing.find(class_='hz-Listing-description').text)
                    shallow_dict['price'] = listing.find(class_='hz-Listing-price').text
                    shallow_dict['date'] = listing.find(class_='hz-Listing-listingDate').text if listing.find(class_='hz-Listing-listingDate') is not None else "N/A"
                    shallow_dict['priority'] = listing.find(class_='hz-Listing-priority').text if listing.find(class_='hz-Listing-priority') is not None else "N/A"
                    shallow_dict['seller'] = clean_string(listing.find(class_='hz-Listing-seller-name').text)

                    self.pipeline.process(shallow_dict)
            self.pipeline.close()
            self.db.success_shallow(model['link'])

        except Exception as e:
            print(f"Error: {e}")
            self.db.error_shallow(model['link'])
            print("exiting this listing!!!")
            return
    # def collect(self):
    #     url_addition = '/l/auto-s/toyota/f/aygo/1241/'
    #     self.pipeline.open()
    #     url = f'{self.base_url}{url_addition}p/{start_page}/'
    #     for data in self.extract.get_data(url=url, callback=self.parse_init):
    #         print(data)
    #     end_page = 2 
    #     for page in range(start_page, end_page + 1):
    #         url = f'{self.base_url}{url_addition}p/{page}/'
    #         for data in self.extract.get_data(url=url, callback=self.parse):
    #             for item in data:
    #                 print(item)
    #                 self.pipeline.process(item)
    #     self.pipeline.close()
    def parse_init(self, response):
        # self.db.update_import_count(self.register_model)
        soup = BeautifulSoup(response, 'html.parser')
        resultaat_count = soup.find_all('li', class_='hz-Breadcrumb')[-1]
        pagina_nav = soup.find('nav', class_='hz-PaginationControls-pagination')
        yield resultaat_count.text.split(" ")[0]

    def parse(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        for listing in soup.find_all('li', class_='hz-Listing'):
            title = listing.find(class_='hz-Listing-title').text
            link = listing.find('a', class_='hz-Listing-coverLink').get('href')
            description = listing.find(class_='hz-Listing-description').text
            price = listing.find(class_='hz-Listing-price').text
            date = listing.find(class_='hz-Listing-date').text if listing.find(class_='hz-Listing-date') is not None else "N/A"
            priority = listing.find(class_='hz-Listing-priority').text if listing.find(class_='hz-Listing-priority') is not None else "N/A"
            seller = listing.find(class_='hz-Listing-seller-name').text

            item = Item(
                        title=title,
                        link=link,
                        description=description,
                        price=price,
                        date=date,
                        priority=priority,
                        seller=seller
                    )

            yield item


