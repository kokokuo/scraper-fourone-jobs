from typing import Dict


class ApplyContactInfo(object):
    def __init__(self, contactor: str, email: str, telphone: str, mobile: str) -> None:
        self.contactor = contactor
        self.email = email
        self.telphone = telphone
        self.mobile = mobile


def __repr__(self) -> str:
    return f"<ApplyContactInfo: \n\
        contactor = {self.contactor} \n\
        email = {self.email} \n\
        telphone = {self.telphone} \n\
        mobile={self.mobile} >"


class FontGlyphIdMap(object):

    def __init__(self, glyphs_ids: Dict[str, str], charmap: Dict[int, str]) -> None:
        """
        FontGlyphIdMap 紀錄透過 fonttool 解析取得字型格式中的檔案內容，可以透過 xml 檔案查看。
        基本上最重要的為 GlyphID 標籤、cmap 標籤 與 TTGlyph 標籤

        GlyphID 標籤： 紀錄每一個字型檔中，字型的編號 ID ，以及代表的 unicode 編碼

        cmap 標籤： 除了代表的 unicode 編碼外，還會有其他的編碼也能代表此字型，這些部分都紀錄在 cmap 標籤中，為了適應不同的系統版本。
                   cmap 中會有多個版本。 cmap 中的 code 便是其他的 unicode 16 進制編碼，但在 FontTool 會用 10 建置的數字呈現。

        TTGlyph 標籤：字型的形狀與座標，字型是透過座標所建立的，所以 TTGlyph 會記錄每一個”字型“的描繪座標，大小，還有代表的 unicode 編碼
        Args:
            glyphs_ids (Dict[str, str]): GlyphID 標籤
            charmap (Dict[int, str]): cmap 標籤，會用 10 進制呈現，需要轉換成 16 進制並與編碼過反爬蟲的文字比較

        """
        self.glyphs_ids = glyphs_ids
        self.charmap = charmap

    def __repr__(self) -> str:
        return f"<FontGlyphIdMap: \n\
            glyphs_ids = {self.glyphs_ids} \n\
            charmap = {self.charmap} >"
