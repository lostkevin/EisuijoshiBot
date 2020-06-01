from nonebot import CommandSession, on_command, MessageSegment
from utils.EisuiDB import EisuiDB
from  utils.Api import get_group_member_list
from wcwidth import wcswidth as ww
import datetime
db = EisuiDB('./data/eisui.db')
db.debugMode = False
groupID = 601691323

def rpad(s, n, c=' '):
    if type(s) != str:
        s = str(s)
    return s + (n-ww(s)) * c

def check(ctx):
    return ctx['message_type'] == 'group' and ctx['group_id'] == groupID

def getBonus():
    t = datetime.datetime.now()
    if t.hour in range(1, 6): #1点到5点
        return 0.5, '[凌晨经验减半]'
    elif t.hour in range(6, 9): #6点到8点
        return 2,  '[早起收益加倍]'
    return 1, ''

@on_command('浇水', only_to_me=False)
async def _watering(session: CommandSession):
    if check(session.ctx):
        print(session.ctx['anonymous'])
        groupLevel = session.ctx['sender']['level']
        expGot, _ = db.getRandomExp(groupLevel)
        bonus = getBonus()
        expGot *= bonus[0]
        r = db.doWater(session.ctx['user_id'], session.current_arg, expGot)
        reply = str(MessageSegment.at(session.ctx['sender']['user_id']))
        if r[0]:
            await session.send(r[5][0] + ':' + str(MessageSegment.at(session.ctx['user_id'])) + ', ' + r[1])
            reply += '本次浇水获得: %s%d点\n\n' % (bonus[1] , r[2])
            reply += '当前人物好感度: [%s] %d %s成长值: [%s] %d' % (r[3][1],r[3][0], r[5][1], r[4][1], r[4][0])
        else:
            reply += r[1]
        await session.send(reply) #返回错误原因
        return

@on_command('参拜', only_to_me=False)
async def _visit(session: CommandSession):
    if check(session.ctx):
        groupLevel = session.ctx['sender']['level']
        print('用户等级为: {}\n'.format(groupLevel))
        _, fameGot = db.getRandomExp(groupLevel)
        r = db.doVisit(session.ctx['user_id'], fameGot)
        reply = str(MessageSegment.at(session.ctx['sender']['user_id']))
        if r[0]:
            if r[1]:
                await session.send(r[1][0] + ':' + str(MessageSegment.at(session.ctx['user_id'])) + ', ' + r[1][1])
            reply += '本次获得声望:  %d, 当前声望值: [%s] %d, 距离下一等级: [%s] %d' % (r[2], r[6][0], r[3], r[6][1], r[4])
        else:
            reply += r[1]
        await session.send(reply)

@on_command('好感度', aliases=['契约'], only_to_me=False)
async def _query(session: CommandSession):
    r = db.queryLiking(session.ctx['user_id'], session.current_arg)
    reply = str(MessageSegment.at(session.ctx['sender']['user_id'])) if session.ctx['message_type'] == 'group' else ''
    if r[0]:
        reply += '上次浇水时间: %s, 获得: %d点' % (r[0][2], r[0][3])
    if len(session.current_arg) > 0:
        #获取群员列表
        l = await get_group_member_list(601691323)
        p_l = {i['user_id']:(i['card'] if len(i['card']) > 0 else i['nickname']) for i in l} # qq: 群备注 or qq: 昵称
        f_list = []
        rank = 1
        liking = r[1][0][2]
        c_tuple = None
        count = 1
        for i in r[1]:
            if i[0] not in p_l:
                continue
            if liking > i[2]:
                rank = count
                liking = i[2]
            f_list.append((rank, p_l[i[0]], *i)) #有记录
            if i[0] == session.ctx['user_id']:
                c_tuple = (rank, p_l[i[0]], *i)
            count += 1
        if len(f_list) > 10:
            f_list = f_list[0:9]
        if c_tuple:
            f_list.append(c_tuple)
        #生成回复
        tplt = '\n{} {} {} {}'
        reply += tplt.format(rpad('排行', 8), rpad('昵称', 20), rpad('等级', 12), rpad('好感度', 12))
        for i in f_list:
            reply += tplt.format(rpad(i[0], 8), rpad(i[1], 20), rpad(i[3], 12), rpad(i[4], 12))
    else:
        tplt = '\n{}{}{}'
        rs = [i for i in r[1] if i[2] > 0]
        reply += tplt.format(rpad('角色', 14), rpad('契约等级', 12), rpad('好感度', 12))
        for i in rs:
            reply += tplt.format(rpad(i[0], 14), rpad(i[1], 12), rpad(i[2], 12))
    await session.send(reply)

@on_command('成长值', only_to_me=False)
async def _growth(session: CommandSession):
    r = db.queryExp(session.ctx['user_id'], session.current_arg)
    reply = str(MessageSegment.at(session.ctx['sender']['user_id'])) if session.ctx['message_type'] == 'group' else ''
    if r[0]:
        reply += '上次浇水时间: %s, 获得成长值: %d点' % (r[0][2], r[0][3])
    tplt = "\n{}\t{}\t{}"
    if len(session.current_arg) > 0:
        l = await get_group_member_list(601691323)
        p_l = {i['user_id']: (i['card'] if len(i['card']) > 0 else i['nickname']) for i in l}  # qq: 群备注 or qq: 昵称
        f_list = []
        rank = 1
        liking = r[2][0][1]
        c_tuple = None
        count = 1
        for i in r[2]:
            if i[0] not in p_l:
                continue
            if liking > i[1]:
                rank = count
                liking = i[1]
            f_list.append((rank, p_l[i[0]], *i))  # 有记录
            if i[0] == session.ctx['user_id']:
                c_tuple = (rank, p_l[i[0]], *i)
            count += 1
        if len(f_list) > 10:
            f_list = f_list[0:9]
        if c_tuple:
            f_list.append(c_tuple)
        #生成回复
        reply += tplt.format(rpad("排名", 4), rpad("昵称",20), rpad("贡献度", 5))
        for i in f_list:
            reply += tplt.format(rpad(i[0], 4), rpad(i[1], 20), rpad(i[3], 5))
    else:
        reply += tplt.format(rpad("树名", 10), rpad("等级",12), rpad("成长值", 15))
        for i in r[1]:
            reply += tplt.format(rpad(i[0], 10), rpad(i[2], 12), rpad(str(i[1]) + '\\' + str(i[3]), 15))
    await session.send(reply)

@on_command('声望', only_to_me=False)
async def _fame(session: CommandSession):
    r = db.queryFame(session.ctx['user_id'])
    if r[0] == 0:
        return await session.send('当前声望值: 0, 等级:中立\n无参拜记录')
    reply = ''
    reply += '当前声望值: %d, 等级: %s\n' % (r[0], r[1][1])
    reply += '上次参拜: %s, 获得声望: %d' %(r[2], r[3])
    await session.send(reply)

@on_command('日常', only_to_me=False)
async def _(session: CommandSession):
    if not check(session.ctx):
        return
    reply = str(MessageSegment.at(session.ctx['sender']['user_id'])) if session.ctx['message_type'] == 'group' else ''
    reply += '欢迎使用永水日常系统 v0.0.1\n'
    reply += '支持以下命令(请加上前缀触发机器人):\n'
    tplt1 = '{}{}:{}\n'
    command_data = [('浇水', '[NPC/树名]', '对指定NPC浇水, 每日一次'),
                    ('参拜','', '神社参拜, 一定会有好事发生的吧, 每月一次'),
                    ('好感度/契约', '[NPC/树名](可选)', '查看当前NPC好感度以及排行榜' ),
                    ('成长值', '[NPC/树名](可选)', '查看神社中树的成长值以及贡献度排行榜')]
    for i in command_data:
        reply += tplt1.format(rpad(i[0], 20), rpad(i[1], 20), rpad(i[2], 60))
    reply += '下面是NPC数据:\n'
    tplt = '{}{}\n'
    reply += tplt.format(rpad('角色名', 12), rpad('神树', 16))
    d = [('神代小莳', '山高神代樱'), ('狩宿巴', '狩宿的下马樱'), ('泷见春', '三春泷樱'), ('薄墨初美','根尾谷淡墨樱'),
         ('石户霞', '石户蒲樱'), ('石户明星', '明星樱'), ('十曽湧', '奥十曾樱')]
    for i in d:
        reply += tplt.format(rpad(i[0], 12), rpad(i[1], 16))
    reply += '系统暂时处于试运行阶段~~~有bug请通知我'
    reply += str(MessageSegment.at(1870697069))
    return await session.send(reply)
