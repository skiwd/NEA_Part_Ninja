import sqlite3
from scrapers.overclockers_scrape_gpu import tool as overclockers  # overclockers web scrape script
from scrapers.novatech_scrape import tool as novatech  # novatech web scrape script
from scrapers.ebuyer_scrape import tool as ebuyer     # ebuyer web scrape script
from scrapers.awdit_scrape import tool as awdit       # awd-it web scrape script


def conf(values):
    conn = sqlite3.connect('../db.sqlite3')
    c = conn.cursor()
    for l in values:
        c.execute(f'''
        INSERT INTO "main".polls_product (type, brand, name, price, site, pub_date) 
        VALUES ('{l[0]}', '{l[1]}', '{l[2]}', '{l[3]}', '{l[4]}', '{l[5]}');
        ''')  # Iterates, adding the new fields into the product table
        conn.commit()


class Data:
    def __init__(self):
        self._products = []

    @staticmethod
    def clear():
        conn = sqlite3.connect('../db.sqlite3')
        c = conn.cursor()
        c.execute('''
        DELETE FROM "main".polls_product;''')
        print('Cleared table')  # CLEARS EVERYTHING FROM THE PRODUCT TABLE
        conn.commit()

    @staticmethod
    def filter():
        conn = sqlite3.connect('../db.sqlite3')
        c = conn.cursor()
        c.execute('''
                 DELETE FROM "main".polls_product WHERE "main"."polls_product".price = 'None';''')
        print('Filtered table')  # CLEARS PRICES WHICH HAVE VALUE OF NONE
        conn.commit()

    def scrape(self, sites):
        for site in sites:
            pageno = 1
            repeat = True
            if 'overclockers' in site:  # Every site has a different script to scrape it, imported at top
                while repeat:
                    try:
                        url = f'{site}{pageno}'
                        dic, repeat = overclockers(url)  # Uses the script imported for overclockers.co.uk
                        if not dic['name'] == []:  # Does not add empty rows to the table
                            self._products.append(dic)
                        pageno += 1
                    except:
                        print("page not found")
                        repeat = False
                print('Scraped overclockers')
            if 'novatech' in site:
                while repeat:
                    url = f'{site}{pageno}'
                    dic, repeat = novatech(url)  # Uses the script imported for novatech.co.uk
                    if not dic['name'] == []:  # Does not add empty rows to the table
                        self._products.append(dic)
                    pageno += 1
                print('Scraped novatech')
            if 'ebuyer' in site:
                while repeat:
                    url = f'{site}{pageno}'
                    dic, repeat = ebuyer(url)  # Uses the script imported for ebuyer.com
                    if not dic['name'] == []:  # Does not add empty rows to the table
                        self._products.append(dic)
                    pageno += 1
                print('Scraped ebuyer')
            if 'awd-it' in site:
                while repeat:
                    url = site.replace('%PAGENO%', str(pageno))
                    dic, repeat = awdit(url)  # Uses the script imported for awd-it.co.uk
                    try:
                        if not dic['name'] == []:  # Does not add empty rows to the table
                            self._products.append(dic)
                    except TypeError:
                        pass
                    pageno += 1
                print('Scraped awd-it')

    def populate(self):
        for prod_dict in self._products:
            prod_list = []  # 'prod_list' is the overall list for all the products currently being added
            for i in range(len(prod_dict['name'])):  # Because 'brand', 'name', 'price' and 'site' are lists, everything
                prod = [prod_dict['type']]  # else has to be duplicated the amount of times for the length of the list
                try:
                    prod.append((prod_dict['brand'])[i])
                except:
                    prod.append(None)
                try:
                    prod.append((prod_dict['name'])[i])
                except:
                    prod.append(None)
                try:
                    prod.append((prod_dict['price'])[i])
                except:
                    prod.append(None)  # In the case that there is a missing price, the program isn't halted
                try:
                    prod.append((prod_dict['site'])[i])
                except:
                    prod.append(None)
                # print(prod)
                # print(prod_list)
                prod.append(prod_dict['pub_date'])  # Has to append the list in a certain order to go into the database more simply
                prod_list.append(prod)  # Creates a list of lists
            conf(prod_list)
        print('Populated table')


if __name__ == '__main__':
    d = Data()
    with open('scrapers/scrape_sites.txt', 'r') as f:
        sites = [line.strip('\n') for line in f.readlines()]
    print(f'Sites being scraped:{sites}')
    d.scrape(sites)
    d.clear()
    d.populate()
    d.filter()
