# 公主连接Re:Dive会战管理插件
# clan == クラン == 戰隊（直译为氏族）（CLANNAD的CLAN（笑））

import re
from typing import Callable, Dict, Tuple, Iterable

import unicodedata
import zhconv
import importlib
import sys
from nonebot import NoneBot, get_bot
from utils.service import Service, Privilege
from .argparse import ArgParser, ParseResult
from .exception import *

sv = Service('clanbattle', manage_priv=Privilege.SUPERUSER, enable_on_default=True)
SORRY = 'ごめんなさい！嘤嘤嘤(〒︿〒)'

_registry:Dict[str, Tuple[Callable, ArgParser]] = {}

def normalize_str(string) -> str:
    """
    规范化unicode字符串 并 转为小写 并 转为简体
    """
    string = unicodedata.normalize('NFKC', string)
    string = string.lower()
    string = zhconv.convert(string, 'zh-hans')
    return string

@sv.on_rex(re.compile(r'^[?？!！](.+)', re.DOTALL), event='group')
async def _clanbattle_bus(bot:NoneBot, ctx, match):
    cmd, *args = match.group(1).split()
    cmd = normalize_str(cmd)
    if cmd in _registry:
        func, parser = _registry[cmd]
        try:
            args = parser.parse(args, ctx['message'])
            await func(bot, ctx, args)
        except DatabaseError as e:
            await bot.send(ctx, f"DatabaseError: {e.message}\n{SORRY}\n※请及时联系维护组")
        except ClanBattleError as e:
            await bot.send(ctx, e.message, at_sender=True)
        except Exception as e:
            sv.logger.exception(e)
            sv.logger.error(f'{type(e)} occured when {func.__name__} handling message {ctx["message_id"]}.')
            await bot.send(ctx, f'Error: 机器人出现未预料的错误\n{SORRY}\n※请及时联系维护组', at_sender=True)


def cb_cmd(name, parser:ArgParser) -> Callable:
    if isinstance(name, str):
        name = (name, )
    if not isinstance(name, Iterable):
        raise ValueError('`name` of cb_cmd must be `str` or `Iterable[str]`')
    names = map(lambda x: normalize_str(x), name)
    def deco(func) -> Callable:
        for n in names:
            if n in _registry:
                sv.logger.warning(f'出现重名命令：{func.__name__} 与 {_registry[n].__name__}命令名冲突')
            else:
                _registry[n] = (func, parser)
        return func
    return deco

def cb_clean():
    #_registry.clear()
    print(get_bot()._bus._subscribers)
    get_bot().unsubscribe('message.group', _clanbattle_bus)

try:
    importlib.reload(sys.modules['plugins.clanbattle.cmdv2'])
except KeyError:
    importlib.import_module('plugins.clanbattle.cmdv2')

@cb_cmd('帮助', ArgParser('!帮助'))
async def cb_help(bot:NoneBot, ctx, args:ParseResult):
    msg = f'''
# PCR会战管理v2.0
> 🐒也会用的会战管理
2. 使用命令 "!入会 N昵称" 进行注册
?入会 N祐树

3. 使用命令 "!出刀 伤害值" 上报伤害
?出刀 514w
?收尾
?出补时刀 114w

4. 忙于工作/学习/娱乐时，使用命令 "!预约 Boss号" 预约出刀
?预约 5

5. 夜深人静时，使用命令 "!催刀" 在群内at未出刀的成员，督促出刀
?催刀

※详细说明见群公告
※使用前请【逐字】阅读必读事项'''
    await bot.send(ctx, msg, at_sender=True)
