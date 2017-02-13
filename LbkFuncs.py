#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import collections
import os
import shutil
import datetime
import pprint
import subprocess
import distutils.dir_util

import LbkTests

from LbkTools   import LbkTools
from LbkIO      import LbkIO
from LbkIO      import Mode

from LbkExceptions import DoNothingExcept

class LbkFuncs:
    """main LabBook features"""

    def __init__(self):
        """LbkFuncs class constructor"""

        # current module directory
        self.cmd=os.path.dirname(os.path.abspath(__file__))
        # current working directory
        self.cwd=os.getcwd()
        # curent template directory
        self.ctd=os.path.join(self.cwd,'tpl')
        # LbkTools instance
        self.lbkTools=LbkTools(self.ctd, self.cwd)
        # json parameter file
        self.paramPath=os.path.join(self.cwd, 'param.lbk')

    def getFunc(self, mode):
        """get function linked to mode enumeration"""

        funcs = {
            Mode.init  : self.init,
            Mode.clean : self.clean,
            Mode.make  : self.make,
            Mode.remake: self.remake,
            Mode.new   : self.new,
            Mode.renew : self.renew,
            Mode.test  : LbkTests.tests
        }
        return funcs.get(mode)

    def init(self, startDate, endDate):
        """initialize LabBook project"""
        
        print("> Initialize and populate folder ... ", end="")

        # Check folder status
        if os.path.isdir(os.path.join( self.ctd)) or \
           os.path.isfile(self.paramPath):
            
            print("fail.")
            print("Folder has already been initialized with LabBook project.")
            raise DoNothingExcept()

        # Create and populate template directory
        try :
            shutil.copytree(os.path.join(self.cmd,'tpl'), self.ctd)

        except Exception:
            print("fail.")
            raise
            
        # Create labbook parameter file
        keyvalues = {   'LBKAUTHOR': 'myName',
                        'LBKTITLE': 'myTitle',
                        'LBKFILENAME': 'myFileName'  }
        try :
            self.lbkTools.saveJsonFile( keyvalues, self.paramPath )

        except Exception:
            print("fail.")
            raise            

        print("ok.")
        print("> Edit and complete LabBook parameter file (param.lbk).")

    def clean(self, startDate, endDate):
        """clean LabBook project"""

        print("> Clean folder ... ", end="")

        # extensions of file to delete
        exts = ['.aux', '.toc', '.lof', '.log', '.out', '.gz']
        
        try:

            # remove non user file everywhere
            for root, dirs, files in os.walk(self.cwd):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in exts):
                        os.remove(os.path.join(root, file))

            # remove pdf and tex files in current working directory
            for file in os.listdir(self.cwd):
                if file.endswith(".tex") or file.endswith(".pdf"):
                    os.remove(os.path.join(self.cwd, file))

        except Exception:

            print("fail.")
            raise   

        print("ok.")

    def new(self, startDate, endDate):
        """add one or more log entries to LabBook project"""

        # Create log directory and store its LaTeX path
        addDay = datetime.timedelta(days=1)
        datePaths = {}
        while startDate < endDate:
            
            # display message
            strDate = LbkIO.date2str(startDate)
            print("> Create new entry for " + strDate + " ... ", end="")

            # fetch pathOS and pathLX for the given dates
            pathOS, pathLX = self.lbkTools.getLogPath(startDate)
                
            # Check if entry exists or not
            if not os.path.isdir(pathOS):

                os.makedirs(pathOS)
                datePaths[startDate] = (pathOS, pathLX)
                print("ok.")

            else:

                print("skip.")

            # increment
            startDate += addDay

        # copy files in each directory
        sortDatePaths = collections.OrderedDict(sorted(datePaths.items()))
        for date, paths in sortDatePaths.items():

            # Paths
            pathOS, pathLX = paths[0], paths[1]

            # Create figs directory
            os.mkdir(os.path.join(pathOS, 'figs'))

            # Copy, replace and paste for header file
            self.lbkTools.createHeader(date, pathOS, pathLX)

            # Copy, replace and paste for log file
            self.lbkTools.createLog(date, pathOS, pathLX)


    def renew(self, startDate, endDate):
        """delete and renew header files for each log entry"""

        # clean all files
        self.clean(startDate, endDate)

        # get all logs and replace header files
        print("> Renew headers ... ", end="") 

        try :

            for date in self.lbkTools.getLogDates():
                
                pathOS, pathLX = self.lbkTools.getLogPath(date)
                self.lbkTools.createHeader(date, pathOS, pathLX)

        except Exception:
            
            print("fail.")
            raise

        print("ok.")

    def make(self, startDate, endDate):
        """build pdf file between given dates depending on available logs"""
        print("> Build pdf output ... ") 

        # Logs to output
        dates = self.lbkTools.getLogDates(startDate, endDate)

        if len(dates) == 0:
            print("No entry log found between ", end='')
            print(LbkIO.date2str(startDate)+" and "+LbkIO.date2str(endDate)+".")
            raise DoNothingExcept()

        # Copy, replace and paste LabBook file
        keyValues = self.lbkTools.openJsonFile(self.paramPath)

        # 1. LabBook subtitle including date(s)
        if len(dates) == 1 :
            subtitle = dates[0].strftime('%B %d, %Y')
        else :
            subtitle  = 'from ' + dates[0].strftime('%B %d, %Y')
            subtitle += ' to ' + dates[-1].strftime('%B %d, %Y')
        keyValues['LBKSUBTITLE'] = subtitle

        # 2. LabBook input logs
        keyValues['LBKINPUT'] = \
            ''.join(['\include{' + self.lbkTools.latexPath([ 
                        'logs', d.strftime('%Y'), d.strftime('%m'),
                        d.strftime('%d'), 'log']) + '}' + os.linesep
                    for d in dates ])
        
        # 3. create main latex file and save its name
        filename = keyValues['LBKFILENAME'] + '.tex'
        self.lbkTools.replace( 'labbook.tex', filename, keyValues )

        # Pdflatex compilation
        subprocess.call(['pdflatex', filename])
        subprocess.call(['pdflatex', filename])

    def remake(self, startDate, endDate):
        """rebuild pdf file"""

        # Main file
        filenames = [   file for file in os.listdir(self.cwd)
                        if file.endswith(".tex") ]
        
        if not len(filenames) == 1:
            print("Impossible to identify main latex file.")
            raise DoNothingExcept()

        # Pdflatex compilaton
        subprocess.call(['pdflatex', filenames[0]])

