import requests
from bs4 import BeautifulSoup

url = 'http://kgd.gov.kz/ru/content/fno-na-2018-god-1'
fnos = ['100.00', '101.01', '101.02', '101.04', 
        '320.00', '200.00', '300.00', '328.00', 
        '870.00', '590.00', '701.00', '700.00', 
        '851.00'
        ]

def get_html(url):
    r = requests.get(url)
    return r.text


def get_tr(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('tbody').find_all('tr')[13:]
    return table


def search_fno(get_tr):
    fno = []
    for f in get_tr:
        s = f.find('p')
        if s.get_text() in fnos:
            fno.append(f)
    return fno


def create_sub_list(list):
     b = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
     for i in range(len(list)):
        
        b[i].append(s.get_text)

     return b
      
 
def main():
    a = (search_fno(get_tr(get_html(url))))
    b = create_sub_list(a)
    print(b)

if __name__ == '__main__':
    main()