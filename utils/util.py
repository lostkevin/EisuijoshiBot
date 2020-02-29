import os
import base64
import zhconv
import unicodedata
import json
from io import BytesIO

from nonebot import get_bot, logger
from aiocqhttp.exceptions import ActionFailed


def load_config(inbuilt_file_var):
    """
    Just use `config = load_config(__file__)`,
    you can get the config.json as a dict.
    """
    filename = os.path.join(os.path.dirname(inbuilt_file_var), 'config.json')
    with open(filename, encoding='utf8') as f:
        config = json.load(f)
        return config
    

async def delete_msg(ctx):
    try:
        if get_bot().config.IS_CQPRO:
            msg_id = ctx['message_id']
            await get_bot().delete_msg(self_id=ctx['self_id'], message_id=msg_id)
    except ActionFailed as e:
        logger.error(f'撤回失败 retcode={e.retcode}')
    except Exception as e:
        logger.exception(e)


async def silence(ctx, ban_time, ignore_super_user=False):
    try:
        self_id = ctx['self_id']
        group_id = ctx['group_id']
        user_id = ctx['user_id']
        bot = get_bot()
        if ignore_super_user or user_id not in bot.config.SUPERUSERS:
            await bot.set_group_ban(self_id=self_id, group_id=group_id, user_id=user_id, duration=ban_time)
    except ActionFailed as e:
        logger.error(f'禁言失败 retcode={e.retcode}')
    except Exception as e:
        logger.exception(e)

def normalize_str(string) -> str:
    """
    规范化unicode字符串 并 转为小写 并 转为简体
    """
    string = unicodedata.normalize('NFKC', string)
    string = string.lower()
    string = zhconv.convert(string, 'zh-hans')
    return string
