# scraper-fourone-jobs
**scraper-fourone-jobs** 是破解某 [數字求職網站](https://1111.com.tw) 徵才頁中的應徵資料的爬蟲程式，該程式僅為學習研究使用，並專注在破解反爬蟲的部分，請勿使用程式在商業用途。

會有該專案的原理，起初是因在 Python Taiwan 看見有人詢問如何抓取並突破反爬蟲，在回答對方的過程中，認為還是要自己寫一次才能找出所有原因，畢竟反爬蟲的方式有許多種，每一種也有變形，所以才會動手開發與破解該網站的反爬蟲。

另外因該專案是在 **2019.06.28** 撰寫開發並完成，因此未來可能因該「數字求職網」改變反爬蟲的方法而導致此程式失效，若發現失效歡迎發 Pull Request 或是開 Issue 清單，感謝。

**<p align="center">「數字求職網」欲爬取的資料與 HTML 源碼</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-fourone-jobs-apply-contents.png?raw=true" width="640px">
</p>

## 破解反爬蟲過程

在該程式中的所要擷取的資料來源是徵才頁面[乙級-職業安全衛生管理員(兼職可)](https://www.1111.com.tw/job/85992852/?agent=sticktop_51563220_85992852) 中的應徵資料，而在該應徵資料中的 **信箱**、**市話** 與 **手機**，若透過正常的爬蟲解析方式如 XPath 是無法抓取下來，而會出現意義不明的編碼，透過 HTML 源碼查看確實如此，如下圖：

**<p align="center">HTML 源碼文字</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-css-font-class-style.png?raw=true" width="640px">
</p>


**備註** ： 以下開始介紹該「數字求職網站」的分析與破解反爬蟲過程，因為過程可以會對該網站造成營業損失，所以不會全部公開細節與過程，且該源碼會採用 **GNU General Public License v2.0**。


### 1. 分析反爬蟲類型

在反爬蟲中，對於顯示資料正常，但 HTML 源碼為亂碼的狀態，通常屬於 JavaScript 加載或是 CSS 的樣式字型編碼的類型，因此通過尋找，我們先發現 CSS 樣式 Class `txticon`，並且循著來源發現了一個自定義 `font-family` 數值 `'runes'`：

**<p align="center">txticon 的 CSS 定義</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-css-font-family-and-font-file.png?raw=true" width="640px">
</p>

### 2.尋找 CSS 編碼反爬蟲的字型檔

因為 `font-family`提供的字型來源是自定義的，那麼一定需要夾帶著該檔案才能正常顯示文字。因此接著我們繼續尋找，便會發現一個路徑為 `webService/NET40/Runes/fonts/Books`的目錄，並且底下有兩個檔案，皆是看似亂碼的名稱與兩個不同的副檔名  `.css` 與 `.woff?v0001`。

首先打開副檔名為 `.css` 檔案，就會直接看到定義 `runes` 字型的 `font-face` 屬性，這是在 CSS3 提供的[新屬性](https://developer.mozilla.org/zh-TW/docs/Web/CSS/@font-face)，用來協助開發端可以提供字型給用戶呈現，而這個 `font-face` 也常常被拿來作為 CSS 字型編碼反爬蟲的方式。

**<p align="center">txticon 的 CSS 定義</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-font-face-custom-font-url.png?raw=true" width="640px">
</p>

從其中的 `url` 也可以看到該網站使用的字型格式種類，不過目前僅有「網路開放字型格式」(Web Open Font Format) 存在，對照
`webService/NET40/Runes/fonts/Books` 就是副檔名為 `.woff?v0001` 的字型檔。
