import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://books.toscrape.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

productlinks = []
t={}
data=[]
c=0

for x in range (1, 2):
    k = requests.get("https://books.toscrape.com/".format(x)).text
    soup = BeautifulSoup(k, "html.parser")
    productlist = soup.find_all("div",{"class":"image_container"})


    for product in productlist:
        link = product.find("a").get("href")
        productlinks.append(baseurl + link)

data = []
for link in productlinks:
    f = requests.get(link, headers=headers).text
    hun = BeautifulSoup(f, "html.parser")

    try:
        price = hun.find("p",{"class":"price_color"}).text.replace('\n',"")
    except:
        price = None

    try:
        about = hun.find("p",{"class":"sub-header"}).text.replace('\n',"")
    except:
        about = None

    try:
        rating = hun.find("p",{"class":"star-rating three"}).text.replace('\n',"")
    except:
        rating = None

    try:
        name = hun.find("div",{"class":"col-sm-6 product_main"}).text.replace('\n',"")
    except:
        name = None

    try:
        availability = hun.find("p",{"class":"instock availability"}).text.replace('\n',"")
    except:
        availability = None


    books = {"name": name, "price": price, "rating": rating, "about": about, "availability": availability}

    data.append(books)
    c =c+1
    print ('completed', c)

df = pd.DataFrame(data)
df.to_csv('Books.csv', index=False, encoding='utf-8')



