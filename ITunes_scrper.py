from lxml import html
import requests
import re
import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import time

main_url = "https://itunes.apple.com/us/app/blocker-by-afternow/id1256222832"


#The Scraper Part.
def parse(url):
    #The Google gspread part
    json_key = json.load(open('creds.json'))
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds
    gc = gspread.authorize(credentials) 
    sheet = gc.open("ARKit Titles") 
    import_sheet = sheet.worksheet('Import')
    #all_cells = import_sheet.range('A1:A5')
    all_cells2 = len(import_sheet.col_values(1))
    all_cells = import_sheet.range('A3:A{}'.format(all_cells2))
    for cells in range(len(all_cells)):
        r = requests.get(all_cells[cells].value)
        h = html.fromstring(r.text)
        #title = h.xpath('//h1[@class="product-header__title product-header__title--app-header"]/text()')
        category = h.xpath('//div[@class="information-list__item l-row"]/dd/a/text()')
        category_bis = re.findall('"applicationCategory":"(.+?)"',r.text)
        if category:
            category = category
        else:
            category= category_bis
        
        #print('p ', category)
        publisher = h.xpath('//h2[@class="product-header__identity product-header__identity--app-header product-header__identity--spaced"]/a/text()')
        #print 'p',publisher
        rating = h.xpath('//figcaption[@class="we-rating-count star-rating__count"]/text()')
        star_rating = "".join(rating).split(',')[0]
        #print "s", star_rating
        of_rating = "".join(rating).split(',')[-1]
        #print 'o',of_rating
        reviews = "".join(h.xpath('//div[@class="we-clamp we-clamp--lines-6 ember-view"]/span/text()'))
        version = "".join(h.xpath('//p[@class="l-column small-6 medium-12 whats-new__latest__version"]/text()'))
        time.sleep(10)
        import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+1, "".join(category))
        time.sleep(2)
        import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+2, "".join(publisher))
        time.sleep(2)
        #import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+3, "".join(rating))
        import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+3, "".join(star_rating))
        time.sleep(2)
        import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+4, "".join(of_rating))
        time.sleep(2)
        import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+5, "".join(version))
        time.sleep(2)
        import_sheet.update_cell(all_cells[cells].row,all_cells[cells].col+6, "".join(reviews))
        print('updating done!')
        
parse(main_url)
print('work finished!')
    
