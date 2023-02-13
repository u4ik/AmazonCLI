#!/usr/bin/env python -B
from bs4 import BeautifulSoup
from os import write
import os
from pprint import pprint
import requests
import re
from InquirerPy import prompt
import itertools   

def start():
    header = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    UNDERLINE = '\033[4m'
    BLUE = '\033[94m'

    def label(s):
        return f"{BOLD}  {s}  {ENDC}"
    def warnlabel(s):
        return f"{header + BOLD + WARNING}  {s}  {ENDC}"
    def okaylabel(s):
        return f"{header + BOLD + OKGREEN}  {s}  {ENDC}"
    def okayblue(s):
        return f"{header + BOLD + BLUE}  {s} {ENDC} "
    def okaycyan(s):
        return f"{header + BOLD }  {s} {ENDC} "

    try:
        q = input(label("Search Amazon For:"))
        while(len(q) == 0):
            print(warnlabel('Enter a search term!'))
            q = input(label("Search Amazon For: "))
            if len(q) > 0:
                break
        m_p = input(label("Min Price: "))
        while(len(m_p) == 0):
            print(warnlabel('Enter a minimum price!'))
            m_p = input(label("Min Price: "))
            if len(m_p) > 0:
                break
        mx_p = input(label("Max Price: "))
        while(len(mx_p) == 0):
            print(warnlabel('Enter a maximum price!'))
            mx_p = input(label("Max Price: "))
            if len(mx_p) > 0:
                break
        sorted_c_d = []
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
        if len(sorted_c_d) == 0:
            print(warnlabel('No Results'))
            return
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
            print(okaylabel(f'{len(sorted_c_d)} Results'))
            # okayblue(' ')
            # pprint(sorted_c_d)
            for i in sorted_c_d:
                size = os.get_terminal_size()
                columns = size.columns
                print(okaylabel("-" * columns))
                print(okayblue(i['Desc']))
                print(okaycyan(i['Arrival']))
                print(okaylabel(i['Price']))
                print(label(i['Image']))
                print(label(i['Link']))
        else:
            return
    except(KeyboardInterrupt) as e:
        print(okaylabel('\n Exiting...'))


def request(url):
    req_headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": r"Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1023"
    }
    response = requests.get(url, headers=req_headers).text
    return response


def sort_price(flag, res):
    if flag == "h":
        return sorted(res, key=lambda x: x['Price_Val'], reverse=True)
    else:
        return sorted(res, key=lambda x: x['Price_Val'])


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
            o = l.find('a')
            link = l.find('a', attrs={'href': True})
            img = l.find('img', attrs={'srcset': True})
            arrival_date = l.find('span', class_="a-text-bold")
            try:
                link_src=[link.attrs['href']]
                link_url = 'https://www.amazon.com'+link_src[0]

                img_src_set=img.attrs['srcset']
                src_arr = img_src_set.split(",")
                img_url = ' '.join(src_arr).split(" ")[0]
                # img_url = src_arr.split(" ")
            except(AttributeError ) as e:
                # print(e)
                continue
            try:
                x = r[2].findChildren('span', class_="a-offscreen")
                for i in x[0]:
                    o = {
                        'id': c,
                        'Desc': l.h2.text,
                        'Price': i.string,
                        'Arrival': arrival_date.string if arrival_date else "----",
                        'Price_Val': int(
                            i.string.replace("$", "").replace(".", "").replace(",", "")[:-2]),
                        'Image': img_url,
                        'Link' : link_url
                    }
                    c_d.append(o)
                    c += 1
            except (NameError, AttributeError, IndexError) as e:
                continue
    return c_d


def write(f):
    with open(f'{os.path.dirname(__file__)}/results.json', "w", encoding='utf-8') as fl:
        fl.write(f)


start()
