from typing import Dict, List, Optional
from scraping.dto import WOFFContent
from settings import Config


class FontTextDecoder(object):
    def __init__(self, woff: WOFFContent, font_translator: Dict[str, str]) -> None:
        self._woff = woff
        self._font_translator = font_translator

    def _restore_unicode(self, data: str) -> str:
        """
        由於在 Python 3 中，字串都是 Unicode 格式任何的字型內容都會在顯示時被解析，因此無法顯示 Unicode 的編碼
        因此藉由此方法還原編碼的樣子並能在 print 顯示。
        對照此網頁一致：http://www.convertstring.com/zh_TW/EncodeDecode/HexEncode

        法二： 可以透過跳脫字元 raw_source.encode('unicode-escape').decode('utf-8') 顯示
        # 測試範例：
        Args:
            data (str): 要轉換還原編碼模式的資料
        """
        return "".join(["\\u%s" % hex(ord(l))[2:].zfill(4) for l in data])

    def _translate(self, unichar: str) -> Optional[str]:
        """
        對來源 Unicode 編碼每個字元做解析跟查表翻譯來解碼
        Args:
            unichar (str): Unicode 字元
        Returns:
            str: 翻譯後的字元
        """
        if unichar:
            # 轉換成 16 進制的數字，拿來對照 Charmap 是否存在
            hex_decimal = int(unichar, 16)
            charmap = self._woff.charmap
            glyphs = self._woff.glyphs
            if hex_decimal in charmap.keys():
                keycode = charmap[hex_decimal]
                for glyphid, code in glyphs.items():
                    if keycode is code:
                        decoded = self._font_translator[glyphid]
                        print(f" [ Match ]  Unicode char decoded - {keycode} > {decoded}")
                        return decoded
        return None

    def decode(self, raw_source: str) -> str:
        result: str = ""
        # unicode_source: str = self._restore_unicode(raw_source)
        # 透過跳脫字元顯示源碼，等同上面方法
        escape_source = raw_source.encode('unicode-escape').decode('utf-8')
        print(f" - Original = {raw_source}")
        # print(f" - Unicode restore content = {unicode_source}")
        print(f" - Unicode Escape  content = {escape_source}")

        unichars: List[str] = escape_source.split("\\u")
        print(f" - Unicode Char List = {unichars}")
        print(f" Starting to decode ...")
        print("============================================================")
        for unichar in unichars:
            decoded = self._translate(unichar)
            result += decoded if decoded else ""
        result = result.replace(" ", "")
        print(f" - Decoded content = {result}")
        print("============================================================")
        return result
