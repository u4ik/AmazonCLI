from bs4 import BeautifulSoup
from os import write
from pprint import pprint
import requests
import re
from InquirerPy import prompt


def start():
    try:
        q = input("Search Amazon For: ")
        
        while( len(q) == 0):
            print('Enter a search term!')
            q = input("Search Amazon For: ")
            if len(q) > 0:
                break

        m_p = input("Min Price: ")

        while( len(m_p) == 0):
            print('Enter a minimum price!')
            m_p = input("Min Price: ")
            if len(m_p) > 0:
                break


        mx_p = input("Max Price: ")


        while( len(mx_p) == 0):
            print('Enter a maximum price!')
            mx_p = input("Max Price: ")
            if len(mx_p) > 0:
                break
        


        sorted_c_d = []
        # q = 'ps5'
        # m_p = 500
        # mx_p = 1200
        
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

        sorted_c_d = res

        sort_result = prompt(questions[0])
        sort = sort_result["sort"]

        if sort:
            sort_result = prompt(questions[1])
            sort_choice = sort_result["sortchoice"]

        outresult = prompt(questions[2])
        output = outresult["output"]

        confirmresult = prompt(questions[-1])
        confirm = confirmresult["confirm"]

        if confirm:
            if sort:
                if sort_choice[0] == "H":
                    sorted_c_d = sort_price('h', res)
                else:
                    sorted_c_d = sort_price('', res)
            if output:
                write(str(sorted_c_d))
            pprint(sorted_c_d)
            pprint(f'{len(sorted_c_d)} Results')
        else:
            return
    except(KeyboardInterrupt) as e:
        print('\nExiting...')


def request(url):
    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    response = requests.get(url, headers=req_headers).text
    return response


def sort_price(flag, res):
    if flag == "h":
        return sorted(res, key=lambda x: x['Price_Val:'], reverse=True)
    else:
        return sorted(res, key=lambda x: x['Price_Val:'])


def parse(res):
    t = 'div'
    c_d = []
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
                    o = {
                        'id': c,
                        'Desc': l.h2.text,
                        'Price': i.string,
                        'Price_Val:': int(
                            i.string.replace("$", "").replace(".", "").replace(",","")[:-2]),
                    }
                    c_d.append(o)
                    c += 1
            except (NameError, AttributeError, IndexError) as e:
                continue
    return c_d


def write(f):
    with open('results.json', "w", encoding='utf-8') as fl:
        fl.write(f)


start()
