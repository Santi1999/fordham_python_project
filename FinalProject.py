import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import datetime
import requests
import sys
import streamlit as st


class makedf:
    
    def __init__(self): #search):
        #self.search = search
        self.Df1Name = 'Ebay Table'
        self.Df2Name = 'Craigslist Table' # have these table names be included when the user utilizes a specific function

    #Create URL's   
    def ebay_url(search):
        q = '+'.join(search.split())
        return 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=' + q + '&_sacat=0'
    
    def craig_url(search):
        loc = location_list
        q2 = '+'.join(search.split())
        return 'https://'+ loc + '.craigslist.org/search/sss?query=' + q2 

        
    #Ebay DataFrame   
    def ebdf(query_url):
        try:
            item_name = []
            prices = []
            condition = []
            url = query_url
            r = requests.get(url)
            data= r.text
            soup = BeautifulSoup(data)
            listings = soup.find_all('li', {'class':'s-item'})
            
            #append the lists
            for listing in listings:
                prod_name = ' '
                prod_price = ' '
                for name in listing.find_all('h3', {'class': 's-item__title'}):
                    if(str(name.find(text = True, recursive = False)) != 'None'):
                        prod_name = str(name.find(text = True, recursive = False))
                        item_name.append(prod_name)
                if(prod_name!=" "):
                    price = listing.find('span', attrs={'class':"s-item__price"})
                    prod_price = str(price.find(text=True, recursive=False))
                    prices.append(prod_price)
                    conditions = listing.find('span', attrs ={'class':"SECONDARY_INFO"})
                    condition.append(conditions) 
                    

            #create dataframes
            df = pd.DataFrame({"Item Listing":item_name, "Price":prices, "Condition":condition})
            df.drop(labels=0, axis=0, inplace=False)
            df['Price'] = [x.strip('$') for x in df['Price']]
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            return df
        except Exception as e:
            print(e)

    #Craigslist DataFrame
    def cldf(query_url):
        try:
            url = query_url
            response = requests.get(url)
            data = response.content
            soup = BeautifulSoup(data, 'html.parser')
            search_results = []
            total_results = int(soup.find('span', 'totalcount').text)
            results = soup.find('ul', {'id': 'search-results'})
            result_rows = results.find_all('li', 'result-row')
            for result_row in result_rows:
                post_date = result_row.time['datetime']
                post_id = result_row.h3.a['data-id']
                price = result_row.find('span', 'result-price')
                title = result_row.h3.a.text
                search_results.append([post_date,post_id, price, title])
            columns = ('Post Date','PostID', 'Price', 'Title')
            df = pd.DataFrame(search_results, columns = columns)
            return df
        except Exception as e:
            print(e)

st.set_page_config(layout = 'wide')
st.header("Product Comparison Ebay & Craigslist")
#code for generation of locations
testurl = 'https://annapolis.craigslist.org/search/pta?'
r = requests.get(testurl)
data= r.text
soup = BeautifulSoup(data)
option = soup.find("select",{"class":"js-only"}).findAll("option")
values = [item.get('value') for item in option]
textValues = [item.text for item in option]
tvNoSpaces = []
for i in textValues:
    j = i.replace(' ', '').replace(',', '').replace('PA', '').replace('NJ', '').replace('VA', '').replace('MD', '').replace('DC', '')
    tvNoSpaces.append(j)




#dropdown code
location_list= st.selectbox('Select a location', tvNoSpaces)
st.write('You selected:', location_list)


def getSearch():
    search_str = st.text_input('What would you like to search for:', key='search_input_field')
    try: 
        search = str(search_str)
    except:
        search = None
    url = makedf.ebay_url(search)
    url1 = makedf.craig_url(search)
    return url, url1
def displayResults(url, url1):
    if url == None or url1 == None:
        return 
    df1 = makedf.ebdf(url)
    df2 =makedf.cldf(url1)
    pd.set_option('display.max_rows', None)

    return st.subheader('Ebay Data'), st.text(df1), st.subheader('Craigslist Data'), st.text(df2)

st.header("Price Comparison")
url, url1 = getSearch()


displayResults(url, url1)


