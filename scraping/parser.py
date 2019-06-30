import re
from lxml import etree
from scraping.dto import ApplyContactPerson, WOFFContent
from scraping.decode import FontTextDecoder
from scraping.font import WebOpenFontReader
from settings import Config


class ContactPesonParsingService(object):
    def __init__(self) -> None:
        pass

    def _find_custom_font(self, html: bytes) -> str:
        tree = etree.HTML(html)
        # 取得字型的 CSS 定義檔所在網址
        custom_font_css_path = str(tree.xpath(Config.FONT_CSS_HREF_XPATH)[0])
        print(f"Extracted custom defined CSS Font URL path: {custom_font_css_path}")
        # 調整文字樣式連結，指向 Font 檔案
        if Config.FONT_CSS_HREF_PATH_PREFIX in custom_font_css_path:
            custom_font_path: str = re.sub(Config.FONT_CSS_REPLACEMENT_PATTERN,
                                           Config.FONT_RES_FILE_WOFF_EXTENSION,
                                           custom_font_css_path)
            print(f"Custom defined Font resouce URL path: {custom_font_path}\n")
            return custom_font_path
        raise Exception("Not Find Custom Defined CSS Font URL")

    def parse(self, html: bytes) -> ApplyContactPerson:
        # 透過 XPATH 取得資訊
        tree = etree.HTML(html)
        contact_name = str(tree.xpath(Config.CONTACT_PERSON_XPATH)[0])

        # 以下為帶有 txticon 樣式，加密過的內容
        raw_email = str(tree.xpath(Config.EMAIL_XPATH)[0])
        raw_telphone = str(tree.xpath(Config.TELPHONE_XPATH)[0])
        raw_mobile = str(tree.xpath(Config.MOBILE_PHONE_XPATH)[0])

        # 取得字型的 CSS 定義檔所在網址路徑
        custom_font_path = self._find_custom_font(html)
        woff: WOFFContent = WebOpenFontReader.read(custom_font_path)

        # 解碼內容
        decoder = FontTextDecoder(woff, Config.FONT_GLYPHID_TRANSLATOR)
        email = decoder.decode(raw_email)
        telphone = decoder.decode(raw_telphone)
        mobile = decoder.decode(raw_mobile)
        return ApplyContactPerson(contact_name, email, telphone, mobile)
