import glob, os, re, tarfile
import pandas as pd
import numpy as np
from datetime import date
from decimal import *

# Opens tar files from scratch/group/kbnk_group/projects/etsy_scraping. The commented line using today only works if this file is run on the same date that catagoryScrapper.py was run on, otherwise a hardcoded value is used.

today=date.today().strftime('%Y-%m-%d')
#data_files = glob.glob('/scratch/group/kbnk_group/projects/etsy_scraping/runs/{}/*'.format(today))
data_files = glob.glob('/PATH/TO/DIR/*')

# Sorts raw html into a dictionary dataDict, and then into the pandas dataframe html_df.

dataDict={}

def load_files(filenames):
# Takes a list of filenames, and returns a filled dictinary consisting of filepath:extractedHTML
    for filename in filenames:
        try:
            with tarfile.open(filename, mode='r:xz') as currFile:
                html = currFile.extractfile(currFile.next())
                dataDict[filename]=html.read()
        except:
            dataDict[filename]='error'
        
load_files(data_files)

html_df = pd.DataFrame.from_dict(dataDict, orient='index', columns=['HTML'])
html_df.reset_index(level=0,inplace=True)
html_df.rename(columns={'index':'Filename'}, inplace=True)

def get_etsy_details(html):
# Searches the html for tags, then inputs them into a dictionary that is put into a column of html_df. Rating and price are stored both as a string (no suffix) and a decimal (suffix 1) due to rounding errors when casting to a float.
    tt = {}
    try:
        tt['seller_name'] = str(re.search(b'data-to_user_display_name="(.+?)"', html).group(1)).lstrip('b\'').rstrip('\'')
    except:
        pass
    try:
        tt['shop_name'] = str(re.search(b'"brand": "(.+?)"', html).group(1)).lstrip('b\'').rstrip('\'')
    except:
        pass       
    try:
        tt['shop_url'] = str(re.search(b'href="(.+?)">\n', html).group(1)).lstrip('b\'').rstrip('\'')
    except:
        pass
    try:
        tt['description'] = str(re.search(b'"description": "(.+?)",\n', html).group(1)).lstrip('b\'').rstrip('\'').replace('\\\\n','').replace('\\\\u','').replace('2764fe0f','').replace('&#39;','')
    except:
        pass
    try:
        tt['rating1'] = Decimal(str(re.search(b'ratingValue": (.+?),\n', html).group(1)).lstrip('b\'').rstrip('\''))
    except:
        pass
    try:
        tt['rating'] = str(re.search(b'ratingValue": (.+?),\n', html).group(1)).lstrip('b\'').rstrip('\'')
    except:
        pass
    try:
        tt['price'] = str(re.search(b'product:price:amount" content="(.+?)"', html).group(1)).lstrip('b\'').rstrip('\'')
    except:
        pass
    try:
        tt['price1'] = Decimal(str(re.search(b'product:price:amount" content="(.+?)"', html).group(1)).lstrip('b\'').rstrip('\''))
    except:
        pass
    return tt

html_df['Tags']=html_df['HTML'].apply(lambda x: get_etsy_details(x))

# Returns the html_df as a csv.

html_df.to_csv("/PATH/TO/DIR/scrapedEtsyPages.csv", index=False)
