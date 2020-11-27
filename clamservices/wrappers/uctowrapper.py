#!/usr/bin/env python3
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script for Text Statistics --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################


from __future__ import print_function, unicode_literals, division, absolute_import

#import some general python modules:
import sys
import os

#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status
from clam.common.util import makencname

shellsafe = clam.common.data.shellsafe

if __name__ == "__main__":

    #this script takes four arguments from CLAM: $BINDIR $DATAFILE $STATUSFILE $OUTPUTDIRECTORY  (as configured at COMMAND= in the service configuration file)
    bindir = sys.argv[1] #the directory containing the ucto executable
    datafile = sys.argv[2]
    statusfile = sys.argv[3]
    outputdir = sys.argv[4]

    #Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml))
    clamdata = clam.common.data.getclamdata(datafile)

    #You now have access to all data. A few properties at your disposition now are:
    # clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

    #Output status to the statusfile
    clam.common.status.write(statusfile, "Starting...")

    #Obtain all parameters, along with their flags, as a string suitable to pass to the tool, this is shell-safe by definition
    commandlineargs = clamdata.commandlineargs()

    l = len(clamdata.program) #total amount of output files, for computation of progress
    for i, (outputfile, outputtemplate) in enumerate(clamdata.program.getoutputfiles()):
        if outputtemplate in ('foliatokoutput','vtokoutput','tokoutput'):
            #Get path+filename for the outputfile
            outputfilepath = str(outputfile)

            #Update our status message to let CLAM know what we're doing
            clam.common.status.write(statusfile, "Producing " + os.path.basename(outputfilepath) + "...", round((i/l)*100))

            #We need one of the metadata fields (inherited from the input data), all of the output templates we defined have this parameter
            language = outputfile.metadata['language']

            #We have a one-one relationship between inputfiles and outputfiles, so we can grab the input file here:
            inputfile, inputtemplate = clamdata.program.getinputfile(outputfile)

            #Which outputtemplate are we processing?
            if outputtemplate == 'foliatokoutput':
                #FoLiA XML output
                docid = None
                if 'documentid' in inputfile.metadata and inputfile.metadata['documentid']:
                    docid = inputfile.metadata['documentid']
                else:
                    docid = makencname(os.path.basename(str(inputfile)).replace(".txt","").replace(".folia.xml","").replace(".xml",""))
                if not docid:
                    docid = "untitled"
                if os.system(os.path.join(bindir,'ucto') + ' -L ' + shellsafe(language,"'") + ' -X --id=' +
                          shellsafe(docid,"'") + ' ' + commandlineargs + ' ' +
                          shellsafe(str(inputfile),'"') +  ' ' + shellsafe(outputfilepath,'"')) != 0:
                    clam.common.status.write(statusfile, "Failed",100) # status update
                    sys.exit(1)
            elif outputtemplate == 'vtokoutput':
                #Verbose output
                if os.system(os.path.join(bindir,'ucto') + ' -L ' + shellsafe(language,"'")+ ' ' +
                          commandlineargs + ' ' + shellsafe(str(inputfile),'"') +
                         ' > ' + shellsafe(outputfilepath,'"')) != 0:
                    clam.common.status.write(statusfile, "Failed",100) # status update
                    sys.exit(1)
            elif outputtemplate == 'tokoutput':
                #plain text output
                if os.system(os.path.join(bindir,'ucto') + ' -L ' + shellsafe(language,"'")+ ' ' +
                          commandlineargs + ' ' + shellsafe(str(inputfile),'"') +
                          ' > ' + shellsafe(outputfilepath,'"'))  != 0:
                    clam.common.status.write(statusfile, "Failed",100) # status update
                    sys.exit(1)

    #A nice status message to indicate we're done
    clam.common.status.write(statusfile, "Done",100) # status update

    sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
