from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import date


def tool(url):
    repeat = True
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = Request(url=url, headers=hdr)

    # Fetching URL source code
    response = urlopen(req)
    webcontent = response.read()
    webcontent = str(webcontent)

    # Writing source code to text file
    f = open('ebuyer.html', 'w')
    f.write(webcontent)
    f.close()

    with open('ebuyer.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        # print(soup)

    dic = {'type': None, 'brand': None, 'name': None, 'price': None, 'site': None,
           'pub_date': date.today().strftime("%d-%m-%Y")}
    names = []
    for a in soup.find_all(class_='grid-item js-listing-product'):
        name = a.find(class_='grid-item__title').text
        name = name[32:-24]
        names.append(name)

    prices = []
    for a in soup.find_all(class_='grid-item js-listing-product'):
        try:
            price = a.find(class_='price').text
            price = ''.join([letter for letter in price if letter.isdigit() or letter == '.'])[:-1]
            prices.append(price)
        except:
            prices.append(None)

    sites = []
    for a in soup.find_all(class_='grid-item js-listing-product'):
        name = a.find(class_='grid-item__title')
        name = name.find('a')
        site = 'https://www.ebuyer.com/' + name['href']
        sites.append(site)

    brands = []
    for a in soup.find_all(class_='grid-item js-listing-product'):
        name = a.find(class_='grid-item__title').text
        name = name[32:-24]
        brand = name.split(' ')
        if len(brand[0]) != 1:
            brand = brand[0]
        else:
            brand = brand[0] + brand[1]
        brands.append(brand.lower().strip('.').title())

    typ = None
    try:
        name1 = names[0].lower()
        if 'graphics card' in name1:
            typ = 'graphics card'
        elif 'processor' in name1 or 'cpu' in name1:
            typ = 'processor'
        elif 'memory' in name1 or 'ram' in name1 or 'ddr' in name1:
            typ = 'memory'
    except IndexError:
        pass

    dic['name'] = names
    if not names:
        repeat = False
    dic['price'] = prices
    dic['site'] = sites
    dic['brand'] = brands
    dic['type'] = typ
    return dic, repeat


if __name__ == '__main__':
    # Nvidia Cards
    pageno = 1
    repeat = True
    test = []
    while repeat:
        try:
            url = f'https://www.ebuyer.com/store/Components/cat/Memory---PC?page={pageno}'
            dic, repeat = tool(url)
            if not dic['name'] == []:
                test.append(dic)
                print(dic)
            pageno += 1
        except:
            print('page not found')
            repeat = False
