from bs4 import BeautifulSoup
from os import write
from pprint import pprint
import requests
import re


def start():
    q = input("Search Amazon For: ")
    m_p = input("Min Price: ")
    mx_p = input("Max Price: ")
    s_url = f'https://www.amazon.com/s?k={q}&rh=p_36%3A{m_p}00-{mx_p}00'
    resp = request(s_url)
    res = parse(resp)
    pprint(f'{len(res)} Results')
    pprint(res)
    write(str(res))

def request(url):

    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    response = requests.get(url, headers=req_headers).text
    return response

def parse(res):
    t = 'div'
    c_d = {}
    c = 0
    b = BeautifulSoup(res, "html.parser")
    p_w = b.findChildren(
        'div', class_='s-main-slot s-result-list s-search-results sg-row')
    for p in p_w:
        f_c = p.findChildren(t, class_='s-result-item',attrs={"data-index": True, "data-asin": True}, recursive=True)
        for l in f_c[1:-2]:
            r = l.findChildren(t, class_="sg-col-inner")
            try:
                x = r[2].findChildren('span', class_="a-offscreen")
                for i in x[0]:
                    c_d[c] = {'Desc:': l.h2.text}
                    c_d[c]['Price:'] = i.string
                    c += 1
            except (NameError, AttributeError, IndexError) as e:
                continue
    return c_d

def write(f):
    with open('results.json', "w", encoding='utf-8') as fl:
        fl.write(f)


start()
