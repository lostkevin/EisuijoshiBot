from nonebot import on_command, CommandSession, load_plugins
import subprocess
import sys
import os
import platform

@on_command('reboot', only_to_me=False)
async def date(session: CommandSession):
    if hasattr(session.bot.config, 'PROGRAMMERS'):
        if session.ctx['sender']['user_id'] in session.bot.config.PROGRAMMERS:
            await session.send('机器人即将更新')
            try:
                subprocess.check_call('git pull %s' % session.bot.config.REPO)
                load_plugins('./plugins', 'plugins')
                # python = sys.executable
                # if platform.system() == 'Windows':
                #     os.spawnl(os.P_WAIT, python, python, sys.argv[0])
                #     sys.exit()
                # elif platform.system() == 'Linux':
                #     os.execl(python, python, *sys.argv)
            except subprocess.CalledProcessError:
                await session.send('git失败,请检查是否安装git')
    else:
        return
