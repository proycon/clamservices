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

#THIS CONFIGURATION IS FOR FROG >= 0.12.10 ! OLDER VERSIONS WON'T WORK WITH IT!

#============== General meta configuration =================
SYSTEM_ID = "frog"
SYSTEM_NAME = "Frog"
SYSTEM_DESCRIPTION = "Frog is a suite containing a tokeniser, Part-of-Speech tagger, lemmatiser, morphological analyser, shallow parser, and dependency parser for Dutch."

SYSTEM_AUTHOR = "Ko van der Sloot, Antal van den Bosch, Maarten van Gompel, Bertjan Busser"

SYSTEM_AFFILIATION = "Centre for Language and Speech Technology, Radboud University"

SYSTEM_URL = "https://languagemachines.github.io/frog"

SYSTEM_EMAIL = "lamasoftware@science.ru.nl"

SYSTEM_LICENSE = "GNU General Public License v3"

SYSTEM_COVER_URL = "https://languagemachines.github.io/frog/style/icon.png"

INTERFACEOPTIONS = "centercover,coverheight100"

CUSTOMHTML_INDEX = """
<p><strong>Frog</strong> is an integration of memory-based natural
language processing (NLP) modules developed for Dutch. All NLP modules are
based on <strong>Timbl</strong>, the Tilburg memory-based learning software package. Most
modules were created in the 1990s at the <a href="http://ilk.uvt.nl">ILK Research Group</a> (Tilburg
University, the Netherlands) and the <a href="http://www.clips.ua.ac.be">CLiPS Research Centre</a> (University of
Antwerp, Belgium). Over the years they have been integrated into a single text
processing tool, which is currently maintained and developed by the <a href="http://cls.ru.nl/languagemachines/">Language Machines</a> Research Group and the <a href="http://www.ru.nl/clst">Centre for Language and Speech Technology</a> at <a href="http://cls.ru.nl">Radboud University Nijmegen</a>. A dependency parser, a base phrase chunker, and
a named-entity recognizer module were added more recently. Where possible, Frog makes use of
multi-processor support to run subtasks in parallel.</p>

<p>Various (re)programming rounds have been made possible through funding by
<a href="http://www.nwo.nl">NWO</a>, the Netherlands Organisation for Scientific Research, particularly under
the CGN project, the IMIX programme, the <a href="http://ilk.uvt.nl/il">Implicit Linguistics project</a>, the
<a href="http://www.clarin.nl">CLARIN-NL</a> programme and the <a href="http://www.clariah.nl">CLARIAH</a> programme.</p>
"""

USERS = None

# ================ Server specific configuration for CLAM ===============

DEBUG = False
FLATURL = None

#load external configuration file
loadconfig(__name__)


#The system command (Use the variables $STATUSFILE $DATAFILE $PARAMETERS $INPUTDIRECTORY $OUTPUTDIRECTORY $USERNAME)
COMMAND = WRAPPERDIR + "/frogwrapper.py " + BINDIR + " $DATAFILE $STATUSFILE $OUTPUTDIRECTORY"


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
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
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
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
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
