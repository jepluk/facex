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

x = Token('datr=g0VEZzg7dFHbuBgt4gu69MNE; sb=jUVEZxE7LpPcj-U0PFKDQ8HO; locale=id_ID; vpd=v1%3B609x320x1.8210935592651367; ps_l=1; ps_n=1; m_pixel_ratio=1; wd=395x753; c_user=100025676432150; fr=0Ga13XfNnKQh7HYqQ.AWWaxWpWySaykfXQqHwQukxP0UE.BnREWD..AAA.0.0.BnRFBr.AWUFqMpoZTE; xs=30%3A1NlxyDm0oEenaQ%3A2%3A1732530283%3A-1%3A11219; fbl_st=100623212%3BT%3A28875504; wl_cbv=v2%3Bclient_version%3A2681%3Btimestamp%3A1732530284')
print(x.adsmanager())
print(x.oauth())
