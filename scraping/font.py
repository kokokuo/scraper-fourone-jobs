import re
import io
from typing import List, Dict
import requests
from requests import Response
from fontTools.ttLib import TTFont
from scraping.dto import WOFFContent
from settings import Config


class WebOpenFontReader(object):
    @classmethod
    def named_xml(cls, fonturl: str) -> str:
        """
        命名 XML 檔名，透過字型網址路徑，擷取該檔案的名稱命名成 XML 副檔名
        """
        pattern = r"[a-zA-Z0-9]+\.woff\?v0001$"
        xml_extension = ".xml"
        matched = re.search(pattern, fonturl)
        if matched:
            extension_pattern = r".woff\?v0001$"
            raw_font: str = matched.group()
            xmlname = re.sub(extension_pattern, xml_extension, raw_font)
            return xmlname
        raise Exception("Font Font File Name not found.")

    @classmethod
    def read(cls, fonturl: str) -> WOFFContent:
        """
        取得 WOFF 格式的 Font 檔案資訊
        Args:
            fonturl (str): 字型來源網址
        Returns:
            WOFFContent: 解析讀取後的內容
        """
        resp: Response = requests.get(fonturl)
        font = TTFont(io.BytesIO(resp.content))
        xmlname = cls.named_xml(fonturl)
        font.saveXML(xmlname)
        # 把 List 轉換成字典形式
        orders: List[str] = font.getGlyphOrder()
        glyphs: Dict[str, str] = {
            str(idx).zfill(2): orders[idx]
            for idx in range(len(orders))
        }
        charmap = font.getBestCmap()
        woff = WOFFContent(glyphs, charmap)
        return woff
