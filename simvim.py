# -*- coding: utf-8 -*-
import curses
import locale

class simvim:
    DOWN = 1
    UP = -1
    SPACE_KEY = 32
    ESC_KEY = 27
    screen = None
    def __init__(self, module):
        locale.setlocale(locale.LC_ALL, '')

        self.screen = curses.initscr()
        self.screen.keypad(1)
        self.screen.border(0)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        #curses.use_default_colors()
        curses.start_color() 
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN) 
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE) 
        curses.init_pair(3, curses.COLOR_MAGENTA,curses.COLOR_BLACK) 
        curses.init_pair(4, curses.COLOR_BLUE,curses.COLOR_BLACK) 

        self.module = module
        self.lines = module.index()

        self.toLineNum = 0

    def __del__(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def loop(self):
        while True:
            self.displayScreen()
            # get user command
            c = self.screen.getch()
            if c == curses.KEY_UP: 
                self.updown(self.UP)
            elif c == curses.KEY_DOWN:
                self.updown(self.DOWN)
            elif c == self.ESC_KEY:
                self.exit()

    def displayScreen(self):
        self.screen.clear()

        top = self.toLineNum
        bottom = top + curses.LINES
        cur = 0
        cur_block = 0
        while cur - top < bottom - 1:
            for (index, line, ) in enumerate(self.lines[cur_block]):
                if cur < top:
                    continue
                if (cur - top) >= (bottom - 1):
                    break
                if index == 0:
                    self.screen.addstr(cur, 0, line.encode('utf-8'), curses.color_pair(4))
                else:
                    self.screen.addstr(cur, 0, line.encode('utf-8'))
                cur += 1

            cur_block += 1

        self.screen.move(curses.LINES - 1, 0)
        self.screen.refresh()


