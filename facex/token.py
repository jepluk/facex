import requests
import re

class Scrape:
    def __init__(self, cookie: str=None, session: object=None) -> None:
        self.ses = session if session else requests.session()
        self.ses.cookies.update({'cookie': cookie}) if cookie is not None else None 

    def oauth(self) -> (str, bool):
        hdx = str(self.ses.get('https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey', headers={'Accept-Language': 'id,en;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36','Referer': 'https://www.instagram.com/','Host': 'www.facebook.com','Sec-Fetch-Mode': 'cors','Accept': '*/*','Connection': 'keep-alive','Sec-Fetch-Site': 'cross-site','Sec-Fetch-Dest': 'empty','Origin': 'https://www.instagram.com','Accept-Encoding': 'gzip, deflate'}).headers)

        if 'EAAB' in hdx:
            return re.search(r'"(EAAB.*?)",', hdx).group(1)






