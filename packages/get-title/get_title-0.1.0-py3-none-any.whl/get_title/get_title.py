import requests
from bs4 import BeautifulSoup

def get_title(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  return soup.title.text