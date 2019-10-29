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

REQUIRE_VERSION = 3.0
WRAPPERDIR = clamservices.wrappers.__path__[0]

SYSTEM_ID = "ucto"
SYSTEM_NAME = "Ucto Tokeniser"
SYSTEM_DESCRIPTION = 'Ucto is a unicode-compliant tokeniser. It takes input in the form of one or more untokenised texts, and subsequently tokenises them. Several languages are supported, but the software is extensible to other languages.'

SYSTEM_AUTHOR = "Maarten van Gompel, Ko van der Sloot"

SYSTEM_AFFILIATION = "Centre for Language and Speech Technology, Radboud University"

SYSTEM_URL = "https://languagemachines.github.io/ucto"

SYSTEM_EMAIL = "lamasoftware@science.ru.nl"

SYSTEM_LICENSE = "GNU General Public License v3"

SYSTEM_COVER_URL = "http://languagemachines.github.io/ucto/style/icon.png"

INTERFACEOPTIONS = "centercover,coverheight100"

CUSTOMHTML_INDEX = """
Ucto comes with tokenisation rules for several languages and can be easily extended to suit other languages. It has been incorporated for tokenizing Dutch text in Frog, our Dutch morpho-syntactic processor.
"""

#Users and passwords
USERS = None #Enable this instead if you want no authentication


# ================ Server specific configuration for CLAM ===============
DEBUG = False

#Load externa configuration file
loadconfig(__name__)




#The system command. It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $DATAFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in user
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags
#
COMMAND =  WRAPPERDIR + "/uctowrapper.py " + BINDIR + " $DATAFILE $STATUSFILE $OUTPUTDIRECTORY > $OUTPUTDIRECTORY/log"


PROFILES = [
    Profile(
        InputTemplate('untokinput', PlainTextFormat,"Text document",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            ChoiceParameter(id='language',name='Language',description='The language this text is in', choices=[('eng','English'),('nld','Dutch'),('nld-twitter','Dutch on Twitter'),('fra','French'),('deu','German'),('ita','Italian'),('fry','Frisian'), ('swe', 'Swedish'), ('rus', 'Russian'), ('spa', 'Spanish'), ('por', 'Portuguese'), ('tur', 'Turkish')], required=True),
            StringParameter(id='documentid', name='Document ID', description='Enter a unique identifier for this document (no spaces). Needed only for XML output, will be auto-generated if not specified.'),
            StringParameter(id='author', name='Author', description='The author of the document (optional)'),
            PDFtoTextConverter(id='pdfconv',label='Convert from PDF Document'),
            MSWordConverter(id='mswordconv',label='Convert from MS Word Document'),
            CharEncodingConverter(id='latin1',label='Convert from Latin-1 (iso-8859-1)',charset='iso-8859-1'),
            CharEncodingConverter(id='latin9',label='Convert from Latin-9 (iso-8859-15)',charset='iso-8859-15'),
            extension='txt',
            multi=True,
        ),
        ParameterCondition(xml=True, #if the XML parameter is set to True...
        then=OutputTemplate('foliatokoutput', FoLiAXMLFormat, "Tokenised Text Document (FoLiA XML)",
                SetMetaField('tokenisation','ucto'),
                FLATViewer(url=FLATURL, mode='viewer'),
                copymetadata=True,
                removeextension='txt',
                extension='xml',
                multi=True,
             ),
        otherwise=ParameterCondition(verbose=True, #if the verbose parameter is set to True
            then=OutputTemplate('vtokoutput', PlainTextFormat,"Verbosely Tokenised Text Document",
                ParameterCondition(sentenceperline=True, #set some parameters that reflect the state of certain global paramaters
                    then=SetMetaField('sentenceperline','yes')
                ),
                ParameterCondition(lowercase=True,
                    then=SetMetaField('lowercase','yes')
                ),
                ParameterCondition(uppercase=True,
                    then=SetMetaField('uppercase','yes')
                ),
                copymetadata=True, #we want all metadata from the input template (language, author, etc) to be carried over to the output template
                removeextension='txt', #remove this extension before adding the one below
                extension='vtok', #add this extension
                multi=True,
            ),
            otherwise=OutputTemplate('tokoutput', PlainTextFormat,"Tokenised Text Document",
                ParameterCondition(sentenceperline=True,
                    then=SetMetaField('sentenceperline','yes')
                ),
                ParameterCondition(lowercase=True,
                    then=SetMetaField('lowercase','yes')
                ),
                ParameterCondition(uppercase=True,
                    then=SetMetaField('uppercase','yes')
                ),
                copymetadata=True,
                removeextension='txt',
                extension='tok',
                multi=True,
            )
        )
        )
    ),
]

PARAMETERS =  [
    ('Tokenisation options', [
        BooleanParameter('xml','FoLiA XML Output','Output FoLiA XML',value=True),
        BooleanParameter('verbose','Verbose tokeniser output','Outputs token types per token, one token per line',paramflag='-V',forbid=['sentenceperline','xml'] ),
        BooleanParameter('sentenceperline','Sentence per line','Output each sentence on a single line. Does not work in verbose or XML mode.', paramflag='-n', forbid=['verbose','xml']),
        BooleanParameter('lowercase','Lowercase','Convert text to lowercase',forbid=['uppercase', 'xml'], paramflag='-l'),
        BooleanParameter('uppercase','Uppercase','Convert text to uppercase',forbid=['lowercase', 'xml'], paramflag='-u'),
    ]),
]

