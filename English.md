# scraper-fourone-jobs

## Translation Assistance Need you 🙏🙏🙏
You're welcome to come to this repository. If you like the repository, hope you could give me a Star. If you are interested, the current English translation is in progress. Really welcome the **fork** project and assist to translate and send PR :)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) [![Python 3.7.1](https://img.shields.io/badge/Python-3.7.1-blue.svg)](https://www.python.org/downloads/release/python-371/)

<p align="center">
  <img src="../master/Images/Program-Result.png?raw=true" width="640px">
</p>

scraper-fourone-jobs is a anti-scraping cracker for extracting apply information of one of Taiwan famous jobs recruiting website, this program **only for learning and researching how to crack anti-scraping, please DO NOT use for commercial**.

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

The program which would like to scrape and extract data is from the recruitment page and the data "email", "telephone" and "mobile" could not scrape from correct way like XPATH, it's will show unmeaningful data and encoding, here is the HTML page source as below.

**<p align="center">HTML Page Source Content</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-css-font-class-style.png?raw=true" width="640px">
</p>

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

First, open the file which the extension is `.css` and you will see the `font-face` attribute and the user-defined value `runes`. The `font-face` is CSS3 new property and it could assist the developer providing more types of fonts to users, but the more interesting usuage is that `font-face` was used for anti-scraping protection.


**<p align="center">User-defined font-family font named runes location</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-font-face-custom-font-url.png?raw=true" width="640px">
</p>

