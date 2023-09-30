from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as urlreq

def openurl(page_url, page_num):
    page_url = page_url + "&page=" + str(page_num)
    uClient = urlreq(page_url) 
    page_html = uClient.read()
    uClient.close()
    return page_html

def get_pages_amount(page_url):
    page_bsoup = bsoup(openurl(page_url, 1),"html.parser")
    pages = page_bsoup.find("span",{"class":"list-tool-pagination-text"}).strong.text
    pages = pages.split("/")
    pages = int(pages[1])
    return pages

page_url = input("Enter NewEgg URL Search: ")
filename = input("Enter name for file: ")
print("Please wait while we create your file...")
f = open(filename + ".csv","w")
headers = "Product, Price\n"
f.write(headers)

pages = get_pages_amount(page_url)
for x in range(0,pages):
    page_url = page_url.replace("&page=" + str(x), "")
print(page_url)
for x in range(0,pages):
    page_bsoup = bsoup(openurl(page_url, x), "html.parser")
    products = page_bsoup.find_all("div",{"class":"item-container"})

    for product in products:
        product_name = product.a.img["title"].replace(",","|")
        product_price = product.find("div",{"class":"item-action"}).ul.find("li",{"class":"price-current"}).text.replace("–","")

        f.write(product_name + "," + product_price.replace(",","") + "\n")

f.close