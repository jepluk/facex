# -*- coding: utf-8 -*-
import re, sqlite3, sys, requests
from .db import open

class Token:
    def __init__(self, cookie: str) -> None:
        self.ses = requests.session()
        self.ses.cookies['cookie'] = cookie

    def adsmanager(self) -> str:
        from .cli import DB_NAME
        source = self.ses.get('https://www.facebook.com/adsmanager/manage/campaigns').text
        redirect = self.ses.get(re.search(r'\.replace\("(.*?)"\)', source).group(1).replace('\\', '')).text

        try:
            token = re.search('"(EAAB.*?)";', redirect).group(1)
            with sqlite3.connect(DB_NAME) as db:
                c__ = db.cursor()
                try:
                    c__.execute('DELETE FROM user')
                    c__.execute('INSERT INTO user (cookie, token) VALUES (?,?)', (self.ses.cookies.get_dict()['cookie'], token))
                    db.commit()
                except sqlite3.OperationalError:
                    open()

            print(f'\n[ INFO! ] Fetch token successfull.')
        except AttributeError:
            with sqlite3.connect(DB_NAME) as db:
                try:
                    db.cursor().execute('DELETE FROM user')
                    db.commit()
                except sqlite3.OperationalError:
                    open()

            exit('\n[ WARN! ] Faillure fetch token.')


