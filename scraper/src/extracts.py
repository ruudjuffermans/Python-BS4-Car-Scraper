from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import mysql.connector as mysql
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class ExtractBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class Scraper(ExtractBase):
    def __init__(self):
        pass

    def get_data(self, url):
        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            response = session.get(url)
            # response = requests.get(url, proxies={"https": "http://77.79.187.74:8080", "http": "http://77.79.187.74:8080"})
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve the webpage: {e}")
            



class DB(ExtractBase):
    def __init__(self):
        pass

    def return_data(self, link):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor()
            
            update_query = f'UPDATE car_models SET state = "DONE" WHERE link = "{link}";'
            cursor.execute(update_query)

            cnx.commit()
            cursor.close()
            cnx.close()

            return

        except mysql.Error as err:
            print(f"Error: {err}")
    def get_listing(self):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor(dictionary=True)
            cnx.start_transaction()
            update_query = "UPDATE car_shallows SET state = 'DOING' WHERE state = 'TODO' LIMIT 1;"
            cursor.execute(update_query)
            cnx.commit()

            select_query = "SELECT * FROM car_shallows WHERE state = 'DOING' LIMIT 1;"
            cursor.execute(select_query)
            data = cursor.fetchone()
                
            cursor.close()
            cnx.close()

            return data

        except mysql.Error as err:
            print(f"Error: {err}")
    def return_listing(self, link):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor(dictionary=True)
            cnx.start_transaction()
            update_query = f'UPDATE car_shallows SET state = "DONE" WHERE link = "{link}";'
            cursor.execute(update_query)
            cnx.commit()

            cursor.close()
            cnx.close()

            return
        except mysql.Error as err:
            print(f"Error: {err}")
    def error_listing(self, link):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor(dictionary=True)
            cnx.start_transaction()
            update_query = f'UPDATE car_shallows SET state = "ERROR" WHERE link = "{link}";'
            cursor.execute(update_query)
            cnx.commit()

            cursor.close()
            cnx.close()

            return

        except mysql.Error as err:
            print(f"Error: {err}")
    def success_shallow(self, link):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor(dictionary=True)
            cnx.start_transaction()
            update_query = f'UPDATE car_models SET state = "DONE" WHERE link = "{link}";'
            cursor.execute(update_query)
            cnx.commit()

            cursor.close()
            cnx.close()

            return
        except mysql.Error as err:
            print(f"Error: {err}")

    def error_shallow(self, link):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor(dictionary=True)
            cnx.start_transaction()
            update_query = f'UPDATE car_models SET state = "ERROR" WHERE link = "{link}";'
            cursor.execute(update_query)
            cnx.commit()

            cursor.close()
            cnx.close()

            return

        except mysql.Error as err:
            print(f"Error: {err}") 

    def get_data(self):
        try:
            cnx = mysql.connect(
                user='python_manager', 
                password='python_manager', 
                database='python',
                host='db', 
                port=3306
            )
            cursor = cnx.cursor(dictionary=True)
            cnx.start_transaction()
            
            select_query = "SELECT * FROM car_models WHERE state = 'TODO' LIMIT 1;"
            cursor.execute(select_query)

            data = cursor.fetchone()
            if data:
                update_query = "UPDATE car_models SET state = 'DOING' WHERE link = %s;"
                cursor.execute(update_query, (data['link'],))

            cnx.commit()
            cursor.close()
            cnx.close()

            return data

        except mysql.Error as err:
            print(f"Error: {err}")