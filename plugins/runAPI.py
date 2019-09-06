from nonebot import on_command, CommandSession
import sys
import importlib
# on_command 装饰器将函数声明为一个命令处理器

@on_command('run', only_to_me=True)
async def _(session: CommandSession):
    args = session.current_arg.split(' ')
    try:
        if session.ctx['user_id'] in session.bot.config.PROGRAMMERS:
            sys.path.append('..')
            try:
                Api = importlib.reload(sys.modules['Api'])
            except KeyError or ImportError:
                Api = importlib.import_module("Api")
            if args[0] in dir(Api):
                await eval("Api." + args[0])(*args[1:])
    except KeyError:
        pass
    return
