#! /usr/bin/python
# -*- encoding: utf-8 -*-
import sys,cmd,re
import os
import ConfigParser
import base64
import json
import urllib2,urllib

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

  def request(self, api, params):
    req = urllib2.Request(self.URLS[api],urllib.urlencode(params))
    req.add_header("Authorization",self.auth_header)
    try:
      handle = urllib2.urlopen(req)
    except:
      content = '{}'
    else :
      content = handle.read()
      handle.close()
    content = json.loads(content)
    return content

  def format_line(self,line,tab_index = 0):
    step = width = self.config['width'] - tab_index
    line = line.encode('gb18030')

    lines = []
    start = 0
    while line[start:]:
      try:
        s = line[start:start+step].decode('gb18030')
        lines.append('%s%s' % (' '*tab_index,s))
        start += step
        step = width
      except:
        step = width - 1

    return lines

  def go_to_top(self):
    self.max_id = 0
    return self.timeline()

  def timeline(self):
    params = {'source':'3743872231','max_id':self.max_id}
    content = self.request('timeline',params)

    lines = []
    if not content or len(content) == 0:
      lines.append('no tweet')
      return lines

    author_color = self.config['author_color']
    end_color  = self.config['end_color']

    for tweet in content:
      tab = 0
      while tweet:
        text = tweet['text']
        username = tweet['user']['name']
        lines.append('%s%s%s%s' % (' '*tab,author_color,username,end_color))
        lines.extend(self.format_line(text,tab))
        #if tweet.get('original_pic'):
        #  lines.extend(self.format_line('Pic: '+tweet.get('original_pic'), tab))
        tab += 4
        tweet = tweet.get('retweeted_status')

      lines.append('')

    self.max_id = int(content[-1]['id']) + 1
    return lines

class Config():
  SECTION = 'weibo'
  COLORS = {}
  COLORS['HEADER' ] = '\033[95m'
  COLORS['BLUE'   ] = '\033[94m'
  COLORS['GREEN'  ] = '\033[92m'
  COLORS['WARNING'] = '\033[93m'
  COLORS['FAIL'   ] = '\033[91m'
  COLORS['END'    ] = '\033[0m'
  #defaults
  author_color   = 'BLUE'
  end_color    = 'END'
  app_id       = '3743872231' #please do not use it to do something bad :)
  width        = '80'
  
  def load(self):
    file_path = os.path.expanduser('~/.weibo')
    cp = ConfigParser.ConfigParser()
    cp.read(file_path)
    if not cp.has_section(self.SECTION):
      cp.add_section(self.SECTION)
    
    attrs = ['username','password','author_color','app_id','width']
    #check
    self.cp_attr(cp,attrs)
    self.raw_attr(attrs[:2])
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
    if key in ('author_color','end_color'):
      return self.__color('author_color') and self.__color(key)
    if key == 'width':
      try:
        return int(self.width)
      except:
        return 80

  def __color(self,key):
    return self.COLORS.get(getattr(self,key,'').upper(),'')


if __name__ == '__main__':
  config = Config()
  config.load()

  weibo = Weibo(config)
  print '\n'.join(weibo.timeline())
