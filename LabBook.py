#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import traceback
import exitstatus

import LbkTests

from LbkIO          import Opt
from LbkIO          import Mode
from LbkIO          import LbkIO
from LbkFuncs       import LbkFuncs

from LbkExceptions  import ModeExcept
from LbkExceptions  import IOModeExcept
from LbkExceptions  import IODateExcept
from LbkExceptions  import IODatesExcept

def main(argv):
    """main LabBook function"""

    lbkIO = LbkIO()

    # parsing options and arguments ------------------------------------------ #
    try:
        getOpts, getArgs = getopt.getopt( argv,
                            'hv'+':'.join([opt.name[0] for opt in Opt])+':',
                            ['help','version']+[opt.name+'=' for opt in Opt] )

    except getopt.GetoptError as e:
        print(e)
        lbkIO.usage()
        sys.exit(exitstatus.ExitStatus.failure)

    # converting options ----------------------------------------------------- #
    optargs = {}
    for getOpt, getArg in getOpts:
        
        # converting option
        if getOpt == '-h':
            lbkIO.usage()
            sys.exit(exitstatus.ExitStatus.success)

        if getOpt == '--help':
            lbkIO.help()
            sys.exit(exitstatus.ExitStatus.success) 

        if getOpt in ('-v', '--version'):
            lbkIO.info_version()
            sys.exit(exitstatus.ExitStatus.success)

        opt =   Opt[getOpt[2:]]   if getOpt[0:2]=='--'\
                else Opt([opt.name[0] for opt in Opt].index(getOpt[1:]))
        
        # converting argument
        try:
            arg = lbkIO.str2date(getArg)

        except IODateExcept as e:
            e.info()
            sys.exit(exitstatus.ExitStatus.failure)

        # output
        optargs[opt] = arg

    # converting argument ---------------------------------------------------- #
    if not(len(getArgs) == 1):
        print("LabBook takes only one argument.")
        lbkIO.usage()
        exit(exitstatus.ExitStatus.failure)

    # looking for valid arguments
    getArg = getArgs[0]

    if not(getArg in [ mode.name for mode in Mode ]):
        print("Unknown argument.")
        lbkIO.help()
        exit(exitstatus.ExitStatus.failure)

    mode = Mode[getArg]

    # checking options with argument and compute start and end dates --------- #
    getDates = lbkIO.getChecker(mode)
    
    try :
        startDate, endDate = getDates(optargs)

    # except (InitException, CleanException) as e:
    except (IOModeExcept, IODatesExcept) as e:
        e.info()
        exit(exitstatus.ExitStatus.failure)

    # calling main function -------------------------------------------------- #
    lbkFuncs = LbkFuncs()
    func = lbkFuncs.getFunc(mode)

    try :
        func(startDate, endDate)

    except ModeExcept as e:
        e.info()
        exit(exitstatus.ExitStatus.failure)

    except Exception as e:
        print("unknown internal error")
        print(e)
        #traceback.print_exc()
        exit(exitstatus.ExitStatus.failure)

    return exitstatus.ExitStatus.success

# Main ======================================================================= #
if __name__ == "__main__":
   
    main(sys.argv[1:])
    sys.exit(exitstatus.ExitStatus.success)