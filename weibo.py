# -*- encoding: utf-8 -*-
import base64,urllib,urllib2,json
from config import Config


class Weibo():

  def __init__(self):
    self.config = Config(self.__class__.__name__)
    self.error  = ''

  def render_name(self, name):
    return '\033[94m%s\033[m' % name

  def render_error(self, error):
    return '\033[41m\033[37m %s \033[m' % error

  def json_request(self, url, params):
    req = self.wrap_request(url, params)
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

