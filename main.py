import re
from io import BytesIO
import colored
import requests
from requests import Response
from lxml import etree
from fontTools.ttLib import TTFont
from dto import ApplyContactInfo, FontGlyphIdMap
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


def display_unicode(data):
    # 對照此網頁一致：http://www.convertstring.com/zh_TW/EncodeDecode/HexEncode
    # 測試範例：
    return "".join(["\\u%s" % hex(ord(l))[2:].zfill(4) for l in data])


def named_xml_file(fontcss_url: str) -> str:
    pattern = r"[a-zA-Z0-9]+\.css$"
    xml_extension = ".xml"
    matched = re.search(pattern, fontcss_url)
    if matched:
        extension_pattern = ".css$"
        raw_font: str = matched.group()
        fontxml = re.sub(extension_pattern, xml_extension, raw_font)
        return fontxml
    raise Exception("Font File Name not found.")


def retrieve_fontmap(fontcss_url: str) -> FontGlyphIdMap:
    green = colored.fg("green")
    yellow = colored.fg("yellow")
    reset = colored.attr("reset")
    print(green + f"Scraping protection font css url: {fontcss_url}" + reset)
    # 調整文字樣式連結，指向 Font 檔案
    if Config.FONT_HREF_PREFIX in fontcss_url:
        fontfile_url: str = re.sub(Config.FONTCSS_REPLACEMENT_PATTERN, Config.FONT_WOFF_EXTENSION, fontcss_url)
        fontxml = named_xml_file(fontcss_url)
        print(green + f"Scraping protection font file url : {fontfile_url}\n" + reset)
        resp: Response = requests.get(fontfile_url)
        font = TTFont(BytesIO(resp.content))
        font.saveXML(fontxml)
        glyph_names = font.getGlyphNames()
        charmap = font.getBestCmap()
        fontmap = FontGlyphIdMap(glyph_names, charmap)
        # print(yellow + f"Font mapping code: {fontmap}" + reset)
        return fontmap
    raise Exception("The font css URL of scraping protection not found.")


def decode_text(raw_text: str, fontmap: FontGlyphIdMap) -> str:
    unitext: str = display_unicode(raw_text)
    print(f"Unicode text = {unitext}, original = {raw_text}")

    escape_text = raw_text.encode('unicode-escape').decode('utf-8')
    for unichar in escape_text.split("\\u"):
        if unichar:
            content: str = ""
            decimal_code = int(unichar, 16)
            charmap = fontmap.charmap
            glyph_ids = fontmap.glyphs_ids
            charcodes = charmap.keys()
            if decimal_code is charcodes:
                maincode = charmap[decimal_code]
                for glyph_id, code in glyph_ids.items():
                    if maincode is code:
                        content += Config.FONT_GLYPHID_MAPPER[glyph_id]
            print(f"decode content => {content}")
    return content


def scraping_apply_contact(html: bytes):
    tree = etree.HTML(html)
    contactor = str(tree.xpath(Config.CONTACTTOR_XPATH)[0])

    # 以下為帶有 txticon 樣式，加密過的內容
    raw_email = str(tree.xpath(Config.EMAIL_XPATH)[0])
    raw_telphone = str(tree.xpath(Config.TELPHONE_XPATH)[0])
    raw_mobile = str(tree.xpath(Config.MOBILE_PHONE_XPATH)[0])

    raw_fontcss_url = tree.xpath(Config.FONT_RES_HREF_XPATH)[0]
    fontmap: FontGlyphIdMap = retrieve_fontmap(raw_fontcss_url)
    email = decode_text(raw_email, fontmap)
    telphone = decode_text(raw_telphone, fontmap)
    mobile = decode_text(raw_mobile, fontmap)


def scraping():
    resp: Response = requests.get(Config.SITE_URL)
    scraping_apply_contact(resp.content)


if __name__ == "__main__":
    scraping()
