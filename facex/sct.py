# -*- coding: utf-8 -*-
import re, sqlite3, sys, requests

class Token:
    def __init__(self, cookie: str) -> None:
        self.ses = requests.session()
        self.ses.cookies['cookie'] = cookie

    def adsmanager(self) -> str:
        source = self.ses.get('https://www.facebook.com/adsmanager/manage/campaigns').text
        redirect = self.ses.get(re.search(r'\.replace\("(.*?)"\)', source).group(1).replace('\\', '')).text

        return re.search('"(EAAB.*?)";', redirect).group(1)

    def oauth(self) -> str:
        get = self.ses.get('https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey', headers={
            'Accept-Language': 'id,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Referer': 'https://www.instagram.com/',
            'Host': 'www.facebook.com',
            'Sec-Fetch-Mode': 'cors',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Dest': 'empty',
            'Origin': 'https://www.instagram.com',
            'Accept-Encoding': 'gzip, deflate',
        })
        print(get.headers)
        
        if 'EAAB' in str(get.headers):
            token = re.search(r'"(EAAB.*?)",', str(get.headers)).group(1)
            with sqlite3.connect('/sdcard/database.db') as db:
                cursor = db.cursor()
                cursor.execute('SELECT * FROM user')
                data = cursor.fetchone()

                cursor.execute('UPDATE user SET token=? WHERE cookie=?', (token, data[0]))
                db.commit()

            return token
        else:
            with sqlite3.connect('/sdcard/database.db') as db:
                db.cursor().execute('DELETE FROM user')
                db.commit()

            sys.exit('\n[ WARN! ] Cookie Error!\n[ INFO! ] Please use old accounts for login.\n[ WARN! ] Please set cookie again. facez --cookie "cookie string"')

