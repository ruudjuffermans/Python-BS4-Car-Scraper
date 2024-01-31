from abc import ABC, abstractmethod
import mysql.connector as mysql
import json

class Pipeline(ABC):
    def __init__(self):
        self.data = {}

    def process(self, group, item):        
        if group not in self.data:
            self.data[group] = [] 
        self.data[group].append(dict(item))
        return item

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

class JsonPipeline(Pipeline):
    def __init__(self, filename="output.json"):
        super().__init__()
        self.filename = filename
        self.file = None

    def open(self):
        self.file = open(self.filename, 'w')

    def process(self, item, key="data"):       
        if key not in self.data:
            self.data[key] = [] 
        self.data[key].append(dict(item))
        return item

    def close(self):
        if self.file:
            json.dump(self.data, self.file, ensure_ascii=False, indent=4)
            self.file.close()


class CarModelPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.cnx = None
        self.cursor = None

    def open(self):
        self.cnx = mysql.connect(
            user='python_manager', 
            password='python_manager', 
            database='python',
            host='db', 
            port=3306
        )
        self.cursor = self.cnx.cursor()

    def process(self, item):
        table_name="car_models"
        sql = f'INSERT IGNORE INTO {table_name} (link, brand, model) VALUES ("%s", "%s", "%s")'
        formated_sql = sql % (item['link'], item['brand'], item['model'])
        try:
            self.cursor.execute(formated_sql)
            print(f"Executed SQL: {sql}")
            self.cnx.commit()
        except mysql.Error as err:
            print(f"Error: {err}")
            print(f"Error: {formated_sql}")
            self.cnx.rollback()

        return item

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()

class CarShallowPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.cnx = None
        self.cursor = None

    def open(self):
        pass
        self.cnx = mysql.connect(
            user='python_manager', 
            password='python_manager', 
            database='python',
            host='db', 
            port=3306
        )
        self.cursor = self.cnx.cursor()

    def process(self, item):
        table_name="car_shallows"
        sql = f'INSERT IGNORE INTO {table_name} ( model, brand, title, link, description, price, date, priority, seller) VALUES ( "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
        formated_sql = sql % (item['model'], item['brand'], item['title'], item['link'], item['description'], item['price'], item['date'], item['priority'], item['seller'])
        try:
            self.cursor.execute(formated_sql)
            print(f"Executed SQL: {formated_sql}")
            self.cnx.commit()
        except mysql.Error as err:
            print(f"Error: {err}")
            print(f"Error: {formated_sql}")
            self.cnx.rollback()

        return item

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()