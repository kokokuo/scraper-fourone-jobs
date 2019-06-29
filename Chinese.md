# 1111jobs-cracker
**1111jobs-cracker** 是破解某[數字求職網站](https://1111.com.tw)徵才頁中的應徵資料的爬蟲程式，該程式僅為學習研究使用，並專注在破解反爬蟲的部分，請勿使用程式在商業用途。起初會寫該專案，是因在 Python Taiwan 看見有人詢問，所以才想要嘗試撰寫。另外該專案是在 **2019.06.28** 撰寫開發，未來可能因該數字求職網改變反爬蟲方式而失效。

**<p align="center">「數字求職網」欲爬取的資料與 HTML 源碼</p>**
<p align="center">
  <img src="../master/Images/Anti-scraping-1111jobs-apply-contents.png?raw=true" width="640px">
</p>

## 解析反爬蟲策略
在該程式中的所要擷取的資料來源是徵才頁面[乙級-職業安全衛生管理員(兼職可)](https://www.1111.com.tw/job/85992852/?agent=sticktop_51563220_85992852) 中的應徵資料，而在該應徵資料中的 **信箱**、**市話** 與 **手機**，若透過正常的爬蟲解析方式如 XPath 是無法抓取下來，而會出現意義不明的編碼，透過 HTML 源碼查看確實如此，如下圖：

在反爬蟲中，對於顯示資料正常，但 HTML 源碼為亂碼的狀態，通常屬於 JavaScript 加載或是 CSS 的樣式字型編碼的類型，

