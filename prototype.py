import pandas as pd
from bs4 import BeautifulSoup
import datetime
import requests
import sys
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
from sqlalchemy import create_engine



class makedf:
    
    def __init__(self, search):
        self.search = search
        self.Df1Name = 'Ebay Table'
        self.Df2Name = 'Craigslist Table' # have these table names be included when the user utilizes a specific function
        
    def ebay_url(self):
        q = '+'.join(self.search.split())
        return 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=' + q + '&_sacat=0'
    
    def craig_url(self):
        q2 = '+'.join(self.search.split())
        return 'https://hudsonvalley.craigslist.org/search/sss?query=' + q2 #are we going with a gui or just focusing on the database
        # Can Tkninter function do in this function? Change the first part of the url?
    def ebdf(query_url):

        item_name = []
        prices = []
        condition = []
        # add try and except conditions to code
        url = query_url
        r = requests.get(url)
        data= r.text
        soup = BeautifulSoup(data)
        listings = soup.find_all('li', {'class':'s-item'})
        #print(listings)

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
                conditions = listing.find('span', attrs ={'class':"SECONDARY_INFO"}).text
                condition.append(conditions) 
                # add code for scraping popularity data '# of watchers or how often the item was bought or how many are left'
        

        df = pd.DataFrame({"Item Listing":item_name, "Price":prices, "Condition":condition})
        df.drop(labels=0, axis=0, inplace=False)
        df['Price'] = [x.strip('$') for x in df['Price']]
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        return df
    

    def cldf(query_url): #check if the code needs to make sure to not repeat the code (requests code)
        try:
            url = query_url
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            search_results = []
            total_results = int(soup.find('span', 'totalcount').text)
#             print(total_results)
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
            
        except Exception as e:
            print(e)
        
        return df
        
    def conn_database(dataframe):

        conn = psycopg2.connect(database='wyarrbvx', 
        user='wyarrbvx',
        password = 'I11YTcTmXMb9FKyi-eg-yhK-7Dm7htLl',
        host = 'rajje.db.elephantsql.com',
        port = '5432')
      
        cursor = conn.cursor()

        engine = create_engine('postgres://wyarrbvx:I11YTcTmXMb9FKyi-eg-yhK-7Dm7htLl@rajje.db.elephantsql.com/wyarrbvx',
             pool_size=20, max_overflow=10)

        dataframe.to_sql('ebay_table', engine, if_exists = 'replace', index=False)
        # Make sure to have the name of the table change based on which function they use if possible
        sqll = '''SELECT * FROM ebay_table;'''
        cursor.execute(sqll)
        
        for i in cursor.fetchall():
            print(i)
        # makedf.cldf(url1).to_sql('self.Df2Name', engine, if_exists = 'replace', index=False)
        conn.close()
        print('\n Dataframe successfully uploaded to remote database') 
        #final report have atleast one diagram and what it is
        
    # add a statistics function that performs three different con

    # add a Tkinter functions that allows the user to pick a location based on the drop down menu.
    
search_input = str(input('What would you like to search for: '))
search = makedf(search_input)




# 