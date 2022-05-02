from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Accept-Encoding': 'identity'
}
#'Accept-Encoding': 'identity'

url = 'https://www.realtor.com/realestateandhomes-search/San-Francisco_CA'

response=requests.get(url,headers=headers)

print(response)
