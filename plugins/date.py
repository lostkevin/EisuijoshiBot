from nonebot import on_command, CommandSession
import datetime

# on_command 装饰器将函数声明为一个命令处理器
@on_command('date', only_to_me=False)
async def date(session: CommandSession):
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await session.send('当前时间:' + nowTime)
