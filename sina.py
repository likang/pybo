# -*- encoding: utf-8 -*-

import os
import config
import time
from sinapi import APIClient as SinaClient
from util import unicode_line_folding

class sina:
    def __init__(self):
        self.auth_file_path = 'tmp/sinauth'
        self.timeline_max_id = 0
        self.client = SinaClient(
                app_key = '3743872231',
                app_secret = None,
                redirect_uri = 'http://pipeline.sinaapp.com/pybo/sina_callback.php',
                version = '1')
        self.init_access_token()
    
    def init_access_token(self):
        if os.path.exists(self.auth_file_path):
            f = open(self.auth_file_path, 'r')
            lines = f.readlines()
            f.close()
        else:
            print 'Please open the url, login to sina(if needed), then folow the guide on the website\n'
            print self.client.get_authorize_url(), '\n'

            response = raw_input()
            lines = response.split(':')
            lines[1] = str(int(time.time()) + int(lines[1]))

            f = open(self.auth_file_path, 'w')
            f.writelines('\n'.join(lines))
            f.close()

        access_token = lines[0]
        expires_in   = int(lines[1])
        self.userid = int(lines[2])
        self.client.set_access_token(access_token, expires_in)

    def index(self):
        return self.timeline();

    def timeline(self):
        response = self.client.statuses__home_timeline().statuses

        lines = []
        for tweet in response:
            indent = u''

            while tweet:
                line_block = []
                text = tweet.text
                username = tweet.user.name
                line_block.append(indent + username)
                line_block.extend(unicode_line_folding(text, config.width, indent))

                tweet = tweet.get('retweeted_status', None)
                if tweet:
                    indent += u'    '
                else:
                    line_block.append(u'')

                lines.append(line_block)

        return lines

