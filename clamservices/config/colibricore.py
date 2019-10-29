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


#============== General meta configuration =================
SYSTEM_ID = "colibricore"
SYSTEM_NAME = "Colibri Core"
SYSTEM_DESCRIPTION = "A tool for pattern extraction and analysis on corpus data."

SYSTEM_AUTHOR = "Maarten van Gompel"

SYSTEM_AFFILIATION = "Centre for Language and Speech Technology, Radboud University"

SYSTEM_URL = "https://proycon.github.io/colibri-core"

SYSTEM_EMAIL = "lamasoftware@science.ru.nl"

SYSTEM_LICENSE = "GNU General Public License v3"

SYSTEM_COVER_URL = "https://proycon.github.io/colibri-core/style/icon.png"

INTERFACEOPTIONS = "centercover,coverheight100"

CUSTOMHTML_INDEX = """
<p>Colibri Core is software to quickly and efficiently count and extract patterns from large corpus data, to extract various statistics on the extracted patterns, and to compute relations between the extracted patterns. The employed notion of pattern or construction encompasses the following categories:</p>

<ul>
    <li>n-gram -- n consecutive words</li>
    <li>skipgram -- An abstract pattern of predetermined length with one or multiple gaps (of specific size).</li>
    <li>flexgram -- An abstract pattern with one or more gaps of variable-size.</li>
</ul>
"""

USERS = None

#Load external configuration file
loadconfig(__name__)




#The system command (Use the variables $STATUSFILE $DATAFILE $PARAMETERS $INPUTDIRECTORY $OUTPUTDIRECTORY $USERNAME)
COMMAND = WRAPPERDIR +  "/colibricore.py " + BINDIR + " $DATAFILE $STATUSFILE $OUTPUTDIRECTORY"




PROFILES = [
    Profile(
        InputTemplate('foliainput', FoLiAXMLFormat,"FoLiA XML document",
            extension='.xml',
            multi=True
        ),
        OutputTemplate('corpusfile',BinaryDataFormat,"Colibri Corpus Data",
            removeextensions=['.txt','.xml'],
            extension='.colibri.dat',
            multi=True,
        ),
        OutputTemplate('patternmodel',BinaryDataFormat,"Colibri Pattern Model",
            removeextensions=['.txt','.xml'],
            extension='.colibri.patternmodel',
            multi=True,
        ),
        OutputTemplate('classfile',CSVFormat,"Colibri Class Data",
            SimpleTableViewer(),
            SetMetaField('encoding','utf-8'),
            removeextensions=['.txt','.xml'],
            extension='.colibri.cls',
            multi=True,
        ),
        ParameterCondition(extract=True,
            then=OutputTemplate('extract',CSVFormat,"Extract Pattern List",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.patterns.csv',
                multi=True
            )
        ),
        ParameterCondition(report=True,
            then=OutputTemplate('report',PlainTextFormat,"Statistical Report",
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.report.txt',
                multi=True
            )
        ),
        ParameterCondition(histogram=True,
            then=OutputTemplate('histogram',CSVFormat,"Histogram",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.histogram.csv',
                multi=True
            )
        ),
        ParameterCondition(reverseindex=True,
            then=OutputTemplate('reverseindex',CSVFormat,"Reverse Index",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.reverseindex.csv',
                multi=True
            )
        ),
        ParameterCondition(cooc=True,
            then=OutputTemplate('cooc',CSVFormat,"Co-occurrence data (absolute)",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.cooc.csv',
                multi=True
            )
        ),
        ParameterCondition(npmi=True,
            then=OutputTemplate('npmi',CSVFormat,"Co-occurrence data (relative)",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.npmi.csv',
                multi=True
            )
        )
    ),
    Profile(
        InputTemplate('textinput_tok', PlainTextFormat,"Plain text input (tokenised)",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            extension='.txt',
            multi=True
        ),
        OutputTemplate('corpusfile',BinaryDataFormat,"Colibri Corpus Data",
            removeextensions=['.txt','.xml'],
            extension='.colibri.dat',
            multi=True,
        ),
        OutputTemplate('patternmodel',BinaryDataFormat,"Colibri Pattern Model",
            removeextensions=['.txt','.xml'],
            extension='.colibri.patternmodel',
            multi=True,
        ),
        OutputTemplate('classfile',CSVFormat,"Colibri Class Data",
            SimpleTableViewer(),
            SetMetaField('encoding','utf-8'),
            removeextensions=['.txt','.xml'],
            extension='.colibri.cls',
            multi=True,
        ),
        ParameterCondition(extract=True,
            then=OutputTemplate('extract',CSVFormat,"Extract Pattern List",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.patterns.csv',
                multi=True
            )
        ),
        ParameterCondition(report=True,
            then=OutputTemplate('report',PlainTextFormat,"Statistical Report",
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.report.txt',
                multi=True
            )
        ),
        ParameterCondition(histogram=True,
            then=OutputTemplate('histogram',CSVFormat,"Histogram",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.histogram.csv',
                multi=True
            )
        ),
        ParameterCondition(reverseindex=True,
            then=OutputTemplate('reverseindex',CSVFormat,"Reverse Index",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.reverseindex.csv',
                multi=True
            )
        ),
        ParameterCondition(cooc=True,
            then=OutputTemplate('cooc',CSVFormat,"Co-occurrence data (absolute)",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.cooc.csv',
                multi=True
            )
        ),
        ParameterCondition(npmi=True,
            then=OutputTemplate('npmi',CSVFormat,"Co-occurrence data (relative)",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.npmi.csv',
                multi=True
            )
        )
    ),
    Profile(
        InputTemplate('textinput_untok', PlainTextFormat,"Plain text input (untokenised)",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'),
            ChoiceParameter(id='language',name='Language',description='The language of the text', choices=[('en','English'),('nl','Dutch'),('de','German'),('fr','French'),('es','Spanish'),('pt','Portuguese'),('fy','Frysian'),('generic','Other (generic tokeniser)')]),
            BooleanParameter('sentenceperline_input','Input is one sentence per line'),
            BooleanParameter('sentenceperline_output','Output one sentence per line'),
            extension='.txt',
            multi=True
        ),
        OutputTemplate('corpusfile',BinaryDataFormat,"Colibri Corpus Data",
            removeextensions=['.txt','.xml'],
            extension='.colibri.dat',
            multi=True,
        ),
        OutputTemplate('patternmodel',BinaryDataFormat,"Colibri Pattern Model",
            removeextensions=['.txt','.xml'],
            extension='.colibri.patternmodel',
            multi=True,
        ),
        OutputTemplate('classfile',CSVFormat,"Colibri Class Data",
            SimpleTableViewer(),
            SetMetaField('encoding','utf-8'),
            removeextensions=['.txt','.xml'],
            extension='.colibri.cls',
            multi=True,
        ),
        ParameterCondition(extract=True,
            then=OutputTemplate('extract',CSVFormat,"Extract Pattern List",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.patterns.csv',
                multi=True
            )
        ),
        ParameterCondition(report=True,
            then=OutputTemplate('report',PlainTextFormat,"Statistical Report",
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.report.txt',
                multi=True
            )
        ),
        ParameterCondition(histogram=True,
            then=OutputTemplate('histogram',CSVFormat,"Histogram",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.histogram.csv',
                multi=True
            )
        ),
        ParameterCondition(reverseindex=True,
            then=OutputTemplate('reverseindex',CSVFormat,"Reverse Index",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.reverseindex.csv',
                multi=True
            )
        ),
        ParameterCondition(cooc=True,
            then=OutputTemplate('cooc',CSVFormat,"Co-occurrence data (absolute)",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.cooc.csv',
                multi=True
            )
        ),
        ParameterCondition(npmi=True,
            then=OutputTemplate('npmi',CSVFormat,"Co-occurrence data (relative)",
                SimpleTableViewer(),
                SetMetaField('encoding','utf-8'),
                removeextensions=['.txt','.xml'],
                extension='.npmi.csv',
                multi=True
            )
        )
    ),
]

PARAMETERS =  [
    ('Configuration', [
        BooleanParameter('lowercase','Lowercase', 'Convert all words to lower case'),
        IntegerParameter('mintokens','Occurrence threshold', 'Specify an occurrence threshold, only patterns occurring at least this many times in the corpus will show up in the result', default=2),
        IntegerParameter('minlength','Minimum length', 'Minimum length of n-gram or skipgram', default=1),
        IntegerParameter('maxlength','Maximum length', 'Maximum length of n-gram or skipgram (i.e value of n)', default=5),
        BooleanParameter('skipgrams','Skipgrams', 'Include skipgrams'),
        BooleanParameter('indexing','Indexing', 'Compute an indexed to where in the corpus the pattern is found (memory intensive!)'),
    ]),
    ('Modules (pick at least one)',[
        BooleanParameter('extract','Extract patterns', 'Output a list of all patterns (ngrams, skipgrams) with their counts'),
        BooleanParameter('report','Statistical Report','Output a statistical report of total counts per ngram-group, and coverage information (enable indexing for accurate coverage information)'),
        BooleanParameter('histogram','Histogram', 'Output a histogram of ngram/skipgram occurrence count'),
        BooleanParameter('reverseindex','Reverse Index', 'Output a reverse index, for each position in the corpus, the patterns that start on that position are listed'),
        IntegerParameter('cooc','Co-occurrence (absolute)', 'Compute co-occurring patterns (occuring on the same input line in the corpus data) that occur together more than the specified times  (0=disabled)', default=0),
        FloatParameter('npmi','Co-occurrence (relative)', 'Compute co-occurring patterns (occuring on the same input line in the corpus data) that have a normalised mutial information higher than the specified value (-1=disabled)', default=-1),
    ]),
    ('Query',[
        StringParameter('query','Query', 'Query the corpus for the following patterns (rather than all), should be a comma-separated list.'),
    ])
]

DISPATCHER_MAXRESMEM = 25000 #25GB
