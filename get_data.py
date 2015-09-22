import requests
import re
from bs4 import BeautifulSoup

from app import Design

from peewee import DoesNotExist


for i in range(1,15,1):
  print i
  url = 'https://www.threadless.com/catalog/view,48/order,popular/page,%d' % i

  r = requests.get(url, verify=False)
  soup = BeautifulSoup(r.text, "html.parser")
  product_catalog = soup.find(id="catalog_products")

  for product in product_catalog.findAll("dd", {"class":"product_item"}):
    link = product.find("dd").find("a")["href"]
    product_id = int(re.search(r"/(\d+)/", link).group(1))
    name = product.find("dd").find("a").text.strip()
    image_url = product.find("img")["src"].strip()

    print name


    try:
      d = Design.get(design_id=product_id)
    except DoesNotExist:
      d = Design.create(name=name, design_id=product_id, image_url=image_url)
      d.save()
    else:
      print "Design already in DB!"