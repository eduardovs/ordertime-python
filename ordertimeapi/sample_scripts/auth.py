#!/usr/bin/env python
# coding: utf-8

import configparser
import confs

# Reading configuration files
parser = configparser.ConfigParser()
parser.read(confs.CONFIGFILE)
word = confs.decoder("ordertime")
pw = word.replace("KISS", "")
api_key = parser["ordertime"]["api_key"]
user = parser["ordertime"]["user"]
