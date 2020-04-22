#!/usr/bin/env python3
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script, demonstrating CLAM Client API --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################


#This script will be called by CLAM and will run with the current working directory set to the specified project directory

from __future__ import print_function, unicode_literals, division, absolute_import

#general python modules:
import sys
import os


#import CLAM-specific modules:
import clam.common.data
import clam.common.status
import clam.common.parameters
import clam.common.formats

import spacy

shellsafe = clam.common.data.shellsafe

#this script takes three arguments: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY
datafile = sys.argv[1]
statusfile = sys.argv[2]
outputdir = sys.argv[3]


#os.environ['PYTHONPATH'] = bindir + '/../lib/python' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '/site-packages/frog' #Necessary for University of Tilburg servers (change or remove this in your own setup)

#Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml))
clamdata = clam.common.data.getclamdata(datafile)

#You now have access to all data. A few properties at your disposition now are:
# clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

clam.common.status.write(statusfile, "Starting...")

inputfiles = []
for i, inputfile in enumerate(clamdata.inputfiles('textinput')):
    inputfiles.append(inputfile)
for i, inputfile in enumerate(clamdata.inputfiles('foliainput')):
    inputfiles.append(inputfile)

models = {}
for lang in spacy.info()['Models'].split(','):
    lang = lang.strip()
    model = spacy.info(lang)
    if lang not in models:
        models[lang] =  lang + "_" + model['name']

clam.common.status.write(statusfile, "Processing ...")

if clamdata['model'] in models:
    model = models[clamdata['model']]
else:
    model = clamdata['model']

inputfilepaths = [ os.path.abspath(str(inputfile)) for inputfile in inputfiles ]

os.chdir(outputdir) #spacy2folia writes in current working directory
r = os.system("spacy2folia --model " + shellsafe(model) + " " + " ".join(( shellsafe(f,) for f in inputfilepaths )))
if r != 0:
    clam.common.status.write(statusfile, "Spacy returned with an error whilst processing. Aborting",100)
    sys.exit(1)

clam.common.status.write(statusfile, "Done",100)

sys.exit(0) #non-zero exit codes indicate an error!
