from nonebot import on_command, CommandSession


# on_command 装饰器将函数声明为一个命令处理器
<<<<<<< HEAD
@on_command('echo', only_to_me=False)
=======
@on_command('testECHO', only_to_me=False)
>>>>>>> db665315f370216c7054711dcf3ee006e7b5032f
async def echo(session: CommandSession):
    await session.send(session.state.get('message') or session.current_arg)
