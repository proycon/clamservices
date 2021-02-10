#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Service Configuration File (Template) --
#       by Maarten van Gompel (proycon)
#       Centre for Language and Speech Technology / Language Machines
#       Radboud University Nijmegen
#
#       https://proycon.github.io/clam
#
#       Licensed under GPLv3
#
###############################################################

#Consult the CLAM manual for extensive documentation

from clam.common.parameters import *
from clam.common.formats import *
from clam.common.converters import *
from clam.common.viewers import *
from clam.common.data import *
from clam.common.digestauth import pwhash
import clamservices.wrappers
from base64 import b64decode as D
import clam
import sys
import os

REQUIRE_VERSION = 3.0
WRAPPERDIR = clamservices.wrappers.__path__[0]

# ======== GENERAL INFORMATION ===========

# General information concerning your system.


#The System ID, a short alphanumeric identifier for internal use only
SYSTEM_ID = "alpino"
#System name, the way the system is presented to the world
SYSTEM_NAME = "Alpino"

#An informative description for this system (this should be fairly short, about one paragraph, and may not contain HTML)
SYSTEM_DESCRIPTION = "Alpino is a dependency parser for Dutch, developed in the context of the PIONIER Project Algorithms for Linguistic Processing, developed by Gertjan van Noord at the University of Groningen. You can upload either tokenised or untokenised files (which will be automatically tokenised for you using ucto), the output will consist of a zip file containing XML files, one for each sentence in the input document."

SYSTEM_AUTHOR = "Gertjan van Noord"

SYSTEM_AFFILIATION = "Rijksuniversieit Groningen"

SYSTEM_URL = "http://www.let.rug.nl/vannoord/alp/Alpino/"

SYSTEM_EMAIL = "lamasoftware@science.ru.nl"

SYSTEM_LICENSE = "GNU Lesser General Public License v2.1"

INTERFACEOPTIONS = "centercover,coverheight100"

# ======== AUTHENTICATION & SECURITY ===========

#Users and passwords

#set security realm, a required component for hashing passwords (will default to SYSTEM_ID if not set)
#REALM = SYSTEM_ID

USERS = None #no user authentication/security (this is not recommended for production environments!)

DEBUG = False
FLATURL = None
SWITCHBOARD_FORWARD_URL = None
FROG_FORWARD_URL = None

if 'ALPINO_HOME' in os.environ:
    ALPINO_HOME = os.environ['ALPINO_HOME']

#Load external configuration file
loadconfig(__name__)

# ======== ENABLED FORMATS ===========

class AlpinoXMLCollection(CLAMMetaData):
    attributes = {}
    name = "Alpino XML Collection"
    mimetype = 'application/zip'
    scheme = '' #for later perhaps

CUSTOM_FORMATS = [ AlpinoXMLCollection ]

# ======== PROFILE DEFINITIONS ===========

#Define your profiles here. This is required for the project paradigm, but can be set to an empty list if you only use the action paradigm.

