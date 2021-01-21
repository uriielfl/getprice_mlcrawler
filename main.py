import requests
from bs4 import BeautifulSoup
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from lxml.html import fromstring
import webbrowser
import mlcrawler
import sqlite3 
from colorama import Fore   
from colorama import Style
con = sqlite3.connect("productinfos.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS product_data(product_id INTEGER PRIMARY KEY, product_name TEXT, product_url TEXT, product_price REAL, product_good_price REAL)")
con.commit()

class FindPrice:
    def __init__(self, product_url, product_price, product_name):
        self.product_url = product_url 
        self.product_price = product_price
        self.product_name = product_name 

    def get_product_info(self):
        self.product_url = str(input('Digite a Url do produto:\n'))
        jurest = mlcrawler.Mutante(self.product_url)
        print(jurest.smartCrawler())          
        self.product_name, self.product_price = jurest.smartCrawler()     
        return self.product_price, self.product_name, self.product_url
    def check_product_info(self):
        url_check_list = []
        cur.execute("SELECT * FROM product_data")
        con.commit()
        games_promotions = []
        url_promotions = []
        for i in cur:            
            jurest_check = mlcrawler.Mutante(i[2])
            comparative_price = str(jurest_check.smartCrawler()[1]).replace('R$','').replace(',','.')
            if float(i[4]) > float(comparative_price):
                print("O produto {} entrou na promoção!!!!".format(i[1]))
                print("Você estava disposoto a pagar R${} e atualmente está custando R${}".format(i[4],comparative_price))
                games_promotions.append(i[1])
                url_promotions.append(i[2])
        count = 0
        for i in games_promotions:
            print(f"{Fore.RED} {count} {Style.RESET_ALL}- {games_promotions[count]} - {url_promotions[count]}")
            count+=1
        ask_open = int(input("Deseja abrir a paǵina de algum produto?\n1 - Sim\n2 - Não\nR:"))
        if ask_open == 1:
            index_ask_open = int(input("Digite o número relativo ao produto que você quer abrir no menu de cima:\n"))
            webbrowser.open(url_promotions[index_ask_open]) 
            
            pass
        elif ask_open == 2:
            print("Ok! Adeus!!!")
            exit()      
        return self.product_price, self.product_name, self.product_url

if __name__ == '__main__':
    loby_menu_options = int(input("Bem-vindo!\n1 - Buscar por preço\n2 - Checar Promoções\n0 - Sair\nR:"))
    save_data1 = []
    save_data2 = []

    if loby_menu_options == 1: 
        product_target = FindPrice('self','self', 'self')      

        for i in product_target.get_product_info():
                save_data1.append(str(i).replace('R$', '').replace('$','').replace(',','.'))
        ask_for_save = int(input("Deseja salva?\n1 - Sim\n2 - Não\nR:"))

        if ask_for_save == 1:
            product_goodprice = float(input("Que preço você está disposto a pagar?"))
            for i in save_data1:
                print(i)
            cur.execute("INSERT INTO product_data(product_name, product_url, product_price,product_good_price) VALUES (?,?,?,?)", (save_data1[1], save_data1[2], save_data1[0], product_goodprice)) 
            con.commit()

        elif ask_for_save == 2:
            print("Ok! Adeus!!!")
            exit()      

    elif loby_menu_options == 2:
        product_target = FindPrice('self', 'self', 'self')
        product_target.check_product_info()
    if loby_menu_options == 0:
        print("Ok! Adeus!!!")
        exit()      
   