import requests
import re
from bs4 import BeautifulSoup
from app import Design, Product


Product.create_table(fail_silently=True)

for design in Design.select().where(Design.status == 0).limit(1800):
    print design.name

    if design.products.count() > 0:
        continue
    print design.design_id
    url = "https://www.threadless.com/product/%d" % design.design_id

    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")

    products = soup.find_all("div", { "class": "th-selectable-option" })

    for product in products:
        title = product.attrs['data-glname']

        sizes = product.find('div', { 'class': 'size-buttons' }).find_all('a')
        for size in sizes:
            product_dict = {}
            product_dict['name'] = title
            product_dict['size'] = size.attrs['data-gllabel']
            product_dict['price'] = size.attrs['data-glprice']
            product_dict['design'] = design

            print "%s - %s" % (title, product_dict['size'])

            Product.create(**product_dict)
