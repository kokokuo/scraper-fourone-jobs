from typing import Dict


class Config(object):
    SITE_URL = "https://www.1111.com.tw/job/85992852/?agent=sticktop_51563220_85992852"

    """
    FONT_CSS_HREF_XPATH: Font 所在的 XPATH 標籤 Href
    FONT_CSS_HREF_PATH_PREFIX: Font CSS 檔案的路徑前綴，確認格式用
    FONT_CSS_REPLACEMENT_PATTERN: 取代的 Pattern，為了讓路徑直接切換成 Font 的檔案來源並解析，因為檔案路徑與名稱一致，只需取代副檔名
    FONT_RES_FILE_WOFF_EXTENSION: 字型資源檔的格式副檔名，也是要取代 FONT_CSS_REPLACEMENT_PATTERN 的詞
    """
    FONT_CSS_HREF_XPATH = "/html/head/link[1]/@href"
    FONT_CSS_HREF_PATH_PREFIX = "https://www.1111.com.tw/webService/NET40/Runes/fonts/Books"
    FONT_CSS_REPLACEMENT_PATTERN = r".css$"
    FONT_RES_FILE_WOFF_EXTENSION = ".woff?v0001"

    """
    要爬取解析的 XPATH
    """
    CONTACT_PERSON_XPATH = "//*[@id='Apply']/div/ul/li[1]/div[2]/text()"
    EMAIL_XPATH = "//*[@id='Apply']/div/ul/li[2]/div[2]/text()"
    TELPHONE_XPATH = "//*[@id='Apply']/div/ul/li[3]/div[2]/text()"
    MOBILE_PHONE_XPATH = "//*[@id='Apply']/div/ul/li[4]/div[2]/text()"

    FONT_GLYPHID_MAPPER: Dict[str, str] = {
        "00": " ",
        "01": " ",
        "02": "#",
        "03": "~",
        "04": "(",
        "05": ")",
        "06": "-",
        "07": ".",
        "08": "0",
        "09": "1",
        "10": "2",
        "11": "3",
        "12": "4",
        "13": "5",
        "14": "6",
        "15": "7",
        "16": "8",
        "17": "9",
        "18": "@",
        "19": "_",
        "20": "a",
        "21": "b",
        "22": "c",
        "23": "d",
        "24": "e",
        "25": "f",
        "26": "g",
        "27": "h",
        "28": "i",
        "29": "j",
        "30": "k",
        "31": "l",
        "32": "m",
        "33": "n",
        "34": "o",
        "35": "p",
        "36": "q",
        "37": "r",
        "38": "s",
        "39": "t",
        "40": "u",
        "41": "v",
        "42": "w",
        "43": "x",
        "44": "y",
        "45": "z"
    }
