#! /usr/bin/python
# -*- encoding: utf-8 -*-
import sys,os
import urllib2,urllib
from string import join
from config import Config
from weibo import Weibo

write = sys.stdout.write
stty_height    = lambda: int(os.popen('stty size', 'r').read().split()[0])
clear_line     = lambda: write('\r\033[K')
clear_pre_line = lambda: write('\033[1A\r\033[K')

class pager():
  lines = weibo.timeline()
  command = ''

  def __init__(self, weibo):
    self.weibo = weibo

  try:
    import tty
    fd = sys.stdin.fileno()
    old = tty.tcgetattr(fd)
    tty.setcbreak(fd)
    getchar = lambda: sys.stdin.read(1)
  except (ImportError, AttributeError):
    tty = None
    getchar = lambda: sys.stdin.readline()[:-1][:1]

  try:
    r = inc = stty_height() -1 -1
    write(join(lines[:inc + 1], '\n') + '\n')

    while lines[r:]:
      inc = stty_height() -1 -1

      if not command and not weibo.error:
        write('-- %s/%s --' % (r,len(lines)))
      elif command:
        write(command)
      else:
        write(render_error(weibo.error))
        weibo.error = ''
      sys.stdout.flush()

      c = getchar()
      if c == '\x1b':
        '''press ESC'''
        command = ''
        clear_line()
        continue
      if command or c == ':':
        if c in ['\r','\n']:
          #process command
          weibo.error = 'unknown command: %s' % command
          command = c = ''

        clear_line()
        command += c
        continue
      if c in ['q', 'Q']:
        clear_line()
        for i in range (inc + 1): clear_pre_line()
        break
      elif c in ['\r', '\n']:
        r = r - (inc -1)
        if len(lines[r]) == 0: r += 1
      elif c in ['b', 'B']:
        r = r - inc - inc
        if r < 0: r = 0

      clear_line()
      for i in range (inc + 1): clear_pre_line()

      write(join(lines[r:r+inc+1], '\n') + '\n')
      r = r + inc
      if r < len(lines) and len(lines[r]) == 0: r += 1
    
    for i in range (inc + 1): clear_pre_line()
  
  finally:
    if tty:
      tty.tcsetattr(fd, tty.TCSAFLUSH, old)


if __name__ == '__main__':
  config = Config('sina')
  config.load()

  weibo = Weibo(config)
  pager = Pager(weibo)
  pager.loop()
