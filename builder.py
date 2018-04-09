#-*- coding=utf-8 -*-
import os
import sys

class Builder():
    def __init__(self, context):
        self.context = context
        self.tpl = {
            'id': context['feed_id'],
            'data': {},
        }
        
    def getFeedID(self):
        return self.context['feed_id']

    def test(self):
        print 'tpl'

    def getTpl(self):
        return self.tpl

    def buildTitle(self):
        self.tpl['data']['title'] = self.context['title']


class Text(Builder):
    def test(self):
        print 'text'
    

class Image(Builder):
    def test(self):
        print 'image'
    

class MiniActivity(Builder):
    def test(self):
        print 'mini activity'

    def buildTitle(self):
        self.tpl['data']['title'] = '#' + self.context['title'] + '#'

    def buildPlaycnt(self):
        self.tpl['data']['playcnt'] = {'count': 1234567, 'text': 'views'}
        
        
class MiniActivityPlaycntNumOnly(MiniActivity):

    def buildPlaycnt(self):
        self.tpl['data']['playcnt'] = {'count': 1234567}


class MiniVideo(Builder):
    def test(self):
        print 'mini video'

    def buildVideoInfo(self):
        self.tpl['data']['videoinfo'] = {'title': self.tpl['data']['title'], 'clarityUrl': []}
    
    def buildScheme(self):
        self.tpl['data']['cmd'] = 'baiduboxapp://...'

def unit_test():
    pass


if __name__ == '__main__':
    unit_test()
