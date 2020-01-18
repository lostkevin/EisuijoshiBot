#coding=utf-8
from nonebot import on_command, CommandSession
from random import randint
from mahjong.tile import TilesConverter
from mahjong.shanten import Shanten
import copy

@on_command('pl', only_to_me=False)
async def pl(session: CommandSession):
    await session.send(session.current_arg + translateIntoMsg(getTile(session.current_arg)))

def getTile(s: str) -> dict:
    #translate s into supported format
    if len(s) == 0:
        return {}
    tiles = TilesConverter.one_line_string_to_136_array(s, True)
    test = {}
    # check tiles length
    added = []
    if len(tiles) % 3 == 0 :
        #3n, add a random tile
        while True:
            tmp = randint(0, 135)
            if tmp not in tiles:
                tiles.append(tmp)
                added.append(tmp)
                break
    if  len(tiles) % 3 == 1 :
        #3n+1, add a random tile
        while True:
            tmp = randint(0, 135)
            if tmp not in tiles:
                tiles.append(tmp)
                added.append(tmp)
                break
    if len(added) > 0:
        test[-1] = added
    # now is a normal form
    tiles.sort()
    avaliable = []
    for i in range(0, 136):
        if i not in tiles:
            avaliable.append(i)
    calculator = Shanten()
    baseShanten = calculator.calculate_shanten(TilesConverter.to_34_array(tiles))
    if baseShanten == -1:
        return {-2: '已和牌'}
    #14*122 try

    tmp = copy.deepcopy(tiles)

    for t in tiles:
        tmp.remove(t)
        one_try = []
        for i in avaliable:
            tmp.append(i)
            res = calculator.calculate_shanten(TilesConverter.to_34_array(sorted(tmp)))
            if res < baseShanten:
                one_try.append(i)
            tmp.remove(i)
        if len(one_try) > 0:
            test[t]=copy.deepcopy(one_try)
        tmp.append(t)

    return test

def __cmp(l1, l2):
    return 1
def translateIntoMsg(res : dict) -> str:
    Msg = {}
    finalStr = ''
    if -1 in res.keys():
        arr = res[-1]
        res.pop(-1)
        finalStr += ' 摸 '
        for i in arr:
            finalStr += '%s' % TilesConverter.to_one_line_string([i])
    if -2 in res.keys():
        finalStr += '\n %s' % res[-2]
        return finalStr
    for k in res:
        name = TilesConverter.to_one_line_string([k])
        tiles = TilesConverter.to_34_array(res[k])
        for i in range(0, len(tiles)):
            tiles[i] = 1 if tiles[i] > 0 else 0
        tiles = TilesConverter.to_136_array(tiles)
        chance = ''
        for i in tiles:
            chance += TilesConverter.to_one_line_string([i])
        Msg[len(res[k])] = '打%s 摸[' % name +  chance + ' %d枚]' % len(res[k])
    keys = sorted(Msg, reverse=True)

    for k in keys:
        finalStr += '\n' + Msg[k]
    return finalStr