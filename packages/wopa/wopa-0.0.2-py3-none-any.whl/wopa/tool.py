# 引入所需套件
import time
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

def crawler(url, wait):
    time.sleep(wait)
    # 製作對網頁請求的假資料，如：假裝是IOS手機、Android手機、mac瀏覽器
    user_agent = generate_user_agent(device_type='desktop')
    #對指定的url連結做請求，並給予假資料
    r = requests.get(url, headers={'user-agent': user_agent})
    r.encoding='utf-8'
    #將網頁作解析，以利找到所需資料
    soup = BeautifulSoup(r.text, "html.parser")
    #回傳整個網頁的解析
    return soup