from nonebot import on_request, RequestSession, get_bot, on_command, CommandSession

@on_request('friend')
async def _(session: RequestSession):
    if str(session.ctx['user_id']) in session.bot.config.ALLOWED_FRIEND:
        await session.approve()
    else:
        await session.reject('请联系管理员')

@on_command('friend', only_to_me=True)
async def _(session: CommandSession):
    if session.ctx['sender']['user_id'] in session.bot.config.SUPERUSERS:
        session.bot.config.ALLOWED_FRIEND.append(session.current_arg)
        await session.send("添加成功!")
