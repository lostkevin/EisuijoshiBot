from nonebot import CommandSession, on_command

@on_command('浇水')
async def _watering(session: CommandSession):
    pass

@on_command('参拜')
async def _visit(session: CommandSession):
    pass

@on_command(['好感度', '契约'])
async def _query(session: CommandSession):
    pass

@on_command('成长值')
async def _growth(session: CommandSession):
    pass

@on_command('声望')
async def _fame(session: CommandSession):
    pass
