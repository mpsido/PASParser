#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG_ACTIVATED_FLAGS = 0

def set_debug_flags(flags):
    global DEBUG_ACTIVATED_FLAGS
    DEBUG_ACTIVATED_FLAGS = flags

def print_debug(string, flag):
    # print("Flag {0} DEBUG_ACTIVATED_FLAGS {1}".format(flag, DEBUG_ACTIVATED_FLAGS))
    if flag & DEBUG_ACTIVATED_FLAGS != 0:
        print(string)
