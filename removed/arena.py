import time
import requests
import json
from nonebot import CommandSession, MessageSegment, on_command
from os import path
from utils.chara import Chara
import re


class Arena(object):
    @staticmethod
    def __get_auth_key():
        return '1'
        config_file = path.join(path.dirname(__file__), "config.json")
        with open(config_file, encoding='utf8') as f:
            config = json.load(f)
            return config["AUTH_KEY"]

    @staticmethod
    def do_query(id_list):
        id_list = [x * 100 + 1 for x in id_list]
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            'authorization': None
        }
        payload = {"_sign": "a", "def": id_list, "nonce": "a", "page": 1, "sort": 1, "ts": int(time.time()),
                   "region": 1}
        resp = requests.post('https://api.pcrdfans.com/x/v1/search', headers=header, data=json.dumps(payload))
        res = resp.json()
        if res['code']:
            return None

        res = res['data']['result']
        res = [
            {
                'atk': [Chara(c['id'] // 100, c['star'], c['equip']) for c in entry['atk']],
                'up': entry['up'],
                'down': entry['down'],
            } for entry in res
        ]
        return res

@on_command('竞技场查询', aliases=('jjc查询', '怎么拆', '怎么解', '怎么打', '如何拆', '如何解', '如何打', '怎麼拆', '怎麼解', '怎麼打'), only_to_me=False)
async def arena_query(session:CommandSession):

    # 处理输入数据
    argv = session.current_arg.strip()
    argv = re.sub(r'[?？呀啊哇]', ' ', argv)
    argv = argv.split()

    if 0 >= len(argv):
        await session.finish('请输入防守方角色，用空格隔开')
    if 5 < len(argv):
        await session.finish('编队不能多于5名角色')

    # 执行查询
    defen = [ Chara.name2id(name) for name in argv ]
    for i, id_ in enumerate(defen):
        if Chara.UNKNOWN == id_:
            await session.finish(f'编队中含未知角色{argv[i]}，请尝试使用官方译名\n您可@bot来杯咖啡+反馈未收录别称\n或前往 github.com/Ice-Cirno/HoshinoBot/issues/5 回帖补充')
    if len(defen) != len(set(defen)):
        await session.finish('编队中出现重复角色')

    res = Arena.do_query(defen)

    # 处理查询结果
    if res is None:
        await session.finish('查询出错，请联系维护组调教')

    if not len(res):
        await session.finish('抱歉没有查询到解法\n※没有作业说明随便拆')


    res = res[:min(6, len(res))]    # 限制显示数量，截断结果

    atk_team_txt = '\n'.join(map(lambda entry: ' '.join(map(lambda x: f"{x.name}{x.star if x.star else ''}{'专' if x.equip else ''}" , entry['atk'])) , res))

    updown = [ f"赞{entry['up']} 踩{entry['down']}" for entry in res ]
    updown = '\n'.join(updown)

    # 发送回复
    defen = [ Chara.fromid(x).name for x in defen ]
    defen = ' '.join(defen)

    header = f'已为骑士君{MessageSegment.at(session.ctx["user_id"])}查询到以下进攻方案：'
    defen = f'【{defen}】'
    updown = f'👍&👎：\n{updown}'
    footer = '禁言是为避免频繁查询，请打完本场竞技场后再来查询'
    ref = 'Support by pcrdfans'
    msg = f'{defen}\n{header}\n{atk_team_txt}\n{updown}\n{footer}\n{ref}'

    await session.send(msg)
