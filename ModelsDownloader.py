#!/usr/bin/env python
# coding: utf-8

import os
import requests
import random
import time
import requests
import re
from bs4 import BeautifulSoup

def parse_urls_generate_in_file(urlFile):
    uris = {'uri':[r'https://t0105774.wixsite.com/artcam2011/26gallery',
    r'https://t0105774.wixsite.com/artcam2011/01gallery',
    r'https://t0105774.wixsite.com/artcam2011/02gallery',
    r'https://t0105774.wixsite.com/artcam2011/03gallery',
    r'https://t0105774.wixsite.com/artcam2011/04gallery',
    r'https://t0105774.wixsite.com/artcam2011/05gallery',
    r'https://t0105774.wixsite.com/artcam2011/06gallery',
    r'https://t0105774.wixsite.com/artcam2011/08gallery',
    r'https://t0105774.wixsite.com/artcam2011/10gallery',
    r'https://t0105774.wixsite.com/artcam2011/11gallery',
    r'https://t0105774.wixsite.com/artcam2011/12gallery',
    r'https://t0105774.wixsite.com/artcam2011/13gallery',
    r'https://t0105774.wixsite.com/artcam2011/14gallery',
    r'https://t0105774.wixsite.com/artcam2011/15gallery',
    r'https://t0105774.wixsite.com/artcam2011/17gallery',
    r'https://t0105774.wixsite.com/artcam2011/19gallery',
    r'https://t0105774.wixsite.com/artcam2011/21gallery',
    r'https://t0105774.wixsite.com/artcam2011/23gallery',
    r'https://t0105774.wixsite.com/artcam2011/20gallery',
    r'https://t0105774.wixsite.com/artcam2011/25gallery',
    r'https://t0105774.wixsite.com/artcam2011/18gallery',
    r'https://t0105774.wixsite.com/artcam2011/16gallery',
    r'https://t0105774.wixsite.com/artcam2011/07gallery',
    r'https://t0105774.wixsite.com/artcam2011/modeli-igorya-bezfamilii'], 
    'name':[r'Расстения, цветы и их части', 
            r'Подвески и медальоны',
            r'Ордена, медали и нагрудные знаки',
            r'Гербы',
            r'Панно',
            r'Животные и птицы',
            r'Логотипы и эмблемы',
            r'Шахматные поля',
            r'Христианские символы и иконы',
            r'Мусульманские символы',
            r'Языческие символы',
            r'Оружие',
            r'Рамы и багет, декор',
            r'Части моделей и рельефов',
            r'Таблички и вывески',
            r'Люди, фигуры и лица, бюсты',
            r'Розетки и картуши',
            r'Знаки зодиака',
            r'Мебель и ее детали',
            r'Эмблемы футбольных клубов',
            r'Авто, мото и военная техника',
            r'Декоративные 2D решетки',
            r'Нарды',
            r'Модели Игоря Безфамилии']}

    curDirNumber = 0
    for uri in uris["uri"]:
        res = requests.get(uri)
        soup = BeautifulSoup(res.text, 'lxml')
        with open(urlFile, 'a') as f:
            f.writelines("The " + uris["name"][curDirNumber] + ":\n")
            print("trying parse " + "The " + uris["name"][curDirNumber])
            for jsStr in re.findall((r'title(.*?)\}\}'), soup.findAll("script", attrs={ "type" : "text/javascript"})[5].text):
                url = re.search((r'https:\\\/\\\/cloud\.mail\.ru\\\/public\\\/[^\"]*'), jsStr)
                if not url:
                    continue;
                name = re.search((r':"(.+?)"'), jsStr)[0]
                f.writelines(name[2:-1] + "\n" + url.group().replace('\\','') + "\n")
        curDirNumber +=1
        
        

def getDirectLink(cloudURL):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    params = {'key': '02822b8222e99221ff0397ec0d02c970', 
              'url': cloudURL}
    res = requests.get(r'https://rocld.com/api', params = params, headers = headers).json()
    if(not res["error"]):
        return res["url"]
    else:
        raise Exception("Could not get direct link")
        
        

def count_lines(filename, chunk_size=1<<13):
    with open(filename) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))
    
    
    
if __name__ == "__main__":
    #main_folder_name = r'C:\Users\pervo\Untitled Folder'
    main_folder_name = os.getcwd()

    in_file_name = main_folder_name + "\\NamedURLs.txt"

    log_file_name = main_folder_name + "\\log.txt"
    with open(log_file_name, 'a') as f:
        pass
    files_already_downloaded = count_lines(log_file_name)

    if not(os.path.exists(in_file_name)):
        print("beginning parsing")
        parse_urls_generate_in_file(in_file_name)
    else:
        print("Continue downloading" +  " from " + str(files_already_downloaded))

    total_files_amount = round(count_lines(in_file_name)/2)

    print("beginning downloading")
    with open(in_file_name, 'r') as in_file:
        for idx in range(total_files_amount):
            out_file_name = in_file.readline().strip()
            
            if(out_file_name[0:3]=="The"):
                if os.chdir(main_folder_name+ '\/' + out_file_name[3:-1]):
                    os.mkdir(main_folder_name + '\/' + out_file_name[3:-1])
                os.chdir(main_folder_name+ '\/' + out_file_name[3:-1])
                out_file_name = in_file.readline().strip()
                
            url = in_file.readline()
            if not url.__contains__(".zip"):
                out_file_name += ".rar"
                
            if(os.listdir(os.getcwd()).__contains__(out_file_name)):
                out_file_name = (str)(random.randint(1,1000000)) + out_file_name
                
            url = getDirectLink(url)
            print("trying: " + out_file_name + " " + url)

            if idx < files_already_downloaded:
                continue

            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
            res = requests.get(url, headers=headers)
            with open(out_file_name, 'wb') as out_file:
                out_file.write(res.content)
                
            print("{0}: In folder: \"{1}\" file \"{2}\" was downloaded".format(time.ctime(), os.getcwd(), out_file_name))

            with open(log_file_name, 'a') as f:
                f.writelines("{0}: In folder: \"{1}\" file \"{2}\" was downloaded\n".format(time.ctime(), os.getcwd(), out_file_name))

