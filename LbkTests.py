#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

import LabBook

from datetime import date
from datetime import datetime
from datetime import timedelta

from LbkIO import LbkIO
from LbkIO import Opt

from LbkExceptions import IODateExcept

# test str2date [LbkIO] ====================================================== #

def test_LbkIO_str2date():
    """test str2date parsing function"""

    # initialization
    lbkIO = LbkIO()
    today = datetime.today().date()
    year = today.year
    oneDay = timedelta(days=1)
    yesterday = today - oneDay
    tomorrow = today + oneDay

    # tests
    tests = [
        {"str": "today",        "ref": today,            'res': True},
        {"str": "yesterday",    "ref": yesterday,        'res': True},
        {"str": "tomorrow",     "ref": tomorrow,         'res': True},
        {"str": "",             "ref": date(2016, 3, 2), 'res': False},
        {"str": "foo",          "ref": tomorrow,         'res': False},
        {"str": "2/3/2016",     "ref": date(2016, 3, 2), 'res': True},
        {"str": "2/03/2016",    "ref": date(2016, 3, 2), 'res': True},
        {"str": "02/3/2016",    "ref": date(2016, 3, 2), 'res': True},
        {"str": "02/03/2016",   "ref": date(2016, 3, 2), 'res': True},
        {"str": "2/3/16",       "ref": date(2016, 3, 2), 'res': True},
        {"str": "2/03/16",      "ref": date(2016, 3, 2), 'res': True},
        {"str": "02/3/16",      "ref": date(2016, 3, 2), 'res': True},
        {"str": "02/03/16",     "ref": date(2016, 3, 2), 'res': True},
        {"str": "2/3",          "ref": date(year, 3, 2), 'res': True},
        {"str": "2/03",         "ref": date(year, 3, 2), 'res': True},
        {"str": "02/3",         "ref": date(year, 3, 2), 'res': True},
        {"str": "02/03",        "ref": date(year, 3, 2), 'res': True},
        {"str": "2/3",          "ref": date(year, 3, 2), 'res': True},
        {"str": "2/03",         "ref": date(year, 3, 2), 'res': True},
        {"str": "02/3",         "ref": date(year, 3, 2), 'res': True},
        {"str": "02/03",        "ref": date(year, 3, 2), 'res': True},
        {"str": "02-03-2016",   "ref": date(2016, 3, 2), 'res': True},
        {"str": "02:03:2016",   "ref": date(2016, 3, 2), 'res': True},
        {"str": "02.03.2016",   "ref": date(2016, 3, 2), 'res': True},
        {"str": "0203",         "ref": date(year, 3, 2), 'res': True},
        {"str": "020316",       "ref": date(2016, 3, 2), 'res': True},
        {"str": "02032016",     "ref": date(2016, 3, 2), 'res': True},
        {"str": "020320166",    "ref": date(2016, 3, 2), 'res': False},
        {"str": "2032016",      "ref": date(2016, 3, 2), 'res': False},
        {"str": "23216",        "ref": date(2016, 3, 2), 'res': False},
        {"str": "216",          "ref": date(2016, 3, 2), 'res': False},
        {"str": "26",           "ref": date(2016, 3, 2), 'res': False},
        {"str": "2",            "ref": date(2016, 3, 2), 'res': False},
    ]

    # running tests
    print("[LbkIO] str2date test ...... ", end='')
    for test in tests:

        if test['res'] :
            
            try:
                res = lbkIO.str2date(test['str'])
                assert( res == test['ref'] )

            except Exception :

                print()
                print("\""+test['str']+"\" input should provide \"", end="")
                print(LbkIO.date2str(test['ref']) + "\" result, ", end="")
                print("got \"", end="");print(res, end="");print("\" instead.")
                print("test [LbkIO, str2date] failed. exit.")
                sys.exit(os.EX_DATAERR)

        else :

            try:
                res = lbkIO.str2date(test['str'])
                assert(False)

            except IODateExcept :

                pass

            except Exception :

                print()
                print("\""+test['str']+"\" should have risen an IODateExcept.")
                print("test [LbkIO, str2date] failed. exit.")
                sys.exit(os.EX_DATAERR)

    print("ok")

# test LabBook [LabBook] ===================================================== #

def test_LabBook():
    """test process"""

    LabBook.main(["init"])
    LabBook.main(["-s", "20/10/15", "-e", "22/10/15", "new"])
    LabBook.main(["renew"])
    LabBook.main(["-d", "21/10/15", "make"])
    LabBook.main(["remake"])

# Main test function ========================================================= #

def tests(startDate, endDate):
    """embedded all available tests"""

    assert(startDate == None and endDate == None)

    test_LbkIO_str2date()
    test_LabBook()

if __name__ == "__main__":
   
    tests(None, None)
    sys.exit(os.EX_OK)


   
