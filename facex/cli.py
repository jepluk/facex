import argparse, sqlite3
from . import config, scrape_token, Facex

def main():
    arg = argparse.ArgumentParser(description='Beautiful Facebook Bruteforce Attack.')
    sub = arg.add_subparsers(title='command', dest='command', required=True)

    useragent = sub.add_parser('set', help='Setup')
    useragent.add_argument('-ua', '--useragents', help='Set useragents to the database for Bruteforce Attack. set None for use random')
    useragent.add_argument('-c', '--cookie', help='Set cookie and tokeb to the database.')

    dump = sub.add_parser('dump', help='Dump id and name from friendlist.')
    dump.add_argument('-t', '--target', type=str, help='Set target for dump <-t <1000xxxxx>>')
    #dump.add_argument('-l', '--limit', type=int, help='Set limit for dump <-l <5000>>')

    parse = arg.parse_args()
    match parse.command:
        case 'set':
            if parse.useragents:
                with sqlite3.connect(config.DB_PATH) as db:
                    cursor = db.cursor()
                    cursor.execute('DELETE FROM useragents')
                    cursor.execute('INSERT INTO useragents (ua) VALUES (?)', (parse.useragents,))

                    db.commit()

                print('\n[ INFO! ] Successfull set useragents.\nValue: '+ str(parse.useragents))

            if parse.cookie:
                with sqlite3.connect(config.DB_PATH) as db:
                    cursor = db.cursor()
                    cursor.execute('DELETE FROM user')
                    
                    token_out = scrape_token.Scrape(cookie=parse.cookie).oauth()
                    if 'EAAB' in str(token_out):
                        print(f'\n[ INFO! ] Successfull set cookie and token!\nCookie: {parse.cookie}\nToken: {token_out}')
                        cursor.execute('INSERT INTO user (cookie, token) VALUES (?,?)', (parse.cookie, token_out))
                    else:
                        print(f'\n[ WARN! ] Faillure setup cookie and token.\nPlease use another cookie.')

                    db.commit()

        case 'dump':
            obj = Facex()
            after = [obj.dump_friends(parse.target)]
            for i in after:
                try:
                    after.append(obj.dump_friends(parse.target, i))
                except Exceptiona as e:
                    print('[ WARN! ] '+ str(e))
                    break
            