And the attribute `url` could discover which font format was used, but only find [(Web Open Font Format)](https://zh.wikipedia.org/wiki/Web%E9%96%8B%E6%94%BE%E5%AD%97%E5%9E%8B%E6%A0%BC%E5%BC%8F), and mapped the file of directory `webService/NET40/Runes/fonts/Books`, the font extension is `.woff?v0001`.

But the file name looks like **automatically and randomly generated**,  the encoding of font content also could be different, so I have to download the file more times and check the HTML scraping source font of encoding again for checking the encoding is different or not.

Then copy the font file URL path and download it for tring to analyze the content of font. After we know the rule,  we could build a scraper process to automatically download file and parse garbled words, then map word to the encoding for translation to correct contents.


<br/>

### 3. Download font file for analyzing

After downloading the font files, then start to analyze the content of font, because the font record different character and the encoding for translating to show character.

Although the words are garbled when we parsed them from HTML, but if we put the garbled words into font file, then the font file will figure out these character of garbled words and map to translate correct character.

This is reason why we need to download the font file first. But the problem is the scraping process not a browser, so we need to make more effort to analyze and parse it by ourself.

### 3.1 Analyze font content by FontCreator or FontDrop

After we know the reason, then we start to talk about analysing, if the people use the Windows operation, then suggest to install the software called **[FontCreator](https://www.linksoft.com.tw/product/fontcreator)**. The software could assist us to understand th contents of font file and visualizing the contents, like we could see the 16 bit Unicode each font.

**<p align="center">FontCreator Viewer Sample</p>**
<p align="center">
  <img src="../master/Images/Font-Creator-Sample.png?raw=true" width="640px">
</p>

The above image sample are not from "jobs recruiting website", it's another [anti-scraping tutorial sample](https://www.itread01.com/content/1547172845.html). We'll see the font `左` map to the unicode encoding `uniED8C`. (The prefix `uni` we could omit it)

But we could use the **FontCreator** software on a MacOS, so I recommend to use the website service called **[FontDrop!](https://fontdrop.info/)**. **[FontDrop!](https://fontdrop.info/)** has the powerful functions on viewer, we just need to import font file, now upload the font file downloaded from "jobs recruiting website":

**<p align="center">FontDrop! Viewer</p>**
<p align="center">
  <img src="../master/Images/FontDrop-Sample-1-View-Fonts.png?raw=true" width="640px">
</p>

We'll see the different fonts on the above image and all of the font map to one unicode encoding, we could click the font to see the detail information:

**<p align="center">FontDrop! Detail Font Viewer</p>**
<p align="center">
  <img src="../master/Images/FontDrop-Sample-2-View-Detail.png?raw=true" width="640px">
</p>

First thing is why there are many unicode encoding? Acutually not only one unicode encoding map to one character in the font file, but each font have a main unicode encoding, like the sample `(` map to `E19B` encoding.

The other two important information is **Index** and **Contours data** :

+ **Index** : Means the order of the font list.
+ **Contours data** : Means the contours of the font and will represent by coordinates to draw.

The above two arguments are the keypoint for assisting check the font if CSS anti-scraping difficulty increase, and we'll talk later.


### 3.2 Use fonttools of python package to read data 

After we know the reason, we could write a program to do it automatically. Install the Python package called `fonttools`. The package could get the content from font file through reading file path or binary content with `TTFont` and then saved to XML format with `saveXML`: 

```python
import io
import requests
from fontTools.ttLib import TTFont

...

url = "The URL path of font file "
resp = requests.get(url)

# If read the font file directly => TTFont("Font file path")
font = TTFont(io.BytesIO(resp.content))
font.saveXML("saved file path")
```


The reason for saving to XML format file is that it's still hard to read the right data from `fonttools` even although we know the content of font by visualizing from **FontCreator** and **FontDrop!** tools before. 

Because we could not know which methods could find the data we want. and that why we need to save to XML file format first and then call the right method by mapping to the content in the XML.

Here, `TTFont` could analyze and parse content from font according to different font format. Each font format has different specification to to recording encoding font, like **[WOFF - Web Open Font Format](https://zh.wikipedia.org/wiki/Web%E9%96%8B%E6%94%BE%E5%AD%97%E5%9E%8B%E6%A0%BC%E5%BC%8F#cite_note-10)**, **[TTF - TrueType](https://zh.wikipedia.org/wiki/TrueType)** and **[EOT - Embedded OpenType](https://zh.wikipedia.org/wiki/%E5%B5%8C%E5%85%A5%E5%BC%8FOpenType)** and record encoding and description of font with different tags and attributes.


Okay, let's open the saved font file of XML format to analyze the contents.


#### (1.) `GlyphOrder` and `GlyphID` tags - Font indexing and unicode mapping

**GlyphOrder** and **GlyphID** tags：These two tags could record the all different fonts orderly.
Each tags of **GlyphID** describe the font through **Unicode** and **Index** attribute. The information is the same information as **Index** int the **FontDrop!**, so we could know every font meaning through the visualization in the **FontDrop!**.

Here is a sample that shows the index `4` have a attribute Unicode is `uniE19B` and after we checking the **FontDrop!** website, we could know the meaning of font is `(`


**<p align="center">XML Font format - GlyphOrder and GlyphID tags</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-font-glyph-ids.png?raw=true" width="640px">
</p>

Now, we could call the `getGlyphOrder` method to get the contents of `GlyphOrder` tags by using `fonttools` package :

```python
# The getGlyphOrder method will return array and the array will show the data orderly according to the index attribue of GlyphID tag in the GlyphOrder parent tag.
orders: List[str] = font.getGlyphOrder()
```

**<p align="center">The data after calling the getGlyphOrder method</p>**
<p align="center">
  <img src="../master/Images/python-font-getGlyphOrder.png?raw=true">
</p>


#### (2.) `TTGlyph` and `contour` tags - Font contours and coordinate 

**TTGlyph** and **contour** tags： **TTGlyph** could record the contour information which mapping to unicode encoding in the **GlyphID**. The information about  contour include the minimum and maximun width of X coordniate, height of Y coordniate width and contour coordinate in **contour** tag.

Because the fonts in the font file are described and identified by the contour, there won't be any tags telling the word what the word is. It only record the 「Contour」of the word, but we could understand what the text is by using software like **FontDrop!**, **[FontCreator]** ..so on and we could also find the contour coordinate in these software.

for example, the previous information shows the tag index of `GlyphID` is `4` and the Unicode is `uniE19B` , so we could find the contour information by encoding number `uniE19B`. Here you could see the contour coordinate is the same as the font `(` in the **FontDrop!**.

**<p align="center">XML Font format - TTGlyph and contour tags</p>**
<p align="center">
  <img src="../master/Images/Anit-scraping-glyph-contours.png?raw=true" width="640px">
</p>

In `fonttools` library, we could get all `TTGlyph` tags and find the contour information through call `get` method and set the `glyf` tag value :

**<p align="center">XML Font format - How to get the information of TTGlyph and contour tags</p>**
<p align="center">
  <img src="../master/Images/python-get-glyph-coordinates.png?raw=true">
</p>

#### (3.) `cmap` and `map` tags  - Other unicode mapping

**cmap** and **map** tags：這兩個標籤紀錄了字型中每個字的其他 Unicode 編碼，例如這邊的 `uniE0AF`， 首先 `code` 屬性會看到同樣是同樣數值的 `0xe0af` (其中的 `0x` 可以忽略)，而這個 `code` 屬性表示了其他可以匹配的 Unicode 編碼。

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
