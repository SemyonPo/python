import requests
from bs4 import BeautifulSoup
import re
import shelve
import urllib.request
import os
import datetime
import smtplib

dt = datetime.datetime.now()
year = dt.year
day = dt.day
month = dt.month
curent_date = str(day) + '.' + str(month)
emails = ['pokivaylo@rakhat.kz', 'tishina@rakhat.kz', 'karacheva@rakhat.kz',
         'jigitova@rakhat.kz', 'g_tuleuova@rakhat.kz', 'nemchenko@rakhat.kz']
body = "Subject: Sono Forms.\nОбновленные формы SONO находятся в каталоге: Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s\\%s" % (year, curent_date)

url = 'http://kgd.gov.kz/ru/content/fno-na-%s-god-1' %year
print(url)
print('+----------------------------------------------+')
fnos = ['100.00', '101.01', '101.02', '101.04', 
        '320.00', '200.00', '300.00', '328.00', 
        '870.00', '590.00', '701.01', '700.00', 
        '851.00', '220.00', '871.00',]

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
    verRegex = re.compile(r'>\d.?.?<')
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
            ftp = ftpRegex.search(text)
            list_forms[c][0] = code.group(0)
            list_forms[c][1] = ver.strip('><')
            list_forms[c][2] = ftp.group(0)
    return list_forms
      
def safe_list_on_hdd(list):
    print('start safing')
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
        print('curent ver ' + curentList[i][0])
        print(a)
        b = savedList[i][1]
        print('saved ver ' + savedList[i][0])
        print(b)
        if a != b:
            link = curentList[i][2]
            print('+----------------------------------------------+')
            print('start downloading ' + curentList[i][0])
            download_forms(link)
            c += 1

    if c != 0:
        print('save curent list on hdd')
        os.chdir('D:\\python\\python')
        safe_list_on_hdd(list)
        smtp()
    print('+----------------------------------------------+')
    print('number of downloaded files - ' + str(c))

def download_forms(link):
    
    file_name = os.path.basename(link)
    
    if os.path.exists('Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s' %year):
        os.chdir('Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s' %year)
        if os.path.exists('Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s\\%s' %(year, curent_date)) == False:
            os.makedirs(curent_date)
    else:
        os.makedirs('Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s' %year)
        os.chdir('Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s' %year)
        os.makedirs(curent_date)

    os.chdir('Q:\\ASU_ARM\\TAX\\SONO_Forms\\%s' %year)
    os.chdir(curent_date)
    urllib.request.urlretrieve(link, file_name)
    print('end downloading ' + file_name)
    print('+----------------------------------------------+')

def smtp():
    smtpObj = smtplib.SMTP('10.128.0.0', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('pokivaylo', 'test1234')
    smtpObj.sendmail('pokivaylo@rakhat.kz', emails, body.encode('cp866'))
    smtpObj.quit()

def main():
    a = search_fno(get_tr(get_html(url)))
    b = create_sub_list(a)
    check_for_new_files(b)
    #safe_list_on_hdd(b)

if __name__ == '__main__':
    main()