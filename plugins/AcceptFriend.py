from nonebot import on_request, RequestSession, get_bot, on_command, CommandSession

_state = False

@on_request('friend')
async def _(session: RequestSession):
    if hasattr(session.bot.config, 'friendState') and session.bot.config.friendState:
        await session.approve()
        return
    if str(session.ctx['user_id']) in session.bot.config.ALLOWED_FRIEND:
        await session.approve()
    else:
        await session.reject('请联系管理员')

@on_command('friend', only_to_me=True)
async def _(session: CommandSession):
    if session.ctx['sender']['user_id'] in session.bot.config.SUPERUSERS:
        if session.current_arg == 'off':
            session.bot.config.state = True
        if session.current_arg == 'on':
            session.bot.config.state = False
        session.bot.config.ALLOWED_FRIEND.append(session.current_arg)
        await session.send("添加成功!")
