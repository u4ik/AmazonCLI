from os import write
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def start():
    q = input("Search Amazon For: ")
    # q = 'ps5'
    s_url = f'https://www.amazon.com/s?k={q}'
    res = request(s_url)
    # write(str(parse(res)))
    result = parse(res)
    pprint(f'Results: {len(result)}')
    pprint(result)

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
    p_wrap = b.find_all(
        'a', class_="a-size-base a-link-normal a-text-normal")

# testing
    # p_wrap = b.findChildren('div', class_='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16')

    # print(p_wrap.encode("utf-8"))
    write(str(p_wrap))
    p = []

    for i in range(len(p_wrap)):
        tmp1 = p_wrap[i].findChildren(
            "span", class_="a-price", attrs={"data-a-size": "l", "data-a-color": "base"}, recursive=True)
        for k in range(len(tmp1)):
            tmp2 = tmp1[k].findChildren(
                "span", class_="a-offscreen", recursive=True)
            for j in range(len(tmp2)):
                p.append(tmp2[j])

    descs = b.find_all(
        "span", class_="a-size-medium a-color-base a-text-normal")

    print(f'Prices: Amount {len(p)}')
    print(f'Desc: Amount {len(descs)}')

    for i in range(len(descs)):
        c_d[i] = {'Desc':descs[i].string}
    for i in range(len(p)):
        # print(i,p[i])
        if i <= len(c_d) - 1:
            c_d[i]['Price'] = p[i].text 
    return c_d

def write(f):
    with open('results.html', "w") as fl:
        fl.write(f)
start()