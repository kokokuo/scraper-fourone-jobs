import requests
from requests import Response
from scraping.dto import ApplyContactPerson, WOFFContent
from scraping.parser import ContactPesonParsingService
from settings import Config

"""
2019.06.26, 因 Python Taiwan 有網友發問如何解析 1111 人力銀行的應徵資料，所以來研究如何找尋
資料來源： https://www.1111.com.tw/job/85992852/?agent=sticktop_51563220_85992852
該網站採用 CSS 文字加解密反爬蟲技巧，對含有 txticon 的 CSS 樣式資料，採用了自訂的 Font 格式，並處理解碼因而可以呈現內容。

解法 :
1. 找尋 txticon 的 CSS 樣式採用的 font-family: 'runes' 來源 font-face 檔案內容
2. 下載檔案 'runes' 文字的 woff 格式，並透過 Font 線上檢視服務 「FontDrop」 查看其對照編媽，並確認是否可以解碼出內容
3. 確認可以後，因為該檔案是由後端自動產生，並夾帶在前端，需要解析網頁有無 https://www.1111.com.tw/webService/NET40/Runes/fonts/Books/
來源的 link 檔案，找到此檔案下載至爬蟲程式的文件中
4. 透過 Python 的 FontTool 套件取出對應的關係資料
"""


def output(result: ApplyContactPerson) -> None:
    print("Finish scraping and decode encrption text ！")
    print(f"> 聯繫人: {result.contact_name}")
    print(f"> 電子郵件: {result.email}")
    print(f"> 市話: {result.telphone}")
    print(f"> 手機: {result.mobile}")


def start_scraping():
    resp: Response = requests.get(Config.SITE_URL)
    parsing_service = ContactPesonParsingService()
    result: ApplyContactPerson = parsing_service.parse(resp.content)
    output(result)


if __name__ == "__main__":
    start_scraping()
