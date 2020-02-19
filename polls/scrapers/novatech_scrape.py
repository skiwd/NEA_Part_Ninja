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
    f = open('novatech.html', 'w')
    f.write(webcontent)
    f.close()

    with open('novatech.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    dic = {'type': None, 'brand': None, 'name': None, 'price': None, 'site': None,
           'pub_date': date.today().strftime("%d-%m-%Y")}

    names = []
    for a in soup.find_all(class_="search-box-liner search-box-results search-hover"):
        b = a.find('h2')
        c = b.find('a')
        names.append(c.text)

    prices = []
    for x in soup.find_all(class_="search-box-liner search-box-results search-hover"):
        for a in x.find_all('p', class_="newspec-price-listing"):
            a = a.text.strip('£')
            a = a.strip(' inc vat')
            prices.append(a)

    sites = []
    for a in soup.find_all(class_="search-box-liner search-box-results search-hover"):
        b = a.find('h2')
        c = b.find('a')
        d = c['href']
        d = 'https://novatech.co.uk' + d.strip('\ ').strip("'")
        sites.append(d)

    brands = []
    for a in soup.find_all(class_="search-box-liner search-box-results search-hover"):
        b = a.find('h2').text
        c = b.split(' ')[0]
        if c == '*B-stock':
            if not b.split(' ')[3].isdigit():
                c = b.split(' ')[3].strip('warranty*')
            else:
                c = b.split(' ')[5].strip('warranty*')
        elif c[0].isdigit():
            c = 'intel'
        d = ""
        if '.' in c:
            for i in c:
                if i.isalpha():
                    d = "".join([d, i])
            c = d
        brands.append(c.lower().strip('.').title())

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
    # graphics
    pageno = 1
    repeat = True
    test = []
    while repeat:
        try:
            url = f'https://www.novatech.co.uk/products/components/memory-pc/ddr4memory/?pg={pageno}'
            dic, repeat = tool(url)
            if not dic['name'] == []:
                test.append(dic)
                print(dic)
            pageno += 1
        except:
            print("page not found")
            repeat = False
    print(test)
