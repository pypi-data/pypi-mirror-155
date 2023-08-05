# 我爬 Wopa

**我爬 Wopa** 一個給研究者使用的簡單便利資料搜索工具 

本工具透過網路爬蟲獲取所需研究資料，為撰寫論文、研究等**非商業行為使用**。同時，若有使用此工具之論文、研究，歡迎提供展示於此git，供其他學術使用參考。

## 🌼 目前的功能
給予特定參數後，程式會自動抓取資料，完成後會在目錄下新增對應的資料夾，並將Excel檔儲存至資料夾內。

#### 新聞
* [x] 自由時報（搜索）
* [X] 中國時報（搜索）
* [ ] 蘋果新聞網（搜索）
* [ ] 聯合新聞網

#### 論壇
* [ ] Dcard
* [ ] PTT

> 更多其他正在開發中，也可以幫忙貢獻唷！

# 如何使用
## 安裝
```console
$ pip install wopa
```

## 參數說明
|  參數  |  解釋  |  範例  |  預設  |
| ------ | ------ | ------ | ------ |
| keyword | 關鍵字  | '蔡英文' | None |
| start_time  | 起始時間 | '20220612' | None |
| end_time  | 結束時間 |   '20220614'  | None |
| pageNumber  | 從第幾頁開始抓資料 |  1  | 第1頁 |
| waitSec  | 資料抓取時間間隔 |  3 | 3秒 |

## 自由時報 (關鍵字)
```python
from papa import LTN
df = LTN.get(keyword, start_time, end_time, pageNumber, waitSec)
# df 回傳 DataFrame
# 自動產生目錄LTN資料夾，儲存excel檔
```

## 中國時報 (關鍵字)
```python
from papa import CT
df = CT.get(keyword, pageNumber, waitSec)
# df 回傳 DataFrame 
# 自動產生目錄CT資料夾，儲存excel檔
```

## 貢獻
歡迎協作，請使用 GitHub issue 以及 Pull Request 功能來協作。
