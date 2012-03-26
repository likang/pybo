#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import curses
from simvim import simvim


if __name__ == '__main__':

    module_name = 'sina'
    if (len(sys.argv) > 1):
        module_name = sys.argv[1]

    #print getattr(__import__(module_name), fromlist=[module_name])
    module = getattr(__import__(name = module_name), module_name)()
    print module.timeline()
    """ 
    global config
    config = Config()

    simvim = simvim(module)
    simvim.loop()
    """
