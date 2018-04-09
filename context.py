#-*- coding=utf-8 -*-
import os
import sys
import json

def get(feed_id):
    context = {'feed_id': feed_id} 
    if feed_id[:12] == 'sv_activity_':
        context['title'] = '运营模板'
    else:
        context['title'] = '小视频模板'
    
    return context


def main():
    feed_id = 'sv_activity_2018'
    context = get_context(feed_id)
    b = builder.MiniActivity(context)
    d = director.Activity(b)
    d.buildTpl()
    tpl = b.getTpl()
    print tpl
    rule_list = ['mini_01', 'mini_02', 'mini_03']
    for rule_name in rule_list:
        rule_path = 'rule/' + rule_name + '.json' 
        with open(rule_path,'r') as rule_json:
            print '=' * 10
            rule = json.load(rule_json)
            print rule
            print '-' * 10
            b = eval('builder.' + rule['builder'] + '(context)')
            d = eval('director.' + rule['director'] + '(b)')
            d.buildTpl()
            t = b.getTpl()
            print t
            print '\n'


if __name__ == '__main__':
    main()
