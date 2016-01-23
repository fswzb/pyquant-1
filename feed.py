#!/usr/bin/env python
# encoding: utf-8
# reads the stock list from feed dir
# feeds store the stock you have pick from the result of algorithm you used

class feed(object):
    def __init__(self):

        self.WKDIR = '/home/way/feed/'
#make sure your file comes only with stock num, like 000001, and one stock num one line,
#store the same kind feeds in their respective txt file
    def get_feed(self,feed_type):
        feed_file = self.WKDIR + feed_type + '.txt'
        f = open(feed_file)
        lines = f.readlines()
        for line in lines:
            line = line[:6]
            yield line
