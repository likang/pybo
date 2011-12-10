# -*- encoding: utf-8 -*-
from weibo import Weibo

class Sina(Weibo):
  def wrap_request(self, url, params):
    req = urllib2.Request(url, urllib.urlencode(params))
    req.add_header('Authorization','OAuth2 %s' % self.config.access_token)
    return req

  def do_timeline(self):
    if not self.m_timeline:
      self.m_timeline = Timeline(self)
    self.module = self.m_timeline
    self.lines = self.m_timeline.lines

  def more(self):
    self.module.more()

class Timeline:
  def __init__(self, weibo):
    self.weibo  = weibo
    self.lines  = []
    self.max_id = 0

  def more(self):
    url = 'https://api.weibo.com/2/statuses/friends_timeline.json'
    params = {'max_id':self.max_id,'count':200}
    content = self.weibo.json_request(url, params)

    if not content or len(content) == 0:  return

    lines = []
    for tweet in content:
      indent = 0
      while tweet:
        text = tweet['text']
        username = tweet['user']['name']
        lines.append(' '*indent + self.weibo.render_name(username))
        lines.extend(self.weibo.tidy_up(text,indent))
        indent += 4
        tweet = tweet.get('retweeted_status')

      lines.append('')

    self.max_id = int(content[-1]['id']) + 1
    self.lines.extend(lines)
