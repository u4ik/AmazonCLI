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

from urllib import request
import requests

url = 'https://www.amazon.com/Playstation-Console-Ultra-High-Bluetooth-Blu-ray/dp/B09KN38HFR/'
import pprint
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
body = BeautifulSoup(make_requests(url).text, "html.parser")
# print(body.prettify())
print(body.title)