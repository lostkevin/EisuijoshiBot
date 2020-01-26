import json
import asyncio
from utils import dhs
from nonebot import get_bot

async def init():
    async def heartbeat():
        while True:
            await get_bot().config.mgr.send('startManageGame', None)
            await asyncio.sleep(60)
    if not hasattr(get_bot().config, 'mgr'):
        get_bot().config.mgr = dhs.DHSMgr()
        with open('.\data\key.json') as f:
            User = json.load(f)
        asyncio.create_task(get_bot().config.mgr.run())
        await get_bot().config.mgr.login(User['user'], User['passwd'])
        await get_bot().config.mgr.send('manageContest', None, {'unique_id': 2203})
        await get_bot().config.mgr.send('startManageGame', None)
        asyncio.create_task(heartbeat())