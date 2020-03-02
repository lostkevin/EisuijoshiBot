import importlib
import sys
from nonebot import on_command, CommandSession, load_plugins, get_bot, scheduler
import subprocess
import plugins.clanbattle
@on_command('reboot', only_to_me=False)
async def reboot(session: CommandSession):
    if hasattr(session.bot.config, 'PROGRAMMERS'):
        if session.ctx['sender']['user_id'] in session.bot.config.PROGRAMMERS:
            try:
                plugins.clanbattle.cb_clean()
                scheduler.remove_all_jobs()
                subprocess.check_call(['git', 'pull' , session.bot.config.REPO])
                get_bot().config = importlib.reload(sys.modules['config'])
                load_plugins('./plugins','plugins', True)
                await session.send('更新成功')
            except subprocess.CalledProcessError:
                await session.send('git失败,请检查是否安装git')
    else:
        return
