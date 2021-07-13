from playwright.sync_api import sync_playwright
import re
from csv import reader

def readCsv(csv):
# Takes the csv of catagory urls and returns a list of all the etsy pages.
    pageList=[]
    with open(csv,'r') as openCsv:
        readCsv=reader(openCsv)
        for row in readCsv:
            if row[0]=='etsy':
                pageList.append(row[4])
    return pageList

def getCatagoryContent(site):
# Uses playwright to open up the catagory page and return the list of urls of the items on the page.
    with sync_playwright() as p:
        browser=p.firefox.launch()
        page=browser.new_page()
        page.goto(site)
        listings=page.query_selector_all('li:has(div.js-merch-stash-check-listing)')
        urlList=[]
        for i in range(len(listings)):
            listingId=listings[i].inner_html()
            urlList.append(re.search('href="(.+?)"',listingId).group(1))
        page.close()
        browser.close()
        return urlList

if __name__ == "__main__":
    pageList=readCsv('site_urls.csv')
    for i in range(len(pageList)):
        pageList1=[]
        # Change the second range number to change how many pages per catagory are scrapped.
        for j in range(1,10):
            pageList1.append(pageList[i]+'?explicit=1&ref=pagination&page={}'.format(i))
        urlList=[]
        for el in pageList1:
            urlList.append(getCatagoryContent(el))
        with open('/PATH/TO/DIR/{}.txt'.format(i),'w') as text:
            #text.writelines(['%s\n' % item for item in urlList[i]])
            text.writelines(['%s\n' % item for item in urlList])