PROFILES = [
    Profile(
        InputTemplate('tokinput', PlainTextFormat,"Plaintext tokenised input, one sentence per line",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            extension='.tok',
            multi=True
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('alpinooutput',AlpinoXMLCollection,'Alpino XML output (XML files per sentence)',
            extension='.alpinoxml.zip', #set an extension or set a filename:
            removeextension='.tok',
            multi=True,
        ),
        OutputTemplate('foliaoutput',FoLiAXMLFormat,'FoLiA XML Output',
            FoLiAViewer(),
            ForwardViewer(id='switchboardforwarder',name="Open in CLARIN Switchboard",forwarder=Forwarder('switchboard','CLARIN Switchboard',SWITCHBOARD_FORWARD_URL),allowdefault=False) if SWITCHBOARD_FORWARD_URL else None,
            ForwardViewer(id='frogforwarder',name="Continue with Frog",forwarder=Forwarder('frog','Frog',FROG_FORWARD_URL)) if FROG_FORWARD_URL else None,
            extension='.folia.xml', #set an extension or set a filename:
            removeextension='.tok',
            multi=True,
        ),
    ),
    Profile(
        InputTemplate('untokinput', PlainTextFormat,"Plaintext document (untokenised)",
            StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #MSWordConverter(id='docconv',label='Convert from MS Word Document'),
            extension='.txt',
            multi=True, #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('tokoutput', PlainTextFormat,"Plaintext tokenised output, one sentence per line",
            SetMetaField('encoding','utf-8'),
            ForwardViewer(id='switchboardforwarder',name="Open in CLARIN Switchboard",forwarder=Forwarder('switchboard','CLARIN Switchboard',SWITCHBOARD_FORWARD_URL),allowdefault=False) if SWITCHBOARD_FORWARD_URL else None,
            removeextensions='.txt',
            extension='.tok',
            multi=True,
        ),
        OutputTemplate('alpinooutput',AlpinoXMLCollection,'Alpino XML output (XML files per sentence)',
            extension='.alpinoxml.zip', #set an extension or set a filename:
            removeextensions='.txt',
            multi=True,
        ),
        OutputTemplate('foliaoutput',FoLiAXMLFormat,'FoLiA XML Output',
            FoLiAViewer(),
            FLATViewer(url=FLATURL, mode='viewer') if FLATURL else None,
            ForwardViewer(id='switchboardforwarder',name="Open in CLARIN Switchboard",forwarder=Forwarder('switchboard','CLARIN Switchboard',SWITCHBOARD_FORWARD_URL),allowdefault=False) if SWITCHBOARD_FORWARD_URL else None,
            ForwardViewer(id='frogforwarder',name="Continue with Frog",forwarder=Forwarder('frog','Frog',FROG_FORWARD_URL)) if FROG_FORWARD_URL else None,
            extension='.folia.xml', #set an extension or set a filename:
            removeextension='.txt',
            multi=True,
        ),
    )
]

# ======== COMMAND ===========

#The system command for the project paradigm.
#It is recommended you set this to small wrapper
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
COMMAND = WRAPPERDIR + "/alpino_wrapper.py $DATAFILE $STATUSFILE $OUTPUTDIRECTORY " + ALPINO_HOME

#COMMAND = None   #Set to none if you only use the action paradigm

# ======== PARAMETER DEFINITIONS ===========

#The global parameters (for the project paradigm) are subdivided into several
#groups. In the form of a list of (groupname, parameters) tuples. The parameters
#are a list of instances from common/parameters.py

PARAMETERS = []

#PARAMETERS =  [
#    ('Alpino Parameters', [
#        #BooleanParameter(id='veryfast',name='Very fast',description='Improves the speed of the parser, returns only the first (best) analysis.'),
#        #BooleanParameter(id='slow',name='slow',description='Provide all possible parses'),
#        #ChoiceParameter(id='casesensitive',name='Case Sensitivity',description='Enable case sensitive behaviour?', choices=['yes','no'],default='no'),
#       #StringParameter(id='author',name='Author',description='Sign output metadata with the specified author name',maxlength=255),
#    ] )
#]


# ======= ACTIONS =============

#The action paradigm is an independent Remote-Procedure-Call mechanism that
#allows you to tie scripts (command=) or Python functions (function=) to URLs.
#It has no notion of projects or files and must respond in real-time. The syntax
#for commands is equal to those of COMMAND above, any file or project specific
#variables are not available though, so there is no $DATAFILE, $STATUSFILE, $INPUTDIRECTORY, $OUTPUTDIRECTORY or $PROJECT.

ACTIONS = [
    #Action(id='multiply',name='Multiply',parameters=[IntegerParameter(id='x',name='Value'),IntegerParameter(id='y',name='Multiplier'), command=sys.path[0] + "/actions/multiply.sh $PARAMETERS" ])
    #Action(id='multiply',name='Multiply',parameters=[IntegerParameter(id='x',name='Value'),IntegerParameter(id='y',name='Multiplier'), function=lambda x,y: x*y ])
]


# ======== DISPATCHING (ADVANCED! YOU CAN SAFELY SKIP THIS!) ========

#The dispatcher to use (defaults to clamdispatcher.py), you almost never want to change this
#DISPATCHER = 'clamdispatcher.py'

#DISPATCHER_POLLINTERVAL = 30   #interval at which the dispatcher polls for resource consumption (default: 30 secs)
#DISPATCHER_MAXRESMEM = 0    #maximum consumption of resident memory (in megabytes), processes that exceed this will be automatically aborted. (0 = unlimited, default)
#DISPATCHER_MAXTIME = 0      #maximum number of seconds a process may run, it will be aborted if this duration is exceeded.   (0=unlimited, default)
#DISPATCHER_PYTHONPATH = []        #list of extra directories to add to the python path prior to launch of dispatcher

#Run background process on a remote host? Then set the following (leave the lambda in):
#REMOTEHOST = lambda: return 'some.remote.host'
#REMOTEUSER = 'username'

#For this to work, the user under which CLAM runs must have (passwordless) ssh access (use ssh keys) to the remote host using the specified username (ssh REMOTEUSER@REMOTEHOST)
#Moreover, both systems must have access to the same filesystem (ROOT) under the same mountpoint.
