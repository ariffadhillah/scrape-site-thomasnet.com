import requests
from bs4 import BeautifulSoup
import csv

baseurl = 'https://www.stanceplus.com'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48'
}

r = requests.get('https://www.stanceplus.com')
soup = BeautifulSoup(r.content, 'lxml')

categorylinks  = []
categorylist = soup.find_all('ul', class_='col-6 col-md-3 col-lg-2')

for itemcategorylist in categorylist:
    for linkcategory in itemcategorylist.find_all('a', href=True):
        categorylinks.append(baseurl + linkcategory['href'])

productURLList = []
data = []

for linkcategory in categorylinks:
    r = requests.get(linkcategory, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    productList = []
    productItem = soup.find_all('div', class_='panel-collapse collapse')
    for item in productItem:
        for href in item.find_all('a', class_='', href=True ):
            productList.append(baseurl + href['href'])

    for link in productList:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')

        productTitle = soup.find('h1', class_='item-title').text.strip()

        try:
            productSubtitle = soup.find('h2', class_='item-title').text.strip()
        except:
            productSubtitle = ''
        try:
            price = soup.find('div', class_='item-price').text.strip()
        except:
            price = ''
        

        StancedUk = {
            'Category (Parent)': linkcategory.split('/')[-1].replace('-', ' ').title(),
            'Category URL (Parent)': linkcategory,
            'Category - Leaf (Child 1)': '',
            'Category URL - Leaf (Child 1)': '',
            'Product URL': link,
            'PartNumber': '',
            'Product Title': productTitle, 
            'Product Subtitle': productSubtitle,
            'Product Description': '',
            'Image URLs': '',
            'Price': price,
            'List of Vehicle Compatibility': '',
            'Brand': '',
            'OE number / cross-reference': ''
        }

        data.append(StancedUk)
        print(StancedUk)

fields = ['Category (Parent)', 'Category URL (Parent)', 'Category - Leaf (Child 1)', 'Category URL - Leaf (Child 1)', 'Product URL', 'PartNumber', 'Product Title', 'Product Subtitle', 'Product Description', 'Image URLs', 'Price', 'List of Vehicle Compatibility', 'Brand', 'OE number / cross-reference']

filename = 'Stanced Uk.csv'

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for item in data:
        writer.writerow(item)

print('data is successfully saved in the file CSV', filename)