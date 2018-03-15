#!/usr/bin/env python3
#-*- coding:utf-8 -*-


###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Settings --
#       by Maarten van Gompel (proycon)
#       http://proycon.github.io/clam/
#       Centre for Language and Speech Technology  / Language Machines
#       Radboud University Nijmegen
#
#       Licensed under GPLv3
#
###############################################################


from __future__ import print_function, unicode_literals, division, absolute_import

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

#THIS CONFIGURATION IS FOR FROG >= 0.12.10 ! OLDER VERSIONS WON'T WORK WITH IT!

#============== General meta configuration =================
SYSTEM_ID = "frog"
SYSTEM_NAME = "Frog"
SYSTEM_DESCRIPTION = "Frog is a suite containing a tokeniser, Part-of-Speech tagger, lemmatiser, morphological analyser, shallow parser, and dependency parser for Dutch, developed at Tilburg University. It is the successor of Tadpole."


USERS = None

# ================ Server specific configuration for CLAM ===============

DEBUG = False

#load external configuration file
loadconfig(__name__)


#The system command (Use the variables $STATUSFILE $DATAFILE $PARAMETERS $INPUTDIRECTORY $OUTPUTDIRECTORY $USERNAME)
COMMAND = WRAPPERDIR + "/frogwrapper.py " + BINDIR + " $DATAFILE $STATUSFILE $OUTPUTDIRECTORY > $OUTPUTDIRECTORY/log"


PROFILES = [
    Profile(
        InputTemplate('maininput', PlainTextFormat,"Text document",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            StringParameter(id='author', name='Author', description='The author of the document (optional)'),
            StringParameter(id='docid', name='Document ID', description='An ID for the document (optional, used with FoLiA XML output)'),
            BooleanParameter(id='sentenceperline', name='One sentence per line?', description='If set, assume that this input file contains exactly one sentence per line'),
            PDFtoTextConverter(id='pdfconv',label='Convert from PDF Document'),
            MSWordConverter(id='mswordconv',label='Convert from MS Word Document'),
            CharEncodingConverter(id='latin1',label='Convert from Latin-1 (iso-8859-1)',charset='iso-8859-1'),
            CharEncodingConverter(id='latin9',label='Convert from Latin-9 (iso-8859-15)',charset='iso-8859-15'),
            multi=True,
            extension='.txt',
        ),
        OutputTemplate('mainoutput', TadpoleFormat,"Frog Columned Output (legacy)",  #named 'mainoutput' for legacy reasons
            SetMetaField('tokenisation','yes'),
            SetMetaField('postagging','yes'),
            SetMetaField('lemmatisation','yes'),
            SetMetaField('morphologicalanalysis','yes'),
            ParameterCondition(skip_contains='m',
                then=SetMetaField('mwudetection','no'),
                otherwise=SetMetaField('mwudetection','yes'),
            ),
            ParameterCondition(skip_contains='p',
                then=SetMetaField('parsing','no'),
                otherwise=SetMetaField('parsing','yes'),
            ),
            removeextensions=['.txt','.xml'],
            extension='.frog.out',
            copymetadata=True,
            multi=True,
        ),
        OutputTemplate('foliaoutput', FoLiAXMLFormat,"FoLiA Document",
            FoLiAViewer(),
            FLATViewer(url=FLATURL, mode='viewer'),
            removeextensions=['.txt'],
            extension='.xml',
            copymetadata=True,
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('foliainput', FoLiAXMLFormat,"FoLiA XML document",
            extension='.xml',
            multi=True,
        ),
        OutputTemplate('mainoutput', TadpoleFormat,"Frog Columned Output (legacy)",  #named 'mainoutput' for legacy reasons
            SetMetaField('tokenisation','yes'),
            SetMetaField('postagging','yes'),
            SetMetaField('lemmatisation','yes'),
            SetMetaField('morphologicalanalysis','yes'),
            ParameterCondition(skip_contains='m',
                then=SetMetaField('mwudetection','no'),
                otherwise=SetMetaField('mwudetection','yes'),
            ),
            ParameterCondition(skip_contains='p',
                then=SetMetaField('parsing','no'),
                otherwise=SetMetaField('parsing','yes'),
            ),
            removeextensions=['.xml','.txt'],
            extension='.frog.out',
            copymetadata=True,
            multi=True,
        ),
        OutputTemplate('foliaoutput', FoLiAXMLFormat,"FoLiA Document",
            FoLiAViewer(),
            FLATViewer(url=FLATURL, mode='viewer'),
            extension='.xml',
            copymetadata=True,
            multi=True,
        ),
    ),

]

PARAMETERS =  [

    ('Modules', [
        ChoiceParameter('skip', 'Skip modules','Are there any components you want to skip? Skipping components you do not need may speed up the process considerably.',paramflag='--skip=',choices=[('t','Tokeniser'),('m','Multi-Word Detector'),('p','Parser'),('c','Chunker / Shallow parser'),('n','Named Entity Recognition')], multi=True ),
        #ChoiceParameter('skip', 'Skip Components','Are there any components you want to skip? Skipping the parser speeds up the process considerably.',paramflag='--skip=',choices=[('p','Skip dependency parser'),('n',"Don't skip anything")] ),
    ]),
]
