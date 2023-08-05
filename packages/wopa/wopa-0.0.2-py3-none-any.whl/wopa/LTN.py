# 引入所需套件
import os
import re
import math
import pandas as pd
from newspaper import Article
from user_agent import generate_user_agent

# self
from wopa.tool import crawler

# 清理文章內容
def cleanLtnContent(df):
    content=[]
    for i in range(len(df)):
        if type(df.content[i]) != float:
            num=df.content[i].find('var')
            c=df.content[i][:num]
            c=c.replace('請繼續往下閱讀...','').replace("displayDFP('ad-IR1', 'm');",'')
            content.append(c)
        else:
            content.append(df.content[i])
    df.content=content
    return df

def get(keyword, start_time, end_time, num = 1, wait = 3):
    # 創建空的資料陣列
    url, category, date, title, content = [], [], [], [], []
    # for迴圈去換頁
    stop = False
    while stop == False:
        # 載入要抓取的連結
        path = 'https://search.ltn.com.tw/list?keyword='+keyword+'&start_time=' + \
            start_time+'&end_time='+end_time + \
            '&sort=date&type=all&page='+str(num)
        # 使用自訂crawler方法，去讀取網頁
        soup = crawler(path, wait)

        if num == 1:
            mark = soup.find('div', class_='mark').text
            mark = re.search('約有(.\w+.)項結果',mark).group(1).replace(' ','')
            print('自由時報搜索 總共'+str(mark)+'筆資料', '大約'+str(math.ceil(int(mark)/20))+'頁')

        # 找到特定要抓取的區塊
        try:
            li = soup.find('ul', class_='list boxTitle').find_all('li')
        except Exception as e:
            if str(e).find('NoneType') != -1:
                print('抓取 '+keyword+' 區間 '+start_time+'-'+end_time+' 完成')
                stop = True
                break
        for i in li:
            # 抓文章連結 (find a 內的 href 連結)
            post_posturl = i.find('a')['href']
            url.append(post_posturl)
            # 抓文章發布時間 (找到 span 的 text文字)
            date.append(i.span.text)
            # 抓文章主題 (找到 i 的 text文字)
            category.append(i.i.text)
            # 抓文章標題  (find a 內的 title tag 文字)
            title.append(i.find('a')['title'])
            # print(i.find('a')['title'])
            # 抓文章內文
            postSoup = crawler(post_posturl, wait)
            try:
                post_content = postSoup.find('div', class_='text').text.strip()
                if post_content == '':
                    try:  # 因為有不同的自由時報網頁，所以調整不同的抓法
                        post_content = postSoup.find(
                            'div', class_='whitecon article boxTitle boxText').find('div', class_='text').text
                    except:
                        post_content = postSoup.find('div', class_='whitecon article').find(
                            'div', class_='text boxTitle boxText').text
            except:
                #都抓不到用  NewsPaper3k
                article = Article(post_posturl)
                article.download()
                article.parse()
                post_content = article.text.encode('utf-8')
            content.append(post_content)
            print('.',end='')
        # 抓到第幾頁
        print(' 第'+str(num)+'頁完成')
        num += 1

    #存檔成 df
    data = list(zip(category, date, title, content, url))
    df = pd.DataFrame(data, columns=['category', 'date', 'title', 'content','url'])
    df = cleanLtnContent(df)

    newpath='./data/LTN/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    df.to_excel(newpath+'自由時報_'+keyword+'_'+start_time+'-'+end_time+'.xlsx')
    return df
