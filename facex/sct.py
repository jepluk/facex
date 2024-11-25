# -*- coding: utf-8 -*-
import re, sqlite3, sys, requests
from .config import DB_PATH

class Token:
    def __init__(self, cookie: str) -> None:
        self.ses = requests.session()
        self.ses.cookies['cookie'] = cookie

    def adsmanager(self) -> str:
        source = self.ses.get('https://www.facebook.com/adsmanager/manage/campaigns').text
        redirect = self.ses.get(re.search(r'\.replace\("(.*?)"\)', source).group(1).replace('\\', '')).text

        try:
            token = re.search('"(EAAB.*?)";', redirect).group(1)
            with sqlite3.connect(DB_PATH) as db:
                c__ = db.cursor()
                c__.execute('DELETE FROM user')
                c__.execute('INSERT INTO user (cookie, token) VALUES (?,?)', (self.ses.cookies.get_dict()['cookie'], token))
                db.commit()

            print(f'\n[ INFO! ] Fetch token successfull.')
        except AttributeError:
            with sqlite3.connect(DB_PATH) as db:
                db.cursor().execute('DELETE FROM user')
                db.commit()

            exit('\n[ WARN! ] Faillure fetch token.')


