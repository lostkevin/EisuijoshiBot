from nonebot import on_command, CommandSession
from nonebot import permission

# on_command 装饰器将函数声明为一个命令处理器
@on_command('查看报名', only_to_me = False)
async def parser(session: CommandSession):
    senderInfo=session.ctx['sender']
    if senderInfo['user_id'] in session.bot.config.SUPERUSERS:
        await session.send('并不知道有没有人报名，但是你是%s, QQ: %d, 而且是超级用户' % (senderInfo['nickname'], senderInfo['user_id']))
        if session.ctx['message_type'] == 'group':
            await session.send('并且是群聊状态')
    elif session.ctx['message_type'] == 'group':
        await session.send('并不知道有没有人报名，但是你是%s, QQ: %d, 并且%s是群管理员' % (senderInfo['nickname'], senderInfo['user_id'], 
        '不' if (senderInfo['role'] == 'member')  else '' ))

@parser.args_parser
async def _(session: CommandSession):
    print('text:')
    print(session.current_arg_text)


