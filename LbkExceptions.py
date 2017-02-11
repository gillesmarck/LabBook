#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime

# IO Date exceptions ========================================================= #

class IODateExcept(Exception):
    """raise for parsing date exception"""

    def info(self):

        print("Error: impossible to parse following date: " + self.args[0])
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<date>    formats are:")
        print(12*" " + "- keywords: yesterday, today, tomorrow")
        print(12*" " + "- formats: d/m, d/m/yy, d/m/yyyy, ddmm, ddmmyy, ddmmyyyy")
        print(12*" " + "- current year is assumed if not specified")
        print(12*" " + "- separators: / . : , -")

class IODatesExcept(Exception):
    """raise for date order exception"""

    def info(self):

        endDate = self.args[1] - datetime.timedelta(days=1)
        print("Error: start date and end date are not consistent:", end="")
        print(" from " + self.args[0].strftime("%d/%m/%Y"), end="")
        print(" to " + endDate.strftime("%d/%m/%Y") + "!")

# IO Mode exceptions ========================================================= #

class IOModeExcept(Exception):
    """raise if mismatching argument and options exception"""

class IOInitExcept(IOModeExcept):
    """raise if mismatching argument and options exception in init function"""
    
    def info(self):

        print("Error: init does not take any argument")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<init>    initialize a new labbook project:")
        print(12*" " + "- create a blank json file with main parameters")
        print(12*" " + "- create and populate folder with LaTeX templates")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook init")


class IOCleanExcept(IOModeExcept):
    """raise if mismatching argument and options exception in clean function"""
    
    def info(self):

        print("Error: clean does not take any argument")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<clean>   clean labbook project:")
        print(12*" " + "- remove .aux, .toc, .lof, .log and .out files from logs")
        print(12*" " + "- remove .tex and .pdf files from root")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook clean")


class IONewExcept(IOModeExcept):
    """raise if mismatching argument and options exception in new function"""
    
    
    def info(self):

        print("Error: new takes either [-d], [-s] or [-s, -e] arguments")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<new>     create new log for the specified dates:")
        print(12*" " + "- add log folder in logs/yyyy/mm/dd")
        print(12*" " + "- populate log folder with log.tex and header.tex")
        print(12*" " + "- add figs sub-folder for artwork materials")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook -d <date> new              ", end="")
        print("(at <date>)")
        print(12*" " + "> labbook -s <date> new              ", end="")
        print("(from <date> to current day)")
        print(12*" " + "> labbook -s <date> -e <date> new    ", end="")
        print("(between dates, included)")

class IORenewExcept(IOModeExcept):
    """raise if mismatching argument and options exception in renew function"""
    
    
    def info(self):

        print("Error: renew does not take any argument")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<renew>   renew template header for each log entry:")
        print(12*" " + "- clean project")
        print(12*" " + "- create new headers for each entry")
        print(10*" " + "required when modifying LaTeX templates in main folder")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook renew")

class IOMakeExcept(IOModeExcept):
    """raise if mismatching argument and options exception in make function"""
    
    def info(self):

        print("Error: new takes either [-d], [-s] or [-s, -e] arguments")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<make>    build pdf file with logs between the specified dates:")
        print(12*" " + "- update main LaTeX file with json data")
        print(12*" " + "- update main LaTeX file with logs to include")
        print(12*" " + "- call pdflatex with main LaTeX file")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook -d <date> make              ", end="")
        print("(at <date>)")
        print(12*" " + "> labbook -s <date> make              ", end="")
        print("(from <date> to newest date)")
        print(12*" " + "> labbook -e <date> make              ", end="")
        print("(from oldest date to <date>)")
        print(12*" " + "> labbook -s <date> -e <date> make    ", end="")
        print("(between dates, included)")

class IORemakeExcept(IOModeExcept):
    """raise if mismatching argument and options exception in remake function"""
    
    def info(self):

        print("Error: remake does not take any argument")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<remake>  rebuild pdf file from LaTeX main file:")
        print(12*" " + "- get current main LaTeX file")
        print(12*" " + "- call pdflatex with main LaTeX file")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook remake")

class IOTestExcept(IOModeExcept):
    """raise if mismatching argument and options exception in test function"""
    
    def info(self):

        print("Error: test does not take any argument")
        print(os.linesep, end="")
        self.help()

    @staticmethod
    def help():

        print("<test>    test main LabBook features:")
        print(12*" " + "- date parsing algorithm")
        print(12*" " + "- ...")
        print(os.linesep, end="")
        print(10*" " + "usage:")
        print(12*" " + "> labbook test")

# Mode exceptions ============================================================ #

class ModeExcept(Exception):
    """raise for internal problem when calling main functions"""

class DoNothingExcept(ModeExcept):
    """raise for exiting a function without doing nothing"""

    def info(self):

        print("Do nothing and exit.")

class InternalExcept(ModeExcept):
    """raise for unknown internal error"""

    def info(self):

        print("Internal error in " + self.args[0] + ". Exit.")

