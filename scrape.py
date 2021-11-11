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
    q = input("Search Amazon For: ")
    # q = 'ps5'
    s_url = f'https://www.amazon.com/s?k={q}'
    res = request(s_url)
    # write(str(parse(res)))
    parse(res)

def request(url):
    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    response = requests.get(url, headers=req_headers).text

    return response

def parse(res):
    c_d = {}
    b = BeautifulSoup(res, "html.parser")
    # old
    pWrap = b.find_all(
        'a', class_="a-size-base a-link-normal a-text-normal")


# testing
    # pWrap = b.findChildren('div', class_='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16')

    # print(pWrap.encode("utf-8"))
    # write(str(pWrap))
    '''Write the results'''
    p = []

    for i in range(len(pWrap)):
        tmp1 = pWrap[i].findChildren(
            "span", class_="a-price", attrs={"data-a-size": "l", "data-a-color": "base"}, recursive=True)
        for k in range(len(tmp1)):
            tmp2 = tmp1[k].findChildren(
                "span", class_="a-offscreen", recursive=True)
            for j in range(len(tmp2)):
                p.append(tmp2[j])

    descs = b.find_all(
        "span", class_="a-size-medium a-color-base a-text-normal")

    # print(f'Prices: Amount {len(p)}')
    # print(f'Desc: Amount {len(descs)}')

    for i in range(len(descs)):
        c_d[i] = {'Desc':descs[i].string}
    for i in range(len(p)):
        # print(i,p[i])
        if i <= len(c_d) - 1:
            c_d[i]['Price'] = p[i].text 
            # print(c_d[i])
            # print(p[i].text)
            # print('')
    pprint(f'Results: {len(c_d)}')
    # pprint(c_d)
    return c_d

def write(f):
    with open('results.html', "w") as file:
        file.write(f)
start()

