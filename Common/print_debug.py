#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#PAS XML Object Parsing
NO_DEBUG_FLAGS = 0
DEBUG_FLAG_PADDING = 1
DEBUG_FLAG_RANGES = 2
DEBUG_DATA_READING = 4
DEBUG_DATA_CHECK = 8
DEBUG_FLAG_ADD_REMOVE_ELEMENTS = 16


#PAS DDS Object Parsing
DEBUG_DDS_OPT_PARSING = 32

#MMI
DEBUG_MMI = 64



DEBUG_ACTIVATED_FLAGS = 0

def set_debug_flags(flags):
    global DEBUG_ACTIVATED_FLAGS
    DEBUG_ACTIVATED_FLAGS = flags

def print_debug(string, flag = 0xFF):
    # print("Flag {0} DEBUG_ACTIVATED_FLAGS {1}".format(flag, DEBUG_ACTIVATED_FLAGS))
    if flag & DEBUG_ACTIVATED_FLAGS != 0:
        logging.debug(string)
