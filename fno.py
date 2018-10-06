import requests
from bs4 import BeautifulSoup

url = 'http://kgd.gov.kz/ru/content/fno-na-2018-god-1'


def get_html(url):
    r = requests.get(url)
    return r.text


def get_tr(html):
    soup = BeautifulSoup(html.text, 'lxml')
    tr = soup.find('td').find_all('tr')[13]
    return tr


def search_fno(get_tr):
    fno = []
    for f in get_tr:
        s = f.find('p')
        if s.get_text() == '300.00':
            fno.append(f)
    return fno

 
def main():
    pass

if __name__ == '__main__':
    main()