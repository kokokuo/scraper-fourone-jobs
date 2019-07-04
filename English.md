# scraper-fourone-jobs

## Translation Assistance Need you 🙏🙏🙏
You're welcome to come to this repository. If you like the repository, hope you could give me a Star. If you are interested, the current English translation is in progress. Really welcome the **fork** project and assist to translate and send PR :)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) [![Python 3.7.1](https://img.shields.io/badge/Python-3.7.1-blue.svg)](https://www.python.org/downloads/release/python-371/)

<p align="center">
  <img src="../master/Images/Program-Result.png?raw=true" width="640px">
</p>

scraper-fourone-jobs is a anti-scraping cracker for extracting apply information of one of Taiwan famous [jobs recruiting website](https://1111.com.tw), this program only for learning and researching how to crack anti-scraping, please **DO NOT use for commercial**.

The reason for creating the project is that saw a question that someone asked how to do scraping for this website in "Python Taiwan Community" of Facebook group, and in the processing of answering, I think that need to write program by myself, and then will know what the detail, even though there are some tips how to crack.

The project was completed in 2019.06.28, and the website will change to other anti-scraping method by the time, so the program will crashed in the future. If you discover the problem, free feel to send a PR or Issue thanks!

**<p align="center">The data would lke to scrape and show the HTML source.</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-fourone-jobs-apply-contents.png?raw=true" width="640px">
</p>

## Prerequisite
- Development enviroment： `vscode`
- Language version： `Python 3.7`
- Package： `pipenv`, `fonttools`, `lxml`, `requests`

## How to Crack

The program which would like to scrape and extract data is from the recruitment page [乙級-職業安全衛生管理員(兼職可)](https://www.1111.com.tw/job/85992852/?agent=sticktop_51563220_85992852) and the data "email", "telephone" and "mobile" could not scrape from correct way like XPATH, it's will show unmeaningful data and encoding, here is the HTML page source as below.

**<p align="center">HTML Page Source Content</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-css-font-class-style.png?raw=true" width="640px">
</p>


**Attention** ： From Here, the document will introduce how to crack, but not reveal all information for protecting the jobs recruiting website. Please **DO NOT** use the program for commercial use.

### 1. Anti-scraping analyzing

In anti-scraping, ths situation for showing data correct but HTML page source is unmeaningful and weired content, the reason almost caused by Javascript dynamic handling or CSS font encoding. For the javascript, it could change the content after DOM loaded or some event triggred. In CSS, it could change the text style by CSS attribute.
 
As time goes by analyzing and reading the source by DevTools, found the possible source is `txticon` ths class selector from CSS, and discover the user-defined font value `'runes'` from `font-family` attribute: 

**<p align="center">The CSS style declaration of txticon</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-css-font-family-and-font-file.png?raw=true" width="640px">
</p>

Usually when you found the user-defined font value from `font-family`, it's means the anti-scraping method from CSS font encoding.

<br/>

### 2. Search font file used for encoding of CSS anti-scraping

Because the font of `font-family ` is user-defined, the source font file must exsit, so the website could show the correct content. After searching the files location further, there were a path called `webService/NET40/Runes/fonts/Books` and the user-defined font CSS `xxxxx.css` was put in here with the font file `xxxxx.woff?v0001` and named randomly.

首先打開副檔名為 `.css` 檔案，就會直接看到定義 `runes` 字型的 `font-face` 屬性，這是在 CSS3 提供的[新屬性](https://developer.mozilla.org/zh-TW/docs/Web/CSS/@font-face)，用來協助開發端可以提供字型給用戶呈現，而這個 `font-face` 也常常被拿來作為 CSS 字型編碼反爬蟲的方式。

**<p align="center">User-defined font-family font named runes location</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-font-face-custom-font-url.png?raw=true" width="640px">
</p>

從其中的 `url` 也可以看到該網站使用的字型格式種類，不過目前僅有[「網路開放字型格式」(Web Open Font Format)](https://zh.wikipedia.org/wiki/Web%E9%96%8B%E6%94%BE%E5%AD%97%E5%9E%8B%E6%A0%BC%E5%BC%8F)存在，對照 `webService/NET40/Runes/fonts/Books` 就是副檔名為 `.woff?v0001` 的字型檔。

不過通常這類命名像是亂碼的字型非常有可能是**每次請求自動產生**，也很有可能**每次字型檔的編碼內容都不同**，所以需要多次下載檔案，並且跟 HTML 來源的編碼再三確認，是否每次都不同。

接著複製該字型檔案的所在 URL 路徑並下載下來，嘗試解析該字型檔的內容，讓爬蟲程式可以透過下載的字型檔案，把抓取下來的在 HTML 上顯示的亂碼文字可以正常顯示。

<br/>

### 3. Download font file for analyzing

下載了字型檔案後，要開始解析字型的格式，因為這些字型都都會紀錄了不同的文字，以及這些文字要顯示的編碼。

所以前面從 HTML 抓取的文字雖然是亂碼，但是這些亂碼的編碼丟到字型檔案中時，亂碼的編碼可以對應到字型文字的編碼，就像查表翻譯一樣轉成可以正常顯示的文字。

這也是為何需要下載字型並先解析內容，透過程式來協助翻譯成正確的內容，因為爬蟲程式不是瀏覽器，所以要自己來做。

### 3.1 Analyze font content by FontCreator or FontDrop

接著聊到解析了， 這邊推薦如果是 Windows 系統，可以去安裝 **[FontCreator](https://www.linksoft.com.tw/product/fontcreator)** 這套軟體，並且透過這套軟體以視覺化的形式查看裡面的字型，與每個字型會有對應的 16 進制 Unicode 編碼，例如下圖：

**<p align="center">FontCreator 字型檢視範例</p>**
<p align="center">
  <img src="../master/Images/Font-Creator-Sample.png?raw=true" width="640px">
</p>

在上圖的範例並非該「數字求職網」，而是其他反爬蟲文章解說的[例子截圖](https://www.itread01.com/content/1547172845.html)，會看到字型 `左` 對應到 Unicode 的 `uniED8C` ，而這個 Unicode 就是需要編碼。另外 Unicode 的前綴字 `uni` 可以省略他主要是前面的即可。

不過在 MacOSX 上並不能使用 **FontCreator** 這套軟體，此時可以建議使用 **[FontDrop!](https://fontdrop.info/)**，這個字型檢視服務有著完整的檢視功能，只需要把字型檔匯入即可，如下圖，上傳剛剛從「數字求職網」下載的字型檔：

**<p align="center">FontDrop! 檢視字型</p>**
<p align="center">
  <img src="../master/Images/FontDrop-Sample-1-View-Fonts.png?raw=true" width="640px">
</p>

在上圖中會看到不同的字型，且每個字型皆有會顯示該 Unicode 編碼。接著點進去字型後便會看見更多內容：

**<p align="center">FontDrop! 檢視字型細節</p>**
<p align="center">
  <img src="../master/Images/FontDrop-Sample-2-View-Detail.png?raw=true" width="640px">
</p>

首先是 Unicode 的編碼變多了，為什麼？ 其實每個字型並非只有一個代表的 Unicode 對應碼，可以很多不同的編碼皆適用，只是都會有一個代表碼，而代表碼會是顯示第一個，例如這邊的例子 `(` 會是 `E19B`。

另外兩個比較重要的訊息分別是 **Index** 與 **Contours data**：

+ **Index** : 表示的是這個字型在字型表中的順序。
+ **Contours data** : 表示的是該字型的輪廓，會由不同座標來描繪

因為上述兩個參數，會隨著 CSS 反爬蟲的難度，而有不同的因素關鍵，幫助判別，後面的例子會提到，因此先記住便可。

### 3.2 Use fonttools of python package to read data 

上述分析後大致上知道原因，接著就用透過程式處理。安裝 Python 的 `fonttools` 套件，該套件可以讀取字型檔案的內容，安裝完後可以透過 `TTFont` 直接載入檔案路徑，或是二進制內容，並且先透過 `saveXML` 方法存成 XML 格式：

```python
import io
import requests
from fontTools.ttLib import TTFont

...

url = "Font 所在 URL 位置路徑"
resp = requests.get(url)

# 如果直接讀取檔案 => TTFont("Font字型檔案位置")
font = TTFont(io.BytesIO(resp.content))
font.saveXML("保存的路徑")
```

保存 XML 格式檔案的原因，是因為 `TTFont` 會根據字型字體的規範來解析與讀取，並且不同的字體會有不同的規範格式，例如 **[WOFF - Web Open Font Format](https://zh.wikipedia.org/wiki/Web%E9%96%8B%E6%94%BE%E5%AD%97%E5%9E%8B%E6%A0%BC%E5%BC%8F#cite_note-10)** 、 **[TTF - TrueType](https://zh.wikipedia.org/wiki/TrueType)** 與 **[EOT - Embedded OpenType](https://zh.wikipedia.org/wiki/%E5%B5%8C%E5%85%A5%E5%BC%8FOpenType)** 內部定義資料的屬性與標籤皆會不同。

因此雖然在前半段透過了 **FontCreator** 或 **FontDrop!** 讀取字型檔案並看見可視化的內容，但仍然需要了解字體內部的規範與定義，在使用 `fonttools` 提供的方法時，才能知道要呼叫的方法會對應什麼標籤、什麼資料值。所以當存成 XML 後便可以直接閱讀。

那麼接著來打開保存的 XML 格式字型檔來認識認識。

#### (1.) `GlyphOrder` and `GlyphID` tags - Font indexing and unicode mapping

**GlyphOrder** 與 **GlyphID** 標籤：會有序的紀錄該字型檔的所有字型。每個 **GlyphID** 標籤藉由 **索引 (Index)** 以及各自代表的 **Unicode** 編碼來代表字型。這也可以對照到前面的 **FontDrop!** 中的 **Index** 資訊，因此便可以透過該 **Index** 得知彼此在 **FontDrop!** 上所呈現的字型是什麼文字。

例如下圖中看一下索引為 `4` 的 Unicode 編碼為 `uniE19B`，而對照一開始的 **FontDrop!** 會是 `(` 。

**<p align="center">字型 XML 格式 - GlyphOrder 與 GlyphID 標籤</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-font-glyph-ids.png?raw=true" width="640px">
</p>

而在 Python 的 `fonttools` 中，可以透過呼叫 `getGlyphOrder` 方法來取得 `GlyphOrder` 標籤：

```python
# getGlyphOrder 會回傳陣列，該陣列會以 GlyphOrder 中的 GlyphID 索引為依序排列
orders: List[str] = font.getGlyphOrder()
```

**<p align="center">getGlyphOrder 方法顯示</p>**
<p align="center">
  <img src="../master/Images/python-font-getGlyphOrder.png?raw=true">
</p>


#### (2.) `TTGlyph` and `contour` tags - Font contours and coordinate 

**TTGlyph** 與 **contour** 標籤： **TTGlyph** 會紀錄 **GlyphID** 文字代表的 Unicode 編碼在字型檔中的「輪廓資訊」，包含該字型的最小最大 X, Y 寬高，以及由標籤 **contour** 所組成的「輪廓描繪座標」。

因為字型檔中的字型是透過輪廓描述並識別的，因此不會有任何標籤告知該字型是什麼「字」，而是只會紀錄該字的「輪廓」，只是透過軟體看得出是什麼文字而已。另外這些輪廓做標可以在 **FontDrop!** 中也能找到一樣的資訊。

例如上述的索引 `GlyphID` 標籤索引為 `4`，該 Unicode 為 `uniE19B`，透過 Unicode 為 `uniE19B `找到的輪廓數值與 **FontDrop!** 中的 `(` 會是一模一樣的輪廓座標。

**<p align="center">字型 XML 格式 - TTGlyph 與 contour 標籤</p>**
<p align="center">
  <img src="../master/Images/Anit-scraping-glyph-contours.png?raw=true" width="640px">
</p>

在 `fonttools` 中，可以透過 `get` 方法帶入 `glyf` 標籤值直接取出所有的 `TTGlyph` 標籤並尋找要的輪廓值，如下：

**<p align="center">字型 XML 格式 - TTGlyph 與 contour 標籤</p>**
<p align="center">
  <img src="../master/Images/python-get-glyph-coordinates.png?raw=true">
</p>


#### (3.) `cmap` and `map` tags  - Other unicode mapping

**cmap** 與 **map** 標籤：這兩個標籤紀錄了字型中每個字的其他 Unicode 編碼，例如這邊的 `uniE0AF`， 首先 `code` 屬性會看到同樣是同樣數值的 `0xe0af` (其中的 `0x` 可以忽略)，而這個 `code` 屬性表示了其他可以匹配的 Unicode 編碼。

**<p align="center">字型 XML 格式 - cmaps 與 cmap 標籤</p>**
<p align="center">
  <img src="../master/Images/Anit-scraping-cmaps.png?raw=true" width="640px">
</p>

再來尋找原先想要的例子 `uniE19B`，可以接著看到該字型 `(` 其他的 Unicode 編碼，如下圖中除了自己本身的 `code` 為 `0xe19b` 外，其他對應到 `uniE19B` 編碼的 `code` 包含了 `0xe20b` 與 `0xe248`，把這兩個 Unicode 編碼 `E20B` 與 `E248` 對照一下 **FontDrop!** 中便可以找到有一模一樣的數值。

**<p align="center">字型 XML 格式 - 其他的 Unicode 編碼</p>**
<p align="center">
  <img src="../master/Images/Anit-scraping-cmaps-other-unichar.png?raw=true" width="640px">
</p>

在 `fonttools` 中，可以透過呼叫 `getBestCamp` 方法來取得最佳的 `cmap` 標籤與資訊，因為字型檔案中有對應不同 platform 的版本 - `cmap_format_4` 與 `cmap_format_6`。

```python
# 回傳的會是字典格式
orders: Dict[str, str] = font.getBestCamp()
```

**<p align="center">getBestCamp 方法取得最佳的 cmap 資訊</p>**
<p align="center">
  <img src="../master/Images/python-font-getBestCamp.png?raw=true" width="640px">
</p>

如上圖在 `fonttools` 中會把 `code` 轉換成 10 進制的資料，因此原本的 `uniE19B` 的 `code` 為 `0xe19b` 便會轉換成 `57755`，所以在使用時，要近得處理進制轉換，看是要以十進制比對，還是把 `57755` 轉換成 `0xe19b` 比對。

到此這些就是在實作解析字型檔時，可以協助判斷的「標籤」與「屬性」，雖然也可以透過一些軟體，如 **FontCreator** 或 **FontDrop!** 以視覺化的方式快速分析字型檔，但是仍建議儲存成 XML 檔案來分析細節。

接下來就來回到一開始爬取下來的亂碼資料，透過先前所介紹的方式來解析與翻譯吧！

<br/>

### 4. 解析 HTML 源碼亂碼的編碼並分析翻譯

雖然在 HTML 源碼看到的亂碼，但那其實代表的只是因為該「編碼」魔有對應的文字而已，所以當抓下來貼到 Python 上時會看到該 Unicode 的編碼，如下圖：

**<p align="center">Python 3 顯示該 HTML 源碼字串編碼</p>**
<p align="center">
  <img src="../master/Images/python-show-unicode-encoding-way.png?raw=true">
</p>

不過因為 Python 3 的字串是 Unicode 格式，所以在 Python 中 `print` 顯示時會被自動轉換，也就看不到原來的編碼樣子。當然在做字串中的字元比對翻譯時也會照成影響，所們可以透過 `encode` 指定 `unicode-escape` 跳脫字元協助並轉換回 UTF8 編碼，這樣再對 `\\u` 做字串切割並依序匹配即可。

**<p align="center">藉由 unicode-escape 協助字元比對</p>**
<p align="center">
  <img src="../master/Images/python-unicode-escape.png?raw=true">
</p>

知道了如何分析與查看 HTML 亂碼後，再來就要驗證一開始的在[2.尋找 CSS 編碼反爬蟲的字型檔](./master/Chinese.md#2尋找-css-編碼反爬蟲的字型檔)中提到的是否每次請求的 HTML 亂碼編碼與字型檔皆不同，並且非常可惜的是沒有錯...每次都會改變編碼：

**<p align="center">再次請求後的 HTML 編碼</p>**
<p align="center">
  <img src="../master/Images/second-request-html.png?raw=true" width="640px">
</p>

**<p align="center">再次請求後的字型檔</p>**
<p align="center">
  <img src="../master/Images/second-request-font.png?raw=true" width="640px">
</p>

這也使翻爬蟲的麻煩度多了一些，但是好在不同的字型檔的索引順序與字型的輪廓ㄧ致，所以只要透過以下**五個步驟**便可以解決。

1. 每次 Request 請求時，同時取得字型檔案下載。
2. 爬取 HTML 內容比透過 `unicode-escape` 編碼處理，與字串切割取得每個編碼。
3. 把編碼轉換成 10 進制，透過 `fonttools` 字型套件的 `cmaps` 找出代表的編碼，比對原先切割好的 HTML 編碼做 10 進制轉換 `int("轉換的字串", 16)`。
4. 在透過代表的編碼找出 `GlyphOrder` 的索引
5. 建立一個索引與字型文字的字典匹配並轉換

當然這還算是容易的，如果每次請求下來的字型檔案內部的索引文字順序皆不同，那麼就要透過 `TTFGlyph` 的 `contour` 比對字型輪廓座標。

更複雜的，若是連每一次的輪廓座標也不同，那麼步驟五的建立索引與文字字典，就不能使用了，要改成 OCR 做辨認了..。

## Disclaimer
If there is anyone saw this repository, remind again, this program only for learning and researching how to crack anti-scraping, please **DO NOT use for commercial**. If someone used, I will not take this responsibility.

## License
The source code adopt **GNU General Public License v2.0**.

## Reference
1. [爬蟲之字型反爬（一）起點網](https://www.itread01.com/content/1544058306.html)
2. [Python：爬蟲例項 2：爬取貓眼電影——破解字型反爬](https://www.itread01.com/content/1542776590.html)
3. [爬蟲之字型反爬（三）汽車之家](https://www.itread01.com/content/1547172845.html)
4. [Python 爬蟲六：字型反爬處理（貓眼+汽車之家）-2018.10](https://www.itread01.com/content/1544669846.html)
5. [Python3 使用 unicode-escape 处理 unicode 16 进制字符串编解码问题](https://blog.csdn.net/chuatony/article/details/72628868)
6. [how do I .decode('string-escape') in Python3?](https://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python3)
7. [How do I convert hex to decimal in Python? [duplicate]](https://stackoverflow.com/questions/9210525/how-do-i-convert-hex-to-decimal-in-python)
