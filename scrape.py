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
prices = body.find_all("span", class_="a-offscreen")
# prices = body.find_all("span", class_="a-price-whole")
descs = body.find_all("span", class_="a-size-medium a-color-base a-text-normal")

holder = {}

print(f'Prices: Amount {len(prices)}')
print(f'Desc: Amount {len(descs)}')


for i in range(len(descs)):
    # print(i,descs[i].string)
    holder[i] = {descs[i].string}
  
for i in range(len(prices)):

    if i <= len(holder) - 1:
        print(holder[i])
        print(prices[i].text)

# holder[i] = {"price": prices[i].string,**holder[i]}
# holder[i] = {"price": prices[i].string}

# pprint(holder)


