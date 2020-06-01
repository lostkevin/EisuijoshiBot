from nonebot import on_command, CommandSession, scheduler, logger, get_bot
import imghdr
import aiofiles
import aiohttp
import ssl
import os.path
import random
import shutil
import json
from utils.Parser import Parser

def _toCQImg(filename: str)->str:
    return "[CQ:image,file=" + filename + "]"

def _makeMessage(count: int) -> str:
    res = random.sample(pic_data.keys(), count)
    msg = ""
    for r in res:
        msg += _toCQImg(r) + '\n'
        data = pic_data[r]
        if data['pid'] != -1:
            msg += 'pid:{}\nuid:{}\n'.format(data['pid'], data['uid'])
    return msg

coolq_dir = '../'
img_dir = 'data/image/'
pic_data = {}
if os.path.exists('./data/imgData.json'):
    with open('./data/imgData.json') as f:
        pic_data = json.load(f)
        f.close()

@scheduler.scheduled_job('interval', seconds=30, max_instances=1)
async def save_imgData():
    with open('./data/imgData.json', 'w') as f:
        json.dump(pic_data, f)
        f.close()

@scheduler.scheduled_job('interval', seconds=4, max_instances=5)
async def fetch_pic(local = False):
    params = {"apikey": "493552455e8c4aab471b45", "r18": "false", "size1200":"true", "num": 5}
    async with aiohttp.request("GET", "https://api.lolicon.app/setu/", params=params) as r:
        res = json.loads(await r.text(encoding="utf-8"))['data']
    for data in res:
        try:
            async with aiohttp.request("GET", data['url']) as r:
                filename = data['url'].split("/")[-1]
                filepath = os.path.join(coolq_dir, img_dir, filename)
                if not os.path.exists(filepath):
                    async with aiofiles.open(filepath, 'wb') as f:
                        img = await r.read()
                        await f.write(img)
                        await f.close()
                        if imghdr.what(filepath) is None:
                            continue
                    pic_data[filename] = data
        except ssl.SSLError:
            pass

@on_command('setu', only_to_me=False)
async def _(session: CommandSession):
    if session.ctx["message_type"] == 'group':
        if session.ctx['sender']['role'] in [ 'admin' ] and session.current_arg == 'on':
            if session.ctx['group_id'] in session.bot.config.SETU_BAN:
                session.bot.config.SETU_BAN.remove(session.ctx['group_id'])
            await session.send("功能已开启!")
            return
        elif session.current_arg == 'off':
            if session.ctx['group_id'] not in session.bot.config.SETU_BAN:
                session.bot.config.SETU_BAN.add(session.ctx['group_id'])
            await session.send("功能已关闭!")
            return
        if session.current_arg == 'status':
            await session.send("当前状态: %s" % ("开启" if session.ctx['group_id'] not in session.bot.config.SETU_BAN else "关闭"))
            return
        if session.ctx['group_id'] in session.bot.config.SETU_BAN:
            return
    try:
        count = int(session.current_arg)
    except ValueError as e:
        count = 1
    await session.send(_makeMessage(count))

@on_command('upload', only_to_me=False)
async def __(session: CommandSession):
    CQs = Parser(session.current_arg)
    cnt = 0
    for cqc in CQs:
        if cqc['CQ'] == "image":
            params = {'file':cqc['file']}
            pic_data[cqc['file']] = {'pid': -1, 'uid': -1}
            cnt += 1
    await session.send(('一共%d张, 社保了' % cnt) if cnt > 0 else '色图呢,让我康康!')
