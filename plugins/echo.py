from nonebot import on_command, CommandSession
from EisuijoshiBot.plugins.utils.pictool import Parser
# on_command 装饰器将函数声明为一个命令处理器

@on_command('echo', only_to_me=False)
async def echo(session: CommandSession):
    await session.send(session.state.get('message') or session.current_arg)
    print(Parser(session.current_arg))
    return
