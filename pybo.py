#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import curses
from simvim import loop


if __name__ == '__main__':

    module_name = 'sina'
    if (len(sys.argv) > 1):
        module_name = sys.argv[1]

    #print getattr(__import__(module_name), fromlist=[module_name])
    module = getattr(__import__(name = module_name), module_name)()
    tweets = module.timeline()
    loop(tweets)

