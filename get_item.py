import requests
import re
from bs4 import BeautifulSoup

from app import Design


for design in Design.select().where(Design.status == 0).limit(25):
	print design.name
	url = "https://www.threadless.com/product/%d" % design.design_id

	r = requests.get(url, verify=False)
	soup = BeautifulSoup(r.text, "html.parser")

	products = soup.find_all("div", { "class": "item_group" })


	found_product = False
	for product in products:
		title = product.find("h2")

		# if "Mens Tee" in title.text:
		if "Mens Tee" in title.text:

			price = title.find("span", { "class": "active_price" })
			print price.text

			design.price = float(price.text.replace("$", ""))
			# print title.text
			sizes = product.find_all("li")
			for size in sizes:
				
				if size.text.strip()[0:1] == "L":
					print "FOUND SIZE L"

					found_product = True
					if size.has_attr("class"):
						print "HASS CLASS"
						if 'disabled' in size.get("class"):
							print "not available!!!"
							design.status = -1
						else:
							design.status = 1
					else:
						print "available!!"
						design.status = 1
	if found_product == False:
		design.status = -2
	design.save()


