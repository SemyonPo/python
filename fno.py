import requests
from bs4 import BeautifulSoup

url = 'http://kgd.gov.kz/ru/content/fno-na-2018-god-1'


def get_html(url):
    r = requests.get(url)
    return r.text


def get_tr(html):
    soup = BeautifulSoup(html, 'lxml')
    td = soup.find('tbody').find_all('tr')[13:].find_all('td')
    
    print(td)
    return td


def search_fno(get_tr):
    fno = []
    for f in get_tr:
        s = f.find('p')
        if s.get_text() == '300.00':
            fno.append(f)
    return fno

 
def main():
    a = (search_fno(get_tr(get_html(url))))
    print(a)

if __name__ == '__main__':
    main()