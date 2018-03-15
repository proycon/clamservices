#!/usr/bin/env python
#-*- coding:utf-8 -*-


###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Settings --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################


from clam.common.parameters import *
from clam.common.formats import *
from clam.common.viewers import *
from clam.common.data import *
from clam.common.converters import *
from clam.common.digestauth import pwhash
import clamservices.wrappers
import os
from base64 import b64decode as D

REQUIRE_VERSION = 2.3
WRAPPERDIR = clamservices.wrappers.__path__[0]

#============== General meta configuration =================
SYSTEM_ID = "foliastats"
SYSTEM_NAME = "FoLiA-stats"
SYSTEM_DESCRIPTION = "N-gram frequency list generation on FoLiA input"


USERS = None
DEBUG = False

#Load external configuration file
loadconfig(__name__)




#The system command (Use the variables $STATUSFILE $DATAFILE $PARAMETERS $INPUTDIRECTORY $OUTPUTDIRECTORY $USERNAME)
COMMAND = WRAPPERDIR +  "/wrappers/foliastats.py " + BINDIR + " $INPUTDIRECTORY $DATAFILE $STATUSFILE $OUTPUTDIRECTORY > $OUTPUTDIRECTORY/log"


PROFILES = [
    Profile(
        InputTemplate('foliainput', FoLiAXMLFormat,"FoLiA XML document",
            extension='.xml',
            multi=True
        ),
        OutputTemplate('wordfreqlist',CSVFormat,"Frequency list",
            SimpleTableViewer(),
            SetMetaField('encoding','utf-8'),
            filename='output.wordfreqlist.tsv',
            unique=True
        ),
        OutputTemplate('lemmafreqlist',CSVFormat,"Lemma Frequency list",
            SimpleTableViewer(),
            SetMetaField('encoding','utf-8'),
            filename='output.lemmafreqlist.tsv',
            unique=True
        ),
        OutputTemplate('lemmaposfreqlist',CSVFormat,"Lemma+PoS Frequency list",
            SimpleTableViewer(),
            SetMetaField('encoding','utf-8'),
            filename='output.lemmaposfreqlist.tsv',
            unique=True
        ),
    )
]

PARAMETERS =  [
    ('Modules', [

        BooleanParameter('lowercase','Lowercase', 'Convert all words to lower case'),
        IntegerParameter('n','N-Gram Count', 'Specify a value for n to count', default=1),
    ]),
]

DISPATCHER_MAXRESMEM = 25000 #25GB
