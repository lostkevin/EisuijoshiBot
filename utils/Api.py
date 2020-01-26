from nonebot import get_bot
from typing import  Any

async def get_stranger_info(*args) -> Any:
    params = { 'user_id':int(args[0]) }
    result = await get_bot().call_action('get_stranger_info', **params)
    return result

async def send_private_msg(*args):
    params = { 'user_id': int(args[0]), 'message': ' '.join(args[1:])}
    return await get_bot().call_action('send_private_msg', **params)

async def set_group_leave(*args):
    params = {'group_id': int(args[0])}
    await get_bot().call_action('set_group_leave', **params)

async def send_group_msg(*args):
    params = {'group_id': int(args[0]), 'message': ' '.join(args[1:])}
    await get_bot().call_action('send_group_msg', **params)

async def send_local_pic():
    return

async def get_image(filename: str) -> str:
    params = {'file':filename}
    return await  get_bot().call_action('get_image', **params )