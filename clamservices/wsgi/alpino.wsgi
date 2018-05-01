#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import os


import clamservices.config.alpino #** import your configuration module here! **
import clam.clamservice
application = clam.clamservice.run_wsgi(clamservices.config.alpino) #** pass your module to CLAM **

