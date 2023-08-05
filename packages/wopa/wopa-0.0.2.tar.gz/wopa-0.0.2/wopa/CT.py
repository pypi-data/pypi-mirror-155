# 引入所需套件
import os
import re
import time
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article
from user_agent import generate_user_agent

# self
from wopa.tool import crawler

def get(keyword, page = 1, wait = 3):
    # 創建空的資料陣列
    url, category, date, title, content, source, author, hashtag = [], [], [], [], [], [], [], []

    # for迴圈去換頁
    stop = False
    while stop == False:
        # 載入要抓取的連結
        path = 'https://www.chinatimes.com/search/'+keyword+'?page='+str(page)+'&chdtv'
        
        # 使用自訂crawler方法，去讀取網頁
        soup = crawler(path, wait)
        
        # 判斷完成與否與資料筆數
        result = soup.find('span', class_='search-result-count').text
        if result == '00':
            print('抓取 '+keyword+' 完成')
            stop = True
            break
        if page == 1:
            print('中國時報搜索 總共'+str(result)+'筆資料', '大約'+str(math.ceil(int(result)/20))+'頁')

        li = soup.find('div', class_='article-list').find_all('div', class_='col')
        for i in li:
            # 抓文章連結 (find a 內的 href 連結)
            post_posturl = i.find('a')['href']
            url.append(post_posturl)
            # 抓文章發布時間 (找到 span 的 text文字)
            date.append(i.find('time')['datetime'])
            # 抓文章主題 (找到 i 的 text文字)
            category.append(i.find('div', class_='category').text)
            # 抓文章標題  (find a 內的 title tag 文字)
            title.append(i.find('h3', class_='title').text)

            # 抓文章內文
            postSoup = crawler(post_posturl, wait)
            sou = postSoup.find('div',class_='source').text.strip()
            auth = postSoup.find('div',class_='author').text.strip()
            hasht = postSoup.find('div', class_='article-hash-tag').text.strip()
            post_content=''
            for c in postSoup.find('div', class_='article-body').find_all('p'):
                post_content += c.text + '\n'
            content.append(post_content)
            source.append(sou)
            author.append(auth)
            hashtag.append(hasht)
            print('.',end='')
        # 抓到第幾頁
        print(' 第'+str(page)+'頁完成')
        page+=1

        data = list(zip(category, date, title, url, content, source, author, hashtag))
        df = pd.DataFrame(data, columns=['category', 'date', 'title','url','content', 'source', 'author', 'hashtag'])

        newpath='./data/CT/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        df.to_excel(newpath+'中國時報_'+keyword+'_.xlsx')
        return df
            