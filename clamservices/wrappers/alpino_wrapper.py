#!/usr/bin/env python3
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script Template --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################

#This is a test wrapper, meant to illustrate how easy it is to set
#up a wrapper script for your system using Python and the CLAM Client API.
#We make use of the XML configuration file that CLAM outputs, rather than
#passing all parameters on the command line.

#This script will be called by CLAM and will run with the current working directory set to the specified project directory

#import some general python modules:
import sys
import os
import codecs
import re
import string
import glob
import traceback

#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status

from clamservices.config.alpino import CUSTOM_FORMATS

from foliatools import alpino2folia

#make a shortcut to the shellsafe() function
shellsafe = clam.common.data.shellsafe

#this script takes three arguments from CLAM: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY  (as configured at COMMAND= in the service configuration file)
datafile = sys.argv[1]
statusfile = sys.argv[2]
outputdir = sys.argv[3]
ALPINO_HOME = sys.argv[4]


#Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml))
clamdata = clam.common.data.getclamdata(datafile, CUSTOM_FORMATS)

#You now have access to all data. A few properties at your disposition now are:
# clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

clam.common.status.write(statusfile, "Starting...")

#SOME EXAMPLES (uncomment and adapt what you need)

#-- Iterate over all input files? --

for inputfile in clamdata.input:

    inputtemplate = inputfile.metadata.inputtemplate
    inputfilepath = str(inputfile)
    basename = os.path.basename(inputfilepath)[:-4] #without extension
    if inputtemplate == 'untokinput':
        #we have to tokenize first
        clam.common.status.write(statusfile, "Tokenizing " + basename)
        tokfile = os.path.join(outputdir,basename + '.tok')
        r = os.system('ucto -L nl -n ' + shellsafe(inputfilepath,'"') + ' > ' + shellsafe(tokfile,'"'))
        if r != 0:
            print("Failure running ucto",file=sys.stderr)
            sys.exit(2)
    else:
        tokfile = os.path.abspath(inputfilepath)
        os.system("sed -i 's/^M$//' " + shellsafe(tokfile,'"'))  #convert nasty DOS end-of-line to proper unix

    clam.common.status.write(statusfile, "Running Alpino on " + basename)

    pwd = os.getcwd()
    os.chdir(outputdir)
    if not os.path.exists("xml"):
        os.mkdir("xml")
    else:
        for filename in glob.glob('xml/*.xml'):
            os.unlink(filename) #clear for next round

    cmd = "ALPINO_HOME=" + shellsafe(ALPINO_HOME) + " " + ALPINO_HOME + "/bin/Alpino -veryfast -flag treebank xml debug=1 end_hook=xml user_max=900000 -parse < "  + tokfile
    print(cmd,file=sys.stderr)
    r = os.system(cmd)
    if r != 0:
        print("Failure running alpino",file=sys.stderr)
        sys.exit(2)

    os.chdir("xml")
    os.system("zip ../" + basename + ".alpinoxml.zip *.xml")
    clam.common.status.write(statusfile, "Conversion to FoLiA for " + basename)
    foliafile = os.path.join(outputdir,basename +'.folia.xml')
    doc = alpino2folia.makefoliadoc(foliafile)
    filenumbers = [ int(os.path.basename(x).replace('.xml','')) for x in glob.glob("*.xml") ]
    try:
        for seqnr in sorted(filenumbers):
            doc = alpino2folia.alpino2folia(str(seqnr) + '.xml',doc)
        doc.save(foliafile)
    except Exception as e: #pylint: disable=broad-except
        print("Error converting Alpino to FoLiA (" + basename +"): " + str(e), file=sys.stderr)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_lines = traceback.format_exc().splitlines()
        traceback.print_tb(exc_traceback, limit=50, file=sys.stderr)

    os.chdir('..')
    os.rename('xml','xml_' + basename)
    os.chdir(pwd)


#A nice status message to indicate we're done
clam.common.status.write(statusfile, "Done",100) # status update

sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
