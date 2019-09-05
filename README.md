# EisuijoshiBot

永水高校使用的QQ管理机器人,用于简化报名\注册等一系列日常工作
## Environment
+ Docker
+ Wine CoolQ
+ CQHttpApi
+ nonebot
    + 为支持重启功能,用modified_lib/下的plugin.py覆盖nonebot内的plugin.py
+ mySQL + python connector
    + pip install pymysql

## CQHttpApi
主动调用Api使用以下指令:
    
    await get_bot().call_action(action, **params)

如:

    params = {'group_id': session.ctx['group_id']}
    await get_bot().call_action('set_group_leave', **params)
具体使用方式以及参数说明见[CQHttpApi](https://cqhttp.cc/docs/)文档