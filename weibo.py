# -*- encoding: utf-8 -*-
import base64,urllib,urllib2,json

render_name  = lambda s: '\033[94m%s\033[m' % s
render_error = lambda s: '\033[41m\033[37m %s \033[m' % s

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
