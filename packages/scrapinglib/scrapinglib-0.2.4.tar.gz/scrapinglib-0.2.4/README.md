# scrapinglib



## 使用:

```
from scrapinglib import search

proxydict = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080"
}
# search tmdb id 14534
data = search('14534', 'tmdb', type='general', proxies=proxydict)

```
