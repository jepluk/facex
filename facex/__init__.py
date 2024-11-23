import requests
import re, json, sqlite3
from . import config

class Facex:
    def __init__(self) -> None:
        self.ses = requests.session()

        with sqlite3.connect(config.DB_PATH) as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM user')
            data = cursor.fetchone()

            self.ses.cookies['cookie'] = data[0]
            self.token = data[1]

    def dump_friends(self, id: str, after: str=None) -> None:
        api = DynamicObject(self.ses.get('https://graph.facebook.com/'+ str(id), params={'access_token': self.token, 'fields': 'name,friends.fields(id, name)' +(f'.after({after})' if after else '')}).json())
        
        if api.friends.data:
            with sqlite3.connect(config.DB_PATH) as db:
                for i in api.friends.data:
                    try:
                        print(f'[ ACCEPT! ] ID: {i.id}, Name: {i.name} save to the database.')
                        db.cursor().execute('INSERT INTO dump (id, name) VALUES (?,?)', (i.id, i.name))
                        db.commit()
                    except sqlite3.IntegrityError:
                        print(f'[ SKIP! ] {i.id} Aleready exists in database.')

        else:
            print('[ WARN! ] Error, please check target or cookie.')

