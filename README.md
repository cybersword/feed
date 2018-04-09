# 设计初衷
用科技让视频Feed迭代更简单

* 将复杂的产品设计留给PM
* 将复杂的测试覆盖留给QA
* 将复杂的能力支持留给RD
## 痛点
* 稳定性
* 需求变更
* 联调
* 产品验收
## 解决方案
> 把Feed做成“积木”，写一个“引擎”，能根据“图纸”把零散的积木搭起来，
> 然后写一个生成器来生成这个图纸，生成器最终面向PM甚至AI。

- 功能建设
	* 将功能封装成一个个“能力”（Builder）
	* 将功能的组织形式封装成一个个Director
	* 提供一个UI，维护Builder和Director的触发条件，形成配置文件
	* 提供一个自动化引擎，根据配置组装模板
	* 条件、展示分离
- 基础设施
	* Mock数据，支持联调和产品验收
	* 模板样式管理
	* 展示条件管理
	* 测试case管理（回归测试）


## 里程碑
* 初步设计方案
* demo
* Builder & Director 开发及管理（模板样式、各种能力）
* 研发测试Mock平台
* 回归测试平台、线上监控平台
* 配置文件界面化，提供web UI
* 自动迭代，根据实验结论或线上日志分析，自动全量某个实验？

# 模块组成
## Case Manager 
### 表结构
case_id, seq, feed_id, os, version, sid, location, ext)
### 输入
case_id
### 输出
feed_id list + common params

## Condition Manager
条件管理, 触发条件到规则的映射
### conf文件（JSON）
```javascript
{
	"condition": {
		"common": {
			"sid": "101_202",
			"os": "Android"
		},
		"meta": {
			"videotype": 3
		}
	},
	"rule_id": "mini_01"
}
```
### 输入
resource params + common params
### 输出
rule_id

## Rule Manager
规则管理, 规则到展现结果的映射
### conf文件（JSON）
```javascript
{
    "data": null,
    "builder": "MiniActivityPlaycntNumOnly",
    "director": "Activity"
}
```
### 输入
rule_id
### 输出
director class + builder class

## Builder & Director Manager
生成器管理, Builder提供具体能力, Director提供组织形式
```python
class Builder():
	"""基类"""
    def __init__(self, context):
        self.context = context
        self.tpl = {
            'id': context['feed_id'],
            'data': {},
        }
    def getTpl(self):
        return self.tpl

    def buildTitle(self):
        self.tpl['data']['title'] = self.context['title']

class MiniActivity(Builder):
	"""小视频运营模板"""
    def buildTitle(self):
	    """重写标题逻辑"""
        self.tpl['data']['title'] = '#' + self.context['title'] + '#'

    def buildPlaycnt(self):
        self.tpl['data']['playcnt'] = {'count': 1234567, 'text': 'views'}


class MiniActivityPlaycntNumOnly(MiniActivity):
	"""播放次数文案不展示"""
    def buildPlaycnt(self):
        self.tpl['data']['playcnt'] = {'count': 1234567}


class MiniVideo(Builder):
    def buildVideoInfo(self):
        self.tpl['data']['videoinfo'] = {'title': self.tpl['data']['title'], 'clarityUrl': []}

    def buildScheme(self):
        self.tpl['data']['cmd'] = 'baiduboxapp://...' 
```
```python
class Director():
	"""组装器基类"""
    def __init__(self, builder):
        self.builder = builder

    def buildTpl(self):
        pass

class Activity(Director):
	"""运营模板类"""
    def buildTpl(self):
        self.builder.buildTitle()
        self.builder.buildPlaycnt()


class MiniVideo(Director):
	"""小视频模板类"""
    def buildTpl(self):
        self.builder.buildTitle()
        self.builder.buildVideoInfo()
        self.builder.buildScheme()
```


## Engine
执行引擎
### 输入
feed_id (list) + common params
### 输出
tpl (list)
```
feed_id + common params
    ==> resource params + common params
    ==> rule_id + context
    ==> director class + builder class + context
    ==> tpl
```
### 主逻辑
```python
#-*- coding=utf-8 -*-
import os
import sys
import json
import builder
import director

def get_context(feed_id):
    context = {'feed_id': feed_id, 'title': 'Baidu Feed'}
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
```

## Mock Platform
### 输入
case_id
### 输出
tpl list
