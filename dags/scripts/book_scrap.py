import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import numpy as np


def scrap_info():
    i=1
    url = "http://books.toscrape.com/index.html"
    while(i<=10):
        response = requests.get(url)
        html = response.content
        scraped = BeautifulSoup(html, 'html.parser')
        title_text = scraped.title.text.strip()
        print(title_text)
        table_data=[]
        articles = scraped.select(".product_pod")
        for article in articles:
            title = article.h3.a["title"]
            price = article.find("p", class_="price_color")
            availibility=article.find("p",class_="instock availability").get_text().strip()
            image=article.img["src"]
            price_float = float(price.text.lstrip("£"))
            currency=price.string[0]
            data_item={"title":title,"price":price_float,"currency":currency,"availibility":availibility,"book_cover":image}
            table_data.append(data_item)


        df = pd.DataFrame(table_data)
        df = df.reset_index()
        df = df.rename(columns={"index":"book_id"})
        username = "store"
        password = "store" 
        ipaddress = "db"
        port = 3306
        dbname = "books" 
        mysql_str = f'mysql://{username}:{password}@{ipaddress}:{port}/{dbname}'
        cnx = create_engine(mysql_str)
        max_id=pd.read_sql('SELECT max(book_id) as ID FROM book', cnx).values
        print(max_id.item())
        if (max_id.item()):
            df["book_id"]=df["book_id"]+max_id.item()+1

        df.to_sql("book", con=cnx, index=False, if_exists="append")
        i=i+1
        url="http://books.toscrape.com/catalogue/page-"+str(i)+".html"
        