#-*- coding=utf-8 -*-
import os
import sys
import json
import builder

class Director():
    def __init__(self, builder):
        self.builder = builder
    
    def buildTpl(self):
        pass
        
        

class Activity(Director):

    def buildTpl(self):
        self.builder.buildTitle()
        self.builder.buildPlaycnt()

        
class MiniVideo(Director):

    def buildTpl(self):
        self.builder.buildTitle()
        self.builder.buildVideoInfo()
        self.builder.buildScheme()
        
    

def unit_test():
    context = {'feed_id': 'sv_activity_2018', 'title': 'Baidu Feed'}
    b = builder.MiniActivity(context)
    d = Activity(b) 
    d.buildTpl()
    t = b.getTpl()
    print t

        


if __name__ == '__main__':
    unit_test()
