# -*- coding: utf-8 -*-
import urwid
import config

class TweetWidget(urwid.WidgetWrap):
    def __init__(self, tweet, state):
        self.state = state

        tweet_block = []
        if tweet.get('user'):
            tweet_block.append(
                # username and post state
                ('flow', urwid.Padding(urwid.Text([
                        tweet['user'],
                        u'  ',
                        ('brown', tweet['extra'])
                    ]),  
                    left = tweet['indent'])))
        tweet_block.append(
            # post
            ('flow', urwid.Padding(
                urwid.AttrWrap(urwid.Text(tweet['post']), 'body', 'focus'),
                left = tweet['indent'])))

        if tweet['is_leaf'] :
            tweet_block.append((urwid.Text(u'')))

        w = urwid.Pile(tweet_block)
        w.set_focus(1)
        self.__super.__init__(w)

    def selectable (self):
        return True

    def keypress(self, size, key):
        if key is 'j':
            return 'down'
        elif key is 'k':
            return 'up'
        return key


    """
    if input is 'enter':
        focus = listbox.get_focus()[0].content
        view.set_header(urwid.AttrWrap(urwid.Text(
            'selected: %s' % str(focus)), 'head'))
    """

def loop(tweets):
    def keystroke (input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def keyfilter(input, raw):
        footer.set_text(u"Passed: %s " % input)
        if type(input[0]) is tuple and input[0][0] == 'mouse press':
            if input[0][1] is 4:
                return ['up']
            elif input[0][1] is 5:
                return ['down']
        return input

    items = []
    for tweet,state in tweets:
        items.append(TweetWidget(tweet, state))

    footer = urwid.Text(u'')
    listbox = urwid.ListBox(urwid.SimpleListWalker(items))
    view = urwid.Frame(urwid.AttrWrap(listbox, 'body'), footer = footer)
    loop = urwid.MainLoop(view, config.palette, input_filter=keyfilter, unhandled_input=keystroke)
    loop.run()
