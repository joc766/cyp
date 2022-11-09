#!/usr/bin/env python

#-----------------------------------------------------------------------
# create.py
# Author: Bob Dondero
# Modified for local use by Alan Weide (c) 2022
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from contextlib import closing
from sqlite3 import connect
import os

from create_sql_script import main as create_instructions

#-----------------------------------------------------------------------

DB_SCRIPT = "./createdb.sql"
DB_FILE = '../buildings.sqlite'
DATABASE_URL = f'file:{DB_FILE}?mode=rwc'

def main():

    if len(argv) != 1:
        print('Usage: python create.py', file=stderr)
        exit(1)

    try:
        if not os.path.exists(DB_SCRIPT):
            create_instructions()

        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:

            with closing(connection.cursor()) as cursor:

                # Use double quotes to delimit Python strings
                # because SQL statements use single quotes.

                #-------------------------------------------------------

                with open(DB_SCRIPT) as script:
                    cursor.executescript(script.read())

                #-------------------------------------------------------

    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
