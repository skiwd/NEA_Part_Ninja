from bs4 import BeautifulSoup
import urllib.request as ur
from datetime import date


def tool(url):
	# Program iterates until there are no more names on the page
	repeat = True

	# Fetching URL source code
	response = ur.urlopen(url)
	webcontent = response.read()
	webcontent = str(webcontent)

	# Writing source code to text file
	f = open('overclockers.html', 'w')
	f.write(webcontent)
	f.close()

	with open('overclockers.html') as html_file:
		soup = BeautifulSoup(html_file, 'lxml')
	# print(soup)

	# Creating dictionary to be later put in database
	dic = {'type': None, 'brand': None, 'name': None, 'price': None, 'site': None,
		   'pub_date': date.today().strftime("%d-%m-%Y")}
	names = []  # Sets up the names for each product
	for a in soup.find_all(class_="producttitles"):
		for b in a.find(class_="ProductTitle"):
			b = b[2:]
			b = b[:-2]
			names.append(b)

	dic['name'] = names
	if not names:
		repeat = False

	prices = []  # Sets up the prices for each product
	for a in soup.find_all("span", class_="price"):
		tempstr = ''
		tempstr += a.text.strip('£')
		prices.append(tempstr)

	dic['price'] = prices

	sites = []
	for a in soup.find_all(class_="producttitles"):
		sites.append(a['href'])

	dic['site'] = sites

	brands = []
	for a in soup.find_all(class_="ProductSubTitle"):
		a = a.text
		a = a[2:]
		a = a[:-2]
		brands.append(a.lower().strip('.').title())

	# Takes the url and splits it into a list, then takes the last part,
	#       minus the last 4 characters
	# dic['brand'] = (((url.split('/'))[-1])[:-4]).strip('?')
	dic['brand'] = brands
	typ = ((url.split('/'))[-2]).replace('-', ' ')
	if typ[-1:] == 's':
		typ = typ[:-1]
	dic['type'] = typ
	return dic, repeat


if __name__ == '__main__':
	# Nvidia Cards
	pageno = 1
	repeat = True
	ncards = []
	while repeat:
		try:
			url = f'https://www.overclockers.co.uk/pc-components/graphics-cards/nvidia?p={pageno}'
			dic, repeat = tool(url)
			if not dic['name'] == []:
				ncards.append(dic)
				print(dic)
			pageno += 1
		except:
			print("page not found")
			repeat = False

	# AMD Cards
	pageno = 1
	repeat = True
	acards = []
	while repeat:
		try:
			url = f'https://www.overclockers.co.uk/pc-components/graphics-cards/amd?p={pageno}'
			dic, repeat = tool(url)
			if not dic['name'] == []:
				acards.append(dic)
				print(dic)
			pageno += 1
		except:
			print("page not found")
			break
	print(ncards)
	print(acards)
