# -*- coding: utf-8 -*-

class simvim:
    def __init__(self, module):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)
        self.screen.border(0)

        self.module = module

    def __del__(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def loop(self):
        pass

