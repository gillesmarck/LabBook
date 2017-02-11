#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum, unique

import io
import json
import os
import shutil
import datetime
import pprint

from LbkExceptions import IODateExcept
from LbkExceptions import IODatesExcept

from LbkExceptions import IOInitExcept
from LbkExceptions import IOCleanExcept
from LbkExceptions import IONewExcept
from LbkExceptions import IORenewExcept
from LbkExceptions import IOMakeExcept
from LbkExceptions import IORemakeExcept
from LbkExceptions import IOTestExcept

@unique
class Mode(Enum):
    """enumeration for input argument"""

    init   = 0
    clean  = 1
    make   = 2
    remake = 3
    new    = 4
    renew  = 5
    test   = 6

@unique
class Opt(Enum):
    """enumeration for input option"""

    date   = 0
    start  = 1
    end    = 2

class LbkIO:
    """input/output data management"""

    def __init__(self):
        """LbkIO class constructor"""

        # version
        self.version = [1,0,1]

        # converting option
        self.oneDay = datetime.timedelta(days=1)

    def getChecker(self, mode):
        """get function linked to mode enumeration"""
        
        checker = {
            Mode.init  : self.init,
            Mode.clean : self.clean,
            Mode.make  : self.make,
            Mode.remake: self.remake,
            Mode.new   : self.new,
            Mode.renew : self.renew,
            Mode.test  : self.test,
        }
        return checker.get(mode);

    def usage(self):
        """define usage for LabBook app"""

        print("usage: labbook [-h | --help] [-d | --date <date>]")
        print("               [-s | --start <date>] [-e | --end <date>] <command>")

    def help(self):
        """define help for LabBook app"""
        
        self.usage()
        print(2*os.linesep, end="")
        print("These are common LabBook commands used in various situations:")
        
        print(2*os.linesep, end="")
        IOInitExcept.help()
        
        print(2*os.linesep, end="")
        IOCleanExcept.help()

        print(2*os.linesep, end="")
        IONewExcept.help()

        print(2*os.linesep, end="")
        IORenewExcept.help()

        print(2*os.linesep, end="")
        IOMakeExcept.help()

        print(2*os.linesep, end="")
        IORemakeExcept.help()

        print(2*os.linesep, end="")
        IOTestExcept.help()

        print(2*os.linesep, end="")
        IODateExcept.help()

    def info_version(self):

        print("LabBook version " + ".".join([ str(i) for i in self.version ]))

    @staticmethod
    def date2str(date):
        """convert date to string"""

        return date.strftime('%d/%m/%Y')

    def str2date(self, strDate):
        """convert string to date and handle different format"""

        # initialization 
        oneDay = datetime.timedelta(days=1)
        todayDate = datetime.datetime.today().date()
        yearDate = todayDate.year
        separators = set(['/', '.', ':', '-'])
        date = None

        # conversion
        if strDate.lower() == 'yesterday':
            date = todayDate - oneDay

        elif strDate.lower() == 'today':
            date = todayDate
        
        elif strDate.lower() == 'tomorrow':
            date = todayDate + oneDay
        
        # with separator
        elif any( (sep in strDate) for sep in separators ):

            sep = [s for s in separators if s in strDate][0]
            
            d = strDate.split(sep)[0].zfill(2)
            m = strDate.split(sep)[1].zfill(2)
            y = strDate.split(sep)[2]   if strDate.count(sep) == 2\
                                        else str(yearDate)[2:]
            
            f = '%d%m%y' if len(y) == 2 else '%d%m%Y'
            
            try :
                date = datetime.datetime.strptime(d+m+y, f).date()
            
            except ValueError:
                raise IODateExcept(strDate)

        # no separator
        elif any( (len(strDate)==length) for length in [4,6,8] ):

            d = strDate[0:2]
            m = strDate[2:4]
            y = strDate[4:] if len(strDate) >= 6 else str(yearDate)[2:]
            f = '%d%m%Y' if len(strDate) == 8 else '%d%m%y'

            try :
                date = datetime.datetime.strptime(d+m+y, f).date()

            except ValueError:
                raise IODateExcept(strDate)

        else:
            raise IODateExcept(strDate)
        
        return date;


    def init(self, optargs):
        """option matching for init mode"""

        if len(optargs) != 0:
            raise IOInitExcept()
        return None, None


    def clean(self, optargs):
        """option matching for clean mode"""


        if len(optargs) != 0:
            raise IOCleanExcept()
        return None, None

    def new(self, optargs):
        """option matching for new mode"""

        if len(optargs) == 1:
            
            if Opt.date in optargs:
                
                startDate = optargs[Opt.date]
                endDate   = optargs[Opt.date]+self.oneDay

            elif Opt.start in optargs:
                
                startDate = optargs[Opt.start]
                endDate   = datetime.datetime.today().date()+self.oneDay

            else:
                raise IONewExcept()

        elif len(optargs) == 2:

            if not (Opt.start in optargs and Opt.end in optargs):
                raise IONewExcept()
            
            startDate = optargs[Opt.start]
            endDate   = optargs[Opt.end]+self.oneDay

            if startDate >= endDate:
                raise IODatesExcept(startDate, endDate)

        else:
            raise IONewExcept()

        return startDate, endDate

    def renew(self, optargs):
        """option matching for renew mode"""

        if len(optargs) is not 0:
            raise IORenewExcept()

        return None, None

    def make(self, optargs):
        """option matching for make mode"""

        if len(optargs) == 0:

            startDate = None
            endDate   = None

        elif len(optargs) == 1:
            
            if Opt.date in optargs:
                
                startDate = optargs[Opt.date]
                endDate   = optargs[Opt.date]+self.oneDay

            elif Opt.start in optargs:
                
                startDate = optargs[Opt.start]
                endDate   = None

            elif Opt.end in optargs:
                
                startDate = None
                endDate   = optargs[Opt.end]+self.oneDay

            else:
                raise IOMakeExcept()

        elif len(optargs) == 2:

            if Opt.date in optargs:
                raise IOMakeExcept()

            startDate = optargs[Opt.start]
            endDate   = optargs[Opt.end]+self.oneDay

            if startDate >= endDate:
                raise DatesExcept(startDate, endDate)

        else :
            raise IOMakeExcept()

        return startDate, endDate

    def remake(self, optargs):
        """option matching for remake mode"""

        if len(optargs) != 0:
            raise IORemakeExcept()

        return None, None

    def test(self, optargs):
        """option matching for test mode"""

        if len(optargs) != 0:
            raise IOTestExcept()

        return None, None
