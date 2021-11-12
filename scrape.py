from bs4 import BeautifulSoup
from os import write
from pprint import pprint
import requests
import re

def start():
    # q = input("Search Amazon For: ")
    q = 'ps5'

    s_url = f'https://www.amazon.com/s?k={q}'
    resp = request(s_url)
    res = parse(resp)

    # ? PRINT FINAL RESULTS:
    # pprint(f'Results: {len(res)}')
    # pprint(res)

    # ? SAVE FINAL RESULTS:
    # write(str(res))


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
    # p_wrap = b.find_all('a', class_="a-size-base a-link-normal a-text-normal")

# testing
    p_wrap = b.findChildren('div', class_='s-main-slot s-result-list s-search-results sg-row')


    tmp = []
    for p in p_wrap:
        f_c = p.findChildren('div', class_='s-result-item', attrs={"data-index": True, "data-asin": True } ,recursive=True)
        

        for l in f_c[1:]:
            r = l.findChildren("div", class_="sg-col-inner")
            print(r.h2.text)
            for f in r:
                d = f.findChildren('h2')
                # for i in d:
                    # print(i.text)

                   
    


         
            # print(l)
        # print(f_c)
        # for c in f_c:
            # item = c.findChildren('div', class_="s-asin")
            # print(item)
            # c2 = c.findChildred('div', attrs={'data-index':1} )
            # pprint(len(c2))
                # if c.has_attr('data-asin'):
                #     print(len(c))
                #     if c.has_attr('data-component-type'):
                #         # pprint(c.prettify())
                #         write(str(c))
    write(str(tmp))
    # pprint(tmp)
            

    # print(p_wrap.encode("utf-8"))
    p = []


    # for i in range(len(p_wrap)):
    #     tmp1 = p_wrap[i].findChildren(
    #         "span", class_="a-price", attrs={"data-a-size": "l", "data-a-color": "base"}, recursive=True)
    #     for k in range(len(tmp1)):
    #         tmp2 = tmp1[k].findChildren(
    #             "span", class_="a-offscreen", recursive=True)
    #         for j in range(len(tmp2)):
    #             p.append(tmp2[j])
    # descs = b.find_all(
    #     "span", class_="a-size-medium a-color-base a-text-normal")
    # print(f'Prices: Amount {len(p)}')
    # print(f'Desc: Amount {len(descs)}')
    # for i in range(len(descs)):
    #     c_d[i] = {'Desc': descs[i].string}
    # for i in range(len(p)):
    #     # print(i,p[i])
    #     if i <= len(c_d) - 1:
    #         c_d[i]['Price'] = p[i].text
    # return c_d


def write(f):
    with open('results.html', "w",encoding='utf-8') as fl:
        fl.write(f)


start()
