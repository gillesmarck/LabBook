#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import io
import json
import os
import shutil
import datetime
import pprint

from LbkExceptions import InternalExcept

class LbkTools:
    """tools for LabBook main functions"""

    def __init__(self, ctd, cwd):
        """LbkTools class constructor"""

        # current template directory
        self.ctd = ctd
        # current working directory
        self.cwd = cwd


    def replace(self, src, dest, keyvalues):
        """replace key by value in src file to dest file"""

        # open source file        
        filedata = None
        with open(os.path.join(self.ctd, src), 'r') as file :
            filedata = file.read()

        # Replace key in src by value in dest
        for key, value in keyvalues.items():
            if isinstance(value, (list, tuple)):
                filedata = filedata.replace(key, ''.join(value))
            else :
                filedata = filedata.replace(key, value)

        # Write dest
        with open(os.path.join(self.cwd, dest), 'w') as file:
            file.write(filedata)


    def getLogPath(self, date):
        """get OS and LaTeX paths for a given date. """

        pathOS = os.path.join(  'logs', 
                                str(date.year),
                                str(date.month).zfill(2),
                                str(date.day).zfill(2) )

        pathLX = self.latexPath(['logs', 
                                str(date.year),
                                str(date.month).zfill(2),
                                str(date.day).zfill(2)] )

        return pathOS, pathLX


    def getLogDates(self, startDate = None, endDate = None):
        """list available log between start and end date"""

        # List available logs
        root = os.path.join(self.cwd,'logs')
        idx = len( os.path.join(root, '') )
        form = os.path.join('%Y','%m','%d');
        avLogs = [datetime.datetime.strptime(subpath[0][idx:], form).date()
                for subpath in os.walk(root) 
                if len(subpath[0][idx:])==len( os.path.join('YYYY','MM','DD')) ]

        # Select dates between start and end dates
        dates = list()

        if   startDate == None and endDate == None:
            
            dates = avLogs

        elif isinstance(startDate, datetime.date) and \
             endDate == None:

            dates = [ date for date in avLogs if startDate <= date ]

        elif startDate == None and \
             isinstance(endDate, datetime.date):

            dates = [ date for date in avLogs if date < endDate ]

        elif isinstance(startDate, datetime.date) and \
             isinstance(endDate, datetime.date):

            dates = [   date for date in avLogs \
                        if startDate <= date and date < endDate ]

        else:
            raise InternalExcept("[LbkTools, getLogDates]")

        return dates


    def latexPath(self, pathList):
        """return a LaTeX path format"""
        return '/'.join(pathList)


    def openJsonFile(self, path ):
        """open Json file and return dictionary."""
        
        # check that path exists
        if not os.path.exists(path):
            raise InternalExcept("[LbkTools, openJsonFile]")

        # Loading data file. 
        jsonData = io.StringIO()
    
        # Skipping comments.
        with open(path) as jsonFile:
            for line in jsonFile:
                if not line.strip().startswith("//"):
                    jsonData.write(line.rstrip())

        # Creating Json dictionary.
        jsonData.seek(0)
        return json.load(jsonData)

    def saveJsonFile(self, jsonData, path ):
        """save data dictionary within a JSON file"""

        # Dumping Json data.
        with open(path, 'w') as jsonFile:
            json.dump(  jsonData, jsonFile,
                        indent=4, separators=(',', ': '))


    def createHeader(self, date, pathOS, pathLX):
        """create LaTeX header at a given date"""

        # Copy, replace and paste for header file
        stampDate = ''.join([   str(date.year),
                                str(date.month).zfill(2),
                                str(date.day).zfill(2) ])

        figPathDate = self.latexPath([ pathLX,'figs','' ])

        titleDate = date.strftime('%A, %B %d, %Y')

        keyvalues ={    'YYYYMMDD' : stampDate,
                        'LBKFIGPATH': figPathDate,
                        'LBKSECTION': titleDate}
                        
        self.replace(  'header.tex',
                        os.path.join(pathOS, "header.tex"),
                        keyvalues )


    def createLog(self, date, pathOS, pathLX):
        """create LaTeX log at a given date"""

        # Copy, replace and paste for log file
        keyvalues ={ 'LBKPATH': self.latexPath([ pathLX,'header']) }

        self.replace(  'log.tex',
                        os.path.join(pathOS, "log.tex"),
                        keyvalues )


