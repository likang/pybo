#! /usr/bin/python
# -*- encoding: utf-8 -*-
import sys,os,cmd,re,json,base64
import ConfigParser
import urllib2,urllib
from string import join

render_name  = lambda s: '\033[94m%s\033[m' % s
render_error = lambda s: '\033[41m\033[37m %s \033[m' % s

def pager(weibo):
  """Page through text on a text terminal, modified from pydoc.ttypager."""
  write = sys.stdout.write
  stty_height    = lambda: int(os.popen('stty size', 'r').read().split()[0])
  clear_line     = lambda: write('\r\033[K')
  clear_pre_line = lambda: write('\033[1A\r\033[K')

  lines = weibo.timeline()
  command = ''

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
      if c in ['b', 'B']:
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


class Weibo():
  URLS = {}
  URLS['timeline'] = 'http://api.t.sina.com.cn/statuses/friends_timeline.json'

  def __init__(self,config):
    self.config = config
    self.lines = []
    username = config['username']
    password = config['password']
    base64string = base64.encodestring('%s:%s' % (username,password))[:-1]
    self.auth_header = 'Basic %s' % base64string
    self.max_id = 0
    self.min_id = 0
    self.error  = ''

  def request(self, api, params):
    req = urllib2.Request(self.URLS[api],urllib.urlencode(params))
    req.add_header('Authorization',self.auth_header)

    try:
      handle = urllib2.urlopen(req)
    except:
      self.error = 'error while connecting to weibo'
      return

    content = handle.read()
    handle.close()
    try:
      return json.loads(content)
    except:
      self.error = 'error while loading json'
      return

  def tidy_up(self,long_line,indent = 0):
    step = width = self.config['width'] - indent
    long_line = long_line.encode('gb18030')

    lines = []
    start = 0
    while long_line[start:]:
      try:
        line = long_line[start : start + step].decode('gb18030')
        lines.append('%s%s' % (' '*indent, line))
        start += step
        step = width
      except:
        step -= 1

    return lines

  def go_to_top(self):
    self.max_id = 0
    return self.timeline()

  def timeline(self):
    params = {'source':self.config['app_id'],'max_id':self.max_id}
    content = self.request('timeline',params)

    if not content or len(content) == 0:
      return

    lines = []
    author_color = self.config['author_color']
    end_color  = self.config['end_color']

    for tweet in content:
      indent = 0
      while tweet:
        text = tweet['text']
        username = tweet['user']['name']
        lines.append(' '*indent + render_name(username))
        lines.extend(self.tidy_up(text,indent))
        #if tweet.get('original_pic'):
        #  lines.extend(self.tidy_up('Pic: '+tweet.get('original_pic'), indent))
        indent += 4
        tweet = tweet.get('retweeted_status')

      lines.append('')

    self.max_id = int(content[-1]['id']) + 1
    return lines

class Config():
  SECTION = 'sina'
  #defaults
  app_id       = 3743872231 #please do not use it to do something bad :)
  width        = 80
  
  def load(self):
    file_path = os.path.expanduser('~/.pybo')
    cp = ConfigParser.ConfigParser()
    cp.read(file_path)
    if not cp.has_section(self.SECTION):
      cp.add_section(self.SECTION)
    
    attrs = ['username','password','app_id','width']
    #check
    self.cp_attr(cp,attrs)
    self.raw_attr(attrs[:3])
    #update
    self.update_attr(cp,attrs)
    f = open(file_path,'w')
    cp.write(f)
    f.close()

  def update_attr(self,config_parser,options):
    for attr in options:
      config_parser.set(self.SECTION,attr,getattr(self,attr,''))

  def cp_attr(self,config_parser,options):
    for attr in options:
      if config_parser.has_option(self.SECTION,attr):
        setattr(self,attr,config_parser.get(self.SECTION,attr))

  def raw_attr(self,options):
    for attr in options:
      while not getattr(self,attr,None):
        setattr(self,attr,raw_input('%s : ' % attr))
  
  def __getitem__(self,key):
    if key in ('username','password'):
      return getattr(self,key)
    if key == 'width':
      try:
        return int(self.width)
      except:
        return 80
    if key == 'app_id':
      try:
        return int(self.app_id)
      except:
        return 3743872231


if __name__ == '__main__':
  config = Config()
  config.load()

  weibo = Weibo(config)
  pager(weibo)
