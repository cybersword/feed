
# Case Manager (case_id, seq, feed_id, os, version, sid, location, ext)
 case_id => feed_id list + common params 

# Condition Manager (conf json)
 条件管理, 触发条件到规则的映射
 resource params + common params => rule_id

# Rule Manager (conf json)
 规则管理, 规则到展现结果的映射
 rule_id => director class + builder class

# Builder & Director Manager
 生成器管理, Builder提供具体能力, Director提供组织形式

# Engine
 执行引擎
 feed_id (list) + common params ==Rule + Builder==> tpl list
    feed_id + common params
    ==> resource params + common params
    ==> rule_id + context
    ==> director class + builder class + context
    ==> tpl

# Mock Platform
 case_id ==Case + Engine==> tpl list
