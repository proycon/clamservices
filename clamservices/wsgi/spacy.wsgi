#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import site


import clamservices.config.spacy #** import your configuration module here! **
import clam.clamservice
application = clam.clamservice.run_wsgi(clamservices.config.spacy) #** pass your module to CLAM **

