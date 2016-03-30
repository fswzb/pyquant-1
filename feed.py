#!/usr/bin/env python
# encoding: utf-8
# reads the stock list from feed dir
# feeds store the stock you have pick from the result of algorithm you used
"""
USAGE: feeds = feed('feed_type'), for feed in feeds.load(): TRADE with feed.
len(feeds) return the number of feeds
"""
class feed(object):
    def __init__(self, feed_type):
        self.feed_type = feed_type
        self.WKDIR = '/home/way/feed/'
#make sure your file comes only with stock num, like 000001, and one stock num one line,
#store the same kind feeds in their respective txt file
        feed_file = self.WKDIR + self.feed_type
        f = open(feed_file)
        self.lines = f.readlines()
        f.close()
    def load(self):
        feeds = []
        for line in self.lines:
            line = line[:6]
            feeds.append(line)
        return feeds
    def __len__(self):
        return len(self.lines)

