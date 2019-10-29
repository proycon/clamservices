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
import spacy
from base64 import b64decode as D

REQUIRE_VERSION = 3.0
WRAPPERDIR = clamservices.wrappers.__path__[0]

#THIS CONFIGURATION IS FOR FROG >= 0.12.10 ! OLDER VERSIONS WON'T WORK WITH IT!

#============== General meta configuration =================
SYSTEM_ID = "spacy"
SYSTEM_NAME = "spaCy"
SYSTEM_DESCRIPTION = "spaCy is a library for advanced Natural Language Processing. It's built on the very latest research, and was designed from day one to be used in real products. spaCy comes with pre-trained statistical models and word vectors, and currently supports tokenization for 45+ languages. It features the fastest syntactic parser in the world, convolutional neural network models for tagging, parsing and named entity recognition and easy deep learning integration. This webservice  provides access to various types of linguistic enrichment for a wide variety of languages. This webservice is developed by the Centre of Language and Speech Technology (Radboud University, Nijmegen) and wraps around spaCy whilst also providing some extra functionality such as FoLiA XML output."

SYSTEM_AUTHOR = "Matthew Honnibal, Ines Montani et al."

SYSTEM_URL = "https://spacy.io"

SYSTEM_LICENSE = "MIT"



USERS = None

# ================ Server specific configuration for CLAM ===============

DEBUG = False

#load external configuration file
loadconfig(__name__)


#The system command (Use the variables $STATUSFILE $DATAFILE $PARAMETERS $INPUTDIRECTORY $OUTPUTDIRECTORY $USERNAME)
COMMAND = WRAPPERDIR + "/spacywrapper.py $DATAFILE $STATUSFILE $OUTPUTDIRECTORY > $OUTPUTDIRECTORY/log"


PROFILES = [
    Profile(
        InputTemplate('textinput', PlainTextFormat,"Text document",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            PDFtoTextConverter(id='pdfconv',label='Convert from PDF Document'),
            MSWordConverter(id='mswordconv',label='Convert from MS Word Document'),
            CharEncodingConverter(id='latin1',label='Convert from Latin-1 (iso-8859-1)',charset='iso-8859-1'),
            CharEncodingConverter(id='latin9',label='Convert from Latin-9 (iso-8859-15)',charset='iso-8859-15'),
            multi=True,
            extension='.txt',
        ),
        OutputTemplate('foliaoutput', FoLiAXMLFormat,"FoLiA Document",
            FoLiAViewer(),
            FLATViewer(url=FLATURL, mode='viewer'),
            removeextensions=['.txt'],
            extension='.folia.xml',
            copymetadata=True,
            multi=True,
        ),
    ),
]

models = []
for lang in spacy.info()['models']:
    for model in spacy.info(lang):
        models.append( ( lang + "_" + model['name'] + model['description'] ) )

PARAMETERS =  [
    ('Model Selection', [
        ChoiceParameter('model', 'Model','The spaCy model to use, determines for what language is processed and what linguistic enrichments are performed',choices=models,required=True ),
    ]),
]
