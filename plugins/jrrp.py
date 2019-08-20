from nonebot import on_command, CommandSession, MessageSegment
import datetime
import string

# on_command 装饰器将函数声明为一个命令处理器
@on_command('jrrp', aliases=['JRRP', '今日人品'], only_to_me=False)
async def jrrp(session: CommandSession):
    nowTime=datetime.datetime.now().date()
    rp = hash(session.ctx['sender']['user_id'] + nowTime.day * nowTime.month * nowTime.year ) % 100
    if session.ctx['message_type'] == 'group':
        user = MessageSegment.at(session.ctx['sender']['user_id'])
        await session.send("%s\n今日狗力：[%d]" % (user, rp))
    else:
        user = ''
        await session.send("今日狗力：[%d]" % rp)
    
