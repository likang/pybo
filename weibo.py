#! /usr/bin/python
# -*- encoding: utf-8 -*-
import sys,cmd,re
import base64
import json
import urllib2,urllib
from urlparse import urlparse
from pydoc import pager

class Weibo(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self)
    self.prompt = 'Weibo: '

    username = 'username'
    password = 'pass'
    base64string = base64.encodestring('%s:%s' % (username,password))[:-1]
    self.auth_header = 'Basic %s' % base64string
    self.max_id = 0

  def help_quit(self):
    print "Quits the program"
  def do_quit(self,line):
    sys.exit()

  def help_next_page(self):
    print "print next page"
  def do_next_page(self,pages):
    url = 'http://api.t.sina.com.cn/statuses/friends_timeline.json'
    params = {'source':'3743872231','max_id':self.max_id}
    req = urllib2.Request(url,urllib.urlencode(params))
    req.add_header("Authorization",self.auth_header)
    try:
      handle = urllib2.urlopen(req)
    except IOError, e:
      print 'seems error'
      sys.exit(1)
    content = handle.read()
    content = json.loads(content)
    if not content or len(content) == 0:
      print 'no tweet'
      return

    lines = []
    for tweet in content:
      text = tweet['text']
      username = tweet['user']['name']
      lines.append('%s : %s' % (username,text) )
      tweet = tweet.get('retweeted_status')
      if not tweet:
        lines.append('')
        continue
      lines.append('  |')
      text = tweet['text']
      username = tweet['user']['name']
      lines.append('   -- %s : %s\n' % (username,text))
      #print '\n'.join(lines)
    self.max_id = int(content[-1]['id']) + 1
    pager('\n'.join(lines).encode('utf-8'))
      
        

  def help_next_line(self):
    print "print next line"
  def do_next_line(self,params):
    print "line"

  def help_gg(self):
    print "go to top"
  def do_gg(self,params):
    self.max_id = 0
    self.do_next_page(3)
  
  def emptyline(self):
    self.do_next_page(3)

  #alias
  do_q = do_quit
  do_n = do_next_line

if __name__ == '__main__':
  weibo = Weibo()
  weibo.do_next_page(1)
  weibo.cmdloop()
