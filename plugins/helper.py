from nonebot import on_command, CommandSession

@on_command('help', only_to_me=False)
async def _(session: CommandSession):
    help_text = '--帮助--\n'
    help_text += '\'?\', \'？\'触发命令\n'
    help_text += '\'pl\' \'pl 1112345678999m\' 引用天凤牌理\n'
    help_text += '\'补偿计算\' cn/tw/jp 剩余血量 伤害 计算PCR会战补偿时间'
    await session.send(help_text)
    return
