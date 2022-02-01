import random
import re
import cloudscraper
import requests
from bs4 import BeautifulSoup


# URL generation
def url_gen():
	alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
	page_url = 'https://prnt.sc/2'
	while len(page_url) <= 21:
		page_url += random.choice(alphabet)
	return page_url

# Filename generation from URL
def name_gen(page_url):
	sep = '2'
	name = page_url.split(sep, 1)[1]
	return name

# Extracting image URL
def get_img_url(page_url):
	scraper = cloudscraper.create_scraper()
	req = scraper.get(page_url).text
	soup = BeautifulSoup(req, 'lxml')
	try:
		img_url = re.search("(?P<url>https?://[^\s]+)", str(
			soup.find("img", class_='no-click screenshot-image'))).group("url")
		return img_url
	except AttributeError:
		return 'No screenshot found'

# Downloading an image
def img_download(img_url):
	img_data = requests.get(img_url).content
	name = img_url.split('.com/', 1)[1].split('"', 1)[0]
	with open(str(name), 'wb') as handler:
		handler.write(img_data)

inp_count = int(input('Number of pages to parce: '))
scr_number = 0

for i in range (0, inp_count):
	try:
		img_download(get_img_url(url_gen()))
		scr_number += 1
		print('Screenshot saved:', name_gen(url_gen()))
	except requests.exceptions.MissingSchema:
		print(f'No screenshot found at {name_gen(url_gen())}')

print(f'Parced {scr_number} of {inp_count} screenshots ({(scr_number/inp_count)*100})%')