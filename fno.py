import requests
from bs4 import BeautifulSoup
import re

url = 'http://kgd.gov.kz/ru/content/fno-na-2018-god-1'
fnos = ['100.00', '101.01', '101.02', '101.04', 
        '320.00', '200.00', '300.00', '328.00', 
        '870.00', '590.00', '701.00', '700.00', 
        '851.00']

def get_html(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text


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
     codeRegex = re.compile(r'\d{3}\.\d{2}')
     verRegex = re.compile(r'>\d{2}.?<')
     ftpRegex = re.compile(r'ftp.*2')       
                         
     b = []
     len_list = len(fnos)

     for i in range(len_list):
        b.append([0] * 3)

     for c in range(len_list):
             for j in list[c]:
                     text = str(list[c])
                     code = codeRegex.search(text)
                     verRaw = verRegex.findall(text)
                     ver = ''.join(verRaw)   
                     fno = ftpRegex.search(text)
                     b[c][0] = code.group(0)
                     b[c][1] = ver.strip('><')
                     b[c][2] = fno.group(0)

     return b
      
 
def main():
    a = search_fno(get_tr(get_html(url)))
    b = create_sub_list(a)
    print(b)

if __name__ == '__main__':
    main()