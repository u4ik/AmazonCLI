from pprint import pprint

import requests
from urllib import request
from bs4 import BeautifulSoup

# ? _________________________________
# * LOCAL HTML FILE PARSING
# ? _________________________________

# ? Opening the test.html file. "r" is passed as we want to read this file.
# ? The result is stored in 'file'.

with open('test.html', "r") as file:

    # ? Using BeautifulSoup to read the result, and parse it using a build in parser, and storing the results in 'doc'''
    doc = BeautifulSoup(file, "html.parser")

# ? Can use the doc class with dot notation to access any tag from the html document.
tag = doc.title

# ?To access the string that's contained within the tag. Which in this example would result in 'Document', the text between the title tag.'''

# print(tag.string)

# ? You can modify the string value within tags as well:
# tag.string = 'something else'
# print(tag)

# ? Using another method from doc class, you can also find tags, along with indexing to select a specific one. Looking for the first div tag

foundTags = doc.find_all('div')[0]

# ? Then you can find ANY nested tags, in this case, main is contained within the fist div.

# print(foundTags('main'))

# print(doc.prettify())

# ? _________________________________
# * REMOTE HTML FILE PARSING
# ? _________________________________
# ? _________________________________
# * Check the price of an item on Amazon
# ? _________________________________

singleItemUrl = 'https://www.amazon.com/Playstation-Console-Ultra-High-Bluetooth-Blu-ray/dp/B09KN38HFR/'

# Check for PS5 on amazon
multipleItemsUrl = 'https://www.amazon.com/s?k=ps5'

# result = requests.get(url)

def make_requests(url):
    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    req = requests.get(url, headers=req_headers)
    return req

def make_request(url):
    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    req = request.Request(str(url))
    for header in req_headers:
        req.add_header(header, req_headers[header])
    body = request.urlopen(req, None, 300).read().decode("utf-8")
    return body

# ? Using request module from urllib
# body = BeautifulSoup(make_requests(url).text, "html.parser")

# ? Using requests module
body = BeautifulSoup(make_requests(multipleItemsUrl).text, "html.parser")
title = body.title.string
# prices = body.find_all("span", class_="a-offscreen")
# priceWrap = body.find_all(class_="a-section a-spacing-none a-spacing-top-small")
priceWrap = body.find_all('a',class_="a-size-base a-link-normal a-text-normal")
# priceWrap = body.find_all(class_="a-price")

# print(priceWrap[0].findChildren("span", class_="a-offscreen", recursive=True))



prices= []
for i in range(len(priceWrap)):
    tmp1 =  priceWrap[i].findChildren("span", class_="a-price", attrs={"data-a-size" : "l", "data-a-color": "base"},recursive=True)
    for i in range(len(tmp1)):
        tmp2 = tmp1[i].findChildren("span", class_="a-offscreen", recursive=True)
        for i in range(len(tmp2)):

            prices.append(tmp2[i])
    # print(tmp2)


# for i in range(len(tmp1)):
    # print(tmp1[0].findChildren(""))
    # tmp2.append(tmp1[i].find("span", class_="a-price", recursive=True))

    # res = tmp[i].findChildren("span", class_="a-whole-price", recursive=True)
    # for i in res:
    #     prices.append(i.text)

    # p = res.text


# parent = prices[0].parent
descs = body.find_all("span", class_="a-size-medium a-color-base a-text-normal")

holder = {}

print(f'Prices: Amount {len(prices)}')
print(f'Desc: Amount {len(descs)}')

# print(prices)

# TODO Prices solved, now need to store the results
for i in range(len(descs)):
    holder[i] = {descs[i].string}
  
for i in range(len(prices)):
    # print(i,prices[i])
    if i <= len(holder) - 1:
        print(holder[i])
        print(prices[i].text)

# holder[i] = {"price": prices[i].string,**holder[i]}
# holder[i] = {"price": prices[i].string}

# pprint(holder)


