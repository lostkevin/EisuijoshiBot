from nonebot import on_notice, NoticeSession, get_bot, on_command, CommandSession

@on_notice('group_increase')
async def _(session: NoticeSession):
    try:
        if session.ctx['user_id'] == session.ctx['self_id']:
            # bot 被邀请入群
            if str(session.ctx['group_id']) not in session.bot.config.ALLOWED_GROUP:
                params = {'group_id': session.ctx['group_id']}
                await get_bot().call_action('set_group_leave', **params)
    except KeyError:
        return
    return

@on_command('group', only_to_me=False)
async def _(session: CommandSession):
    if session.ctx['sender']['user_id'] in session.bot.config.SUPERUSERS:
        session.bot.config.ALLOWED_GROUP.append(session.current_arg)
        await session.send("添加成功!")
