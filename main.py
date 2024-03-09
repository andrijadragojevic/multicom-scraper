import pandas as pd
import requests
from bs4 import BeautifulSoup
from g4f.client import Client

file_path = './components.txt'

url = "https://www.multicom.me/k/komponente"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.google.com"}

file = open(file_path, 'w')

component_categories = []
component_category_names = []

response = requests.get(url, headers=headers).content

soup = BeautifulSoup(response, "html.parser")

for div in soup.find_all('div', class_='kockica-grupa'):
  component_categories.append(
      f"https://www.multicom.me/{div.find('a')['href']}")
  component_category_names.append(
      f"{div.find('div', class_='ArtikalNaslov').text}")

#print(component_categories)

for index, category_link in enumerate(component_categories):
  file.write(f"\n\n{component_category_names[index]}\n")
  response = requests.get(category_link, headers=headers).content
  soup = BeautifulSoup(response, 'html.parser')

  number_of_articles_span = soup.select_one('div.broj > span')
  number_of_articles = 0
  
  if number_of_articles_span:
    number_of_articles = int(number_of_articles_span.text)
  page = 1

  while number_of_articles > 0:
    response = requests.get(f'{category_link}?page={page}&vrstaprikaza=kocka',
                            headers=headers).content
    soup = BeautifulSoup(response, 'html.parser')

    for article in soup.find_all('div', class_='artikal-n'):
      file.write(
          f"{article.find('h2').find('a').text} - {article.find('p', class_='cijenaGotovina').text}\n"
      )
      number_of_articles -= 1
    page += 1

file.close()
