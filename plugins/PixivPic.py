from nonebot import on_command, CommandSession, scheduler, logger, get_bot
import imghdr
import aiofiles
import aiohttp
import ssl
import  os.path
import  random
import shutil
import json
from utils.Parser import Parser

pic_pool = []
pic_dir = './data/Image/'
pic_local = os.listdir(pic_dir)
if len(pic_local) > 6:
    for i in range(0, 6):
        filename = pic_local.pop(random.randint(0, len(pic_local) - 1))
        logger.info("successfully load %s into pool" % filename)
        p = os.path.abspath(os.path.join(pic_dir, filename))
        pic_pool.append("[CQ:image,file=file:///"+ ("Z:/" if p.startswith('/') else "") + p + "]")

@scheduler.scheduled_job('interval', seconds=4, max_instances=5)
async def fetch_pic(local = False):
    if local:
        for j in range(0, 6):
            filename = pic_local.pop(random.randint(0, len(pic_local) - 1))
            logger.info("successfully load %s into pool" % filename)
            p = os.path.abspath(os.path.join(pic_dir, filename))
            pic_pool.append("[CQ:image,file=file:///" + ("Z:/" if p.startswith('/') else "") + p + "]")
            return
    if len(pic_pool) >= 10:
        return
    async with aiohttp.request("GET", "https://api.lolicon.app/setu/") as r:
        res = json.loads(await r.text(encoding="utf-8"))['data']
    for data in res:
        try:
            async with aiohttp.request("GET", data['url']) as r:
                filename = data['url'].split("/")[-1]
                if not os.path.exists(pic_dir + filename):
                    async with aiofiles.open(pic_dir + filename, 'wb') as f:
                        img = await r.read()
                        await f.write(img)
                        f.close()
                        if imghdr.what(pic_dir + filename) is None:
                            logger.info("download %s fail" % filename)
                            return
                        p = os.path.abspath(os.path.join(pic_dir, filename))
                        pic_pool.append("[CQ:image,file=file:///" + ("Z:/" if p.startswith('/') else "") + p + "]")
                        pic_local.append(filename)
                        logger.info("successfully download %s" % filename)
        except ssl.SSLError:
            pass
        logger.info("successfully fetch a pic into pool")
    return

@on_command('setu', only_to_me=False)
async def _(session: CommandSession):
    if session.ctx["message_type"] == 'group' and session.ctx['sender']['role'] in [ 'admin' ]:
        if session.current_arg == 'on':
            if session.ctx['group_id'] in session.bot.config.SETU_BAN:
                session.bot.config.SETU_BAN.remove(session.ctx['group_id'])
            await session.send("功能已开启!")
            return
        elif session.current_arg == 'off':
            if session.ctx['group_id'] not in session.bot.config.SETU_BAN:
                session.bot.config.SETU_BAN.add(session.ctx['group_id'])
            await session.send("功能已关闭!")
            return
    if session.ctx["message_type"] =='group' and session.ctx['group_id'] in session.bot.config.SETU_BAN:
        return
    if len(session.current_arg) > 0:
        return
    while len(pic_pool) == 0:
        await fetch_pic(True)
    await session.send(pic_pool.pop(random.randint(0, len(pic_pool) - 1)))
    return


@on_command('upload', only_to_me=False)
async def __(session: CommandSession):
    CQs = Parser(session.current_arg)
    cnt = 0
    for cqc in CQs:
        if cqc['CQ'] == "image":
            params = {'file':cqc['file']}
            filepath = await get_bot().call_action('get_image', **params)
            shutil.copy(filepath['file'], pic_dir + params['file'])
            p =  os.path.abspath(pic_dir + params['file'])
            pic_pool.append("[CQ:image,file=file:///" + ("Z:/" if p.startswith('/') else "") + p + "]")
            pic_local.append(params['file'])
            logger.info("successfully upload %s" % cqc['file'])
            cnt += 1
    if cnt > 0:
        await session.send('一共%d张, 社保了' % cnt)
    else:
        await session.send('色图呢,让我康康!')