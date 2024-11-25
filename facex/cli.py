#!/usr/bin/env python3
import argparse, os, sys, sqlite3
from . import Facebook

DB_DIR = os.path.expanduser('~/.facex')
DB_NAME = os.path.join(DB_DIR, 'database.db')

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
    action = parser.add_subparserd(title='Action', dest='Action', required=True)

    dump = action.add_parser('dump')
    dump.add_argument('-t', '--target', help='Facebook id for get list friends.')

    run = action.add_parser('run')

    pars = parser.parse_args()
    match pars:
        case 'dump':
            Facebook().dump_friendlist(id=str(pars.target))

        case 'run':
            Facebook().crack()




if __name__ == "__main__":
    main()
