from nonebot import  on_command, CommandSession, get_bot

@on_command('test', only_to_me=False)
async def query(session: CommandSession):
    async def send(dict):
        await session.send(str(dict))
    request = {
        'slots' : [{
            'account_id': 113998,
            'start_point': 30000
        } ],
        'random_position': True,
        'open_live': True
    }
    await get_bot().config.mgr.send('createContestGame', send, request)