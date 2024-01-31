import requests


data = requests.get("https://www.marktplaats.nl/v/auto-s/alfa-romeo/m1928327854-alfa-romeo-giulietta-1-4t-distinctive-2015-zeer-nette-auto").text

file_path = "scraped.txt"
with open(file_path, 'w') as file:
    file.write(data)