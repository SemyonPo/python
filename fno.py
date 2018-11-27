import requests
from bs4 import BeautifulSoup
import re
import shelve

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
                         
     list_forms = []
     len_list = len(fnos)

     for i in range(len_list):
        list_forms.append([0] * 3)

     for c in range(len_list):
             for j in list[c]:
                     text = str(list[c])
                     code = codeRegex.search(text)
                     verRaw = verRegex.findall(text)
                     ver = ''.join(verRaw)   
                     fno = ftpRegex.search(text)
                     list_forms[c][0] = code.group(0)
                     list_forms[c][1] = ver.strip('><')
                     list_forms[c][2] = fno.group(0)
     return list_forms
      
def safe_list_on_hdd(list):
        shelFile = shelve.open('formsdata')
        shelFile['forms'] = list
        shelFile.close

def check_for_new_files(list):
        shelFile = shelve.open('formsdata')
        savedList = shelFile['forms']
        
        curentList = list
        c = 0
        for i in range(len(curentList)):
                a = curentList[i][1]
                b = savedList[i][1]
                if a == b:
                        continue
                else:
                        c +=1

        if c != 0:
                print('save list on hdd')
                safe_list_on_hdd(list)

def main():
    a = search_fno(get_tr(get_html(url)))
    b = create_sub_list(a)
    check_for_new_files(b)
    #print(b)

if __name__ == '__main__':
    main()