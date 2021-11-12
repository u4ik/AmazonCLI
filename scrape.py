from bs4 import BeautifulSoup
from os import write
from pprint import pprint
import requests
import re
from InquirerPy import prompt


def start():
    # q = input("Search Amazon For: ")
    # m_p = input("Min Price: ")
    # mx_p = input("Max Price: ")

    sorted_c_d = {}
    q = 'ps5'
    m_p = 500
    mx_p = 1000

    s_url = f'https://www.amazon.com/s?k={q}&rh=p_36%3A{m_p}00-{mx_p}00'
    resp = request(s_url)
    questions = [
        {"type": "confirm", "message": "Sort by price?", "name": "sort"},
        {"type": "list", "message": "Sort by...", "name": "sortchoice", "choices": [
            "Highest Price",
            "Lowest Price"
        ]},
        {"type": "confirm",
            "message": "Save output file? (results.json):", "name": "output"},
        {"type": "confirm", "message": "Confirm?", "name": "confirm"},
    ]
    

    res = parse(resp)

    sorted_arr = sorted(res.items(), key=lambda x: x[1]['Price_Val:'])
    
    for i in sorted_arr:
        idx, obj = i 
        sorted_c_d[idx] = ''
        # sorted_c_d[i[0]] = {i[1]['Price_Val:']}
        # sorted_c_d[i[0]] = {"Desc:":i[1]['Desc:']}
        # sorted_c_d[i[0]]['Price:'] = i[1]['Price_Val:']

        # print(i[0])
        # print(i[1]['Desc:'])
        # print(i[1]['Price:'])
        # print(i[1]['Price_Val:'])
    pprint(sorted_c_d)

    # sort_items = sorted(res.items(), key=lambda x: (x[2]['Price_Val']))
    # print(sort_items)

    # sort_result = prompt(questions[0])
    # sort = sort_result["sort"]

    # if sort:
    #     sort_result = prompt(questions[1])
    #     sort_choice = sort_result["sortchoice"]

    # outresult = prompt(questions[2])
    # output = outresult["output"]

    # confirmresult = prompt(questions[-1])
    # confirm = confirmresult["confirm"]

    # if confirm:
    #     res = parse(resp)
    #     sort_items = sorted(res.items(), key=lambda x: x[1]['Price'])
    #     print(sort_items)
    #     if sort:
    #         if sort_choice[0] == "H":
    #             sort_price('h', res )
    #         else:
    #             sort_price('l', res )
    #     else:
    #         pprint(f'{len(res)} Results')
    #         # pprint(res)
    #         if output:
    #             write(str(res))
    #         else:
    #             return
    # else:
    #     return


def request(url):
    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    response = requests.get(url, headers=req_headers).text
    return response


def sort_price(flag, res):

    # sort_items = sorted(res.items())
    # print()

    if flag == "h":
        print('sorting highest')
    else:
        print('sorting lowest')


def parse(res):
    t = 'div'
    c_d = {}
    c = 0
    b = BeautifulSoup(res, "html.parser")
    p_w = b.findChildren(
        'div', class_='s-main-slot s-result-list s-search-results sg-row')
    for p in p_w:
        f_c = p.findChildren(t, class_='s-result-item',
                             attrs={"data-index": True, "data-asin": True}, recursive=True)

        for l in f_c[1:-2]:
            r = l.findChildren(t, class_="sg-col-inner")
            try:
                x = r[2].findChildren('span', class_="a-offscreen")
                for i in x[0]:
                    c_d[c] = {'Desc:': l.h2.text}
                    c_d[c]['Price:'] = i.string
                    c_d[c]['Price_Val:'] = int(
                        i.string.replace("$", "").replace(".", "")[:-2])
                    c += 1
            except (NameError, AttributeError, IndexError) as e:
                continue
    return c_d


def write(f):
    with open('results.json', "w", encoding='utf-8') as fl:
        fl.write(f)


start()
