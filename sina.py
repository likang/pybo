# -*- encoding: utf-8 -*-

import os
import config
import time
from sinapi import APIClient as SinaClient

class sina:
    def __init__(self):
        self.auth_file_path = 'tmp/sinauth'
        self.timeline_max_id = 0
        self.client = SinaClient('3743872231',None,'http://pipeline.sinaapp.com/pybo/sina_callback.php')
        self.init_access_token()
    
    def init_access_token(self):
        if os.path.exists(self.auth_file_path):
            lines = open(self.auth_file_path, 'r').readlines()
        else:
            print 'Please open the url, login to sina(if needed), then folow the guide on the website\n'
            print self.client.get_authorize_url(), '\n'
            response = raw_input()
            lines = response.split(':')
            lines[1] = str(int(time.time()) + int(lines[1]))
            f = open(self.auth_file_path, 'w')
            f.writelines('\n'.join(lines))
            f.close()

        access_token = lines[0].strip()
        expires_in   = int(lines[1].strip())
        self.client.set_access_token(access_token, expires_in)

    def timeline(self):
        return response = self.client.statuses__public_timeline()
        """
        lines = []
        for tweet in response:
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
        """

