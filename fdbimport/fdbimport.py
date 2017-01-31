#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fdb import
"""

import os
import sys
import argparse
import logging
from openpyxl import load_workbook
import fdb


# ......................................................................................................................
class FdbImport(object):
    """
    Class to Import xlsx file
    """

    def __init__(self, file: str = ''):
        self.file = file
        self.wb = None
        self.con = None
        self.outFile = None
        self.cinfo = dict(host='', port=3050, database = 'c:/restomax/data.gdb', user='', password='')

    # ..................................................................................................................
    @staticmethod
    def printTitle(title: str) -> None:
        print(title)
        print('-' * 1 * (len(title)))

    # ..................................................................................................................
    def loadFile(self, file: str) -> bool:
        self.printTitle('Load File '+file)
        self.file = os.path.realpath(file)
        if not os.path.isfile(self.file):
            print('** Error: File %s not found!' % self.file, file=sys.stderr)
            exit(-1)
        self.wb = load_workbook(filename=self.file, read_only=True)
        print('.. OK Loaded')
        return True

    # ..................................................................................................................
    def scanFile(self) -> bool:
        try:
            ws = self.wb.active
            # ws = self.wb['big_data']
            for row in ws.rows:
                line = 'Insert Into () Values ('
                for cell in row:
                    line += ','+str(cell.value)
                line += '\n'
                self.outFile.write(line)
            return True
        except Exception as ex:
            print('** '+str(ex))
            return False

    # ..................................................................................................................
    def openOut(self, out: str) -> bool:
        try:
            # https: // docs.python.org / 3 / library / csv.html?highlight = csv
            # import csv
            # with open('eggs.csv', 'w', newline='') as csvfile:
            #     spamwriter = csv.writer(csvfile, delimiter=',',
            #                             quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            #     # spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            #     spamwriter.writerow(['Spam', 5, 'Lovely Spam', 'Wonderful Spam'])

            # google python 3 load dico from text file
            # import json
            # # echo {\"two\": 2, \"one\": 1} > eggs.csv
            # d2 = json.load(open("eggs.csv"))
            # print(d2)
            # print(d2['one'])
            # print(d2['two'])

            logging.info(out)
            self.outFile = open(out, mode='w', encoding = 'utf8')
            return True
        except Exception as ex:
            self.outFile = None
            print('** '+str(ex))
            return False

    # ..................................................................................................................
    def fdbConnect(self) -> bool:
        try:
            self.printTitle('Connect to DB '+self.cinfo['host']+self.cinfo['database'])
            self.con = fdb.connect(**self.cinfo)
            print('.. OK Connected')
            cur = self.con.cursor()
            cur.execute("Select MAJORVERSION,MINORVERSION from DUAL")
            for (major, minor) in cur:
                print('.. DB Version %s.%s' % (major, minor))
            return True
        except Exception as ex:
            print('** '+str(ex))
            return False


# ......................................................................................................................
def main():
    logging.getLogger().setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
        prog="fdbimport.py",
        description=__doc__,
        epilog="\nbe carefull and good lock !\n",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35)
        )
    parser.add_argument('-f', '--file', type=str, default='/home/cdc/Tempo/tempo.xlsx', help='File to process')
    parser.add_argument('-o', '--out', type=str, default='/home/cdc/PycharmProjects/fdb-import/tempo.sql', help='Output script')
    parser.add_argument('-u', '--user', type=str, default=os.getenv("isc_user", "PNA"), help='FDB User (def=isc_user)')
    parser.add_argument('-p', '--pwd', type=str, default=os.getenv("isc_password", "1"), help='FDB Password (def=isc_password)')
    parser.add_argument('-d', '--dbn', type=str, default=os.getenv("isc_database", "1"), help='FDB Database name (def=isc_database)')
    parser.add_argument( '--dbh', type=str, default=os.getenv("isc_host",'localhost'), help='FDB Host name (def=isc_host)')
    parser.add_argument( '--port', type=int, default=3050, help='FDB Port')
    args = parser.parse_args()
    logging.info(str(args))

    fdbimport = FdbImport()
    fdbimport.cinfo['user']=args.user
    fdbimport.cinfo['password']=args.pwd
    fdbimport.cinfo['database']=args.dbn
    fdbimport.cinfo['host']=args.dbh
    fdbimport.cinfo['port']=args.port
    if not fdbimport.loadFile(args.file):
        exit(-1)
    if not fdbimport.openOut(args.out):
        exit(-1)
    if not fdbimport.fdbConnect():
        exit(-1)
    if not fdbimport.scanFile():
        exit(-1)

if __name__ == "__main__":
    main()
