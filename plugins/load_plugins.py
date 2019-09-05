from nonebot import on_command, CommandSession, load_plugins
import subprocess

@on_command('reboot', only_to_me=False)
async def reboot(session: CommandSession):
    if hasattr(session.bot.config, 'PROGRAMMERS'):
        if session.ctx['sender']['user_id'] in session.bot.config.PROGRAMMERS:
            try:
                subprocess.check_call('git pull %s' % session.bot.config.REPO)
                load_plugins('./plugins','plugins', True)
                await session.send('更新成功')
            except subprocess.CalledProcessError:
                await session.send('git失败,请检查是否安装git')
    else:
        return
