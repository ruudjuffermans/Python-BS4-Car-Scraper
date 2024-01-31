import datetime

def clean_string(input_str):
    return input_str.replace('"', '').replace(',', '').replace("'", '').replace('.', '')

class ShallowItem(dict):
    def __init__(self, link, model, brand):
        self['link'] = link
        self['model'] = model
        self['brand'] = brand
        
class ListingsItem(dict):
    def __init__(self, link, model, brand):
        self['link'] = link
        self['model'] = model
        self['brand'] = brand

class Item(dict):
    def __init__(self, title, link, description, price, date, priority, seller):
        self.validate_input(title, link, description, price, date, priority, seller)
        date = self.parse_date(date)

        self['title'] = clean_string(title)
        self['link'] = link
        self['description'] = clean_string(description)
        self['price'] = price
        self['date'] = date
        self['priority'] = priority
        self['seller'] = clean_string(seller)

    def parse_date(self, date_str):
        # Convert 'vandaag' to the current date
        if date_str.lower() == 'vandaag':
            return datetime.date.today().strftime('%Y-%m-%d')
        
        # Convert 'gisteren' to the date of yesterday
        if date_str.lower() == 'gisteren':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            return yesterday.strftime('%Y-%m-%d')

        # Convert 'eergisteren' to the date of the day before yesterday
        if date_str.lower() == 'eergisteren':
            day_before_yesterday = datetime.date.today() - datetime.timedelta(days=2)
            return day_before_yesterday.strftime('%Y-%m-%d')
        try:
            date_parts = date_str.strip("'").strip(".")
            if len(date_parts) == 3:
                day = int(date_parts[0])
                month_str = date_parts[1]
                year_str = date_parts[2].strip("'")
                
                # Map month names to their corresponding numbers
                month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
                month = month_names.index(month_str.lower()) + 1
                
                # Calculate the full year, assuming years like '24' are in the 2000s
                if len(year_str) == 2:
                    year = int('20' + year_str)
                else:
                    year = int(year_str)

                return datetime.date(year, month, day)
        except ValueError:
            return date_str.strip("'").strip(".")

        
    def validate_input(self, title, link, description, price, date, priority, seller):
        missing_fields = []

        if not title:
            missing_fields.append("title")
        if not link:
            missing_fields.append("link")
        if not description:
            missing_fields.append("description")
        if not price:
            missing_fields.append("price")
        if not date:
            missing_fields.append("date")
        if not priority:
            missing_fields.append("priority")
        if not seller:
            missing_fields.append("seller")

        if missing_fields:
            return


