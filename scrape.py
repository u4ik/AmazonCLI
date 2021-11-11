from os import write
from pprint import pprint
import requests
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

# singleItemUrl = 'https://www.amazon.com/Playstation-Console-Ultra-High-Bluetooth-Blu-ray/dp/B09KN38HFR/'


def start():
    # q = input("Search Amazon For:")
    q = 'ps5'
    s_url = f'https://www.amazon.com/s?k={q}'
    res = request(s_url)
    # write(str(parse(res)))
    parse(res)


def request(url):



    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    response = requests.get(url, headers=req_headers)
    return response
def parse(res):

    c_d={}
    body = BeautifulSoup(res.text, "html.parser")
    priceWrap = body.find_all(
        'a', class_="a-size-base a-link-normal a-text-normal")

    print(priceWrap)
    # write(str(priceWrap))
    prices = []
    for i in range(len(priceWrap)):
        tmp1 = priceWrap[i].findChildren(
            "span", class_="a-price", attrs={"data-a-size": "l", "data-a-color": "base"}, recursive=True)
        for i in range(len(tmp1)):
            tmp2 = tmp1[i].findChildren(
                "span", class_="a-offscreen", recursive=True)
            for i in range(len(tmp2)):
                prices.append(tmp2[i])

      

        descs = body.find_all(
            "span", class_="a-size-medium a-color-base a-text-normal")

        print(f'Prices: Amount {len(prices)}')
        print(f'Desc: Amount {len(descs)}')
        print(prices)

        for i in range(len(descs)):
            c_d[i] = {descs[i].string}

        for i in range(len(prices)):
            # print(i,prices[i])
            if i <= len(c_d) - 1:
                # print(c_d[i])
                print(prices[i].text)

    return c_d
def write(f):
    with open('ps5-amazon.html', "w") as file:
        file.write(f)


start()