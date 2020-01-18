from nonebot import on_command, CommandSession

@on_command('help', only_to_me=False)
async def _(session: CommandSession):
    help_text = '--帮助--\n'
    help_text += '\'?\', \'？\'触发命令\n'
    help_text += '\'pl\' \'pl 1112345678999m\' 引用天凤牌理\n'
    help_text += '待机 查看大会室准备情况\n'
    help_text += '大会室 查看大会室\n'
    help_text += '还有一些奇怪的功能等待发现...'
    await session.send(help_text)
    return
