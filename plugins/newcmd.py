from nonebot import on_command, CommandSession


# on_command 装饰器将函数声明为一个命令处理器

@on_command('aaa', only_to_me=False)
async def echo(session: CommandSession):
    await session.send(session.state.get('message') or session.current_arg)
