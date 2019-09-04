from nonebot import on_command, CommandSession

@on_command('test', only_to_me=False)
async def echo(session: CommandSession):
    await session.send('更新成功')
