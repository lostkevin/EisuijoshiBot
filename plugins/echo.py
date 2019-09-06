from nonebot import on_command, CommandSession, get_bot

# on_command 装饰器将函数声明为一个命令处理器

@on_command('echo', only_to_me=False)
async def echo(session: CommandSession):
    result = await session.send(session.state.get('message') or session.current_arg)
    return
