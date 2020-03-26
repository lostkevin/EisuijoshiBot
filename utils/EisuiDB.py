import sqlite3
import json
import datetime
import random
from functools import cmp_to_key
class EisuiDB:
    def __init__(self, dbPath: str):
        self.conn = sqlite3.connect(dbPath)
        with open('./data/Signin.json', encoding='utf-8') as f:
            self.d = json.load(f)
            f.close()
        self.debugMode = False #在debug模式下会禁用每日次数限制

    #attrName: TreeLevel, CharacterExp, FameLevel
    #左闭右开
    def _getLv(self, attrName, value):
        level = 0
        maxLevel = len(self.d[attrName])
        while level < maxLevel and value >= self.d[attrName][level]['TotalExp']:
            level += 1
        level -= 1
        return level, self.d[attrName][level]['LevelName']

    def getRandomExp(self, groupLv):
        return random.randint(self.d['Velocity'][groupLv][0], self.d['Velocity'][groupLv][1]), \
                random.randint(self.d['FameVelocity'][groupLv][0], self.d['FameVelocity'][groupLv][1])

    #对指定人物/树浇水
    def doWater(self, qq:int, name: str, exp: int):
        now = datetime.datetime.now()
        timeStr = now.strftime('%Y-%m-%d %H:%M:%S')
        today = timeStr.split(' ')[0]
        c = self.conn.cursor()
        c.execute('SELECT * FROM NPCdata WHERE NPCNAME == \'%s\' or TREENAME == \'%s\'' % (name, name))
        r = c.fetchall()
        if len(r) > 0:
            r = r[0]
        else:
            return False, '请确认名称是否正确' #名称输入错误
        id = r[0] #ID attr
        if not self.debugMode:
            # 检查浇水历史
            c.execute('SELECT TIME FROM WaterHistory WHERE QQ == \'%d\'' % qq)
            t = c.fetchall()
            for i in t:
                day = i[0].split(' ')[0]
                if day == today:
                    return False, '今天已经浇过水了'
        # 开始浇水
        # 生成回复
        birth = datetime.datetime.strptime(r[4], '%m-%d')
        npcName = (r[1], r[2])
        response = r[5]
        if birth.day == now.day and birth.month == now.month:
            response = r[6]
        # 更新成长值
        c.execute('UPDATE NPCdata SET TREELIKING = TREELIKING + \'%d\' WHERE ID == \'%d\'' % (exp, id))
        c.execute('select TREELIKING from NPCdata where ID == \'%d\'' % id)
        cTreeLiking = c.fetchall()[0][0]
        #插入浇水记录
        c.execute('INSERT INTO WaterHistory VALUES(\'%d\', \'%d\', \'%s\', \'%d\')' % (qq, id, timeStr, exp))
        #增加人物好感度
        c.execute('SELECT LIKING FROM Liking WHERE QQ == \'%d\' AND NPCID == \'%d\'' % (qq, id))
        r = c.fetchall()
        old = 0
        if len(r) > 0:
            old = r[0][0]
            new = old + exp
            c.execute('UPDATE Liking SET LIKING = LIKING + \'%d\' WHERE NPCID == \'%d\' and QQ == \'%d\''%(exp, id, qq) )
        else:
            c.execute('INSERT INTO Liking VALUES (\'%d\', \'%d\', \'%d\')' % (qq, id, exp))
            new = exp
        self.conn.commit()
        return True, response, exp, (new, self._getLv('CharacterExp', new)[1]),\
               (cTreeLiking, self._getLv('TreeLevel', cTreeLiking)[1]), npcName,
        #回复, 本次获取exp,人物好感度,树成长值, 名字

    def doVisit(self, qq:int, fame:int):
        now = datetime.datetime.now()
        c = self.conn.cursor()
        if not self.debugMode:
            c.execute('SELECT * FROM VisitHistory WHERE QQ == \'%d\';' % qq)
            r = c.fetchall()
            for i in r:
                t = datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')  # time
                if t.month == now.month and t.year == now.year:
                    return False, '您本月已经参拜过了'
        #没有参拜过,开始参拜
        #构造回复
        c.execute('SELECT NPCID, LIKING from Liking WHERE QQ == \'%d\'' % qq)
        r = c.fetchall()
        possible_reply = [ i for i in r if self._getLv('CharacterExp', i[1])[0] > 0]
        maxid = max(possible_reply, key= lambda x: x[1]) if len(possible_reply) > 0 else None
        response = None
        if maxid:
            c.execute('SELECT NPCNAME, VisitRes from NPCdata WHERE ID == \'%d\'' % maxid[0])
            response = c.fetchall()[0]
        #插入参拜数据
        c.execute('INSERT INTO VisitHistory VALUES (\'%d\', \'%s\', \'%d\')' %(qq, now.strftime('%Y-%m-%d %H:%M:%S'), fame))
        #更新声望
        newFame = self._updateFame(qq, fame)
        self.conn.commit()
        #根据声望构造系统消息
        f = self._getLv('FameLevel', newFame)
        d = -1
        total = -1
        level = [f[1], '']
        if f[0] != len(self.d['FameLevel']) - 1:
            total = self.d['FameLevel'][f[0] + 1]['TotalExp']
            level[1] = self.d['FameLevel'][f[0] + 1]['LevelName']
            d = total - newFame
        return True, response, fame, newFame, d, total, level

    def _updateFame(self, qq, delta):
        c = self.conn.cursor()
        old = self._getFame(qq)
        new = old + delta
        c.execute('INSERT OR REPLACE INTO Member VALUES (\'%d\', \'%d\')' % (qq, new))
        return new

    def _getFame(self, qq):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Member WHERE QQ == \'%d\'' % qq)
        r = c.fetchall()
        if len(r) > 0:
            return r[0][1]
        return 0

    def _getNPCID(self, name:str):
        c = self.conn.cursor()
        c.execute('select ID from NPCdata where NPCNAME == \'%s\' or TREENAME == \'%s\'' % (name, name))
        r = c.fetchall()
        if len(r):
            return r[0][0]
        return None

    def queryExp(self, qq, name = None):
        c = self.conn.cursor()
        history = self._getHistory('water', qq, name)
        if name:
            # 查找对应人物的浇水历史
            id = self._getNPCID(name)
            if not id:
                return False, '该名字不存在'
            c.execute('select TREENAME, TREELIKING from NPCdata where ID == \'%d\'' % id)
            #求某棵树的成长值
            treeExp = c.fetchall()[0]
            #求每个人的贡献度并排序
            c.execute('select QQ, SUM(EXP) from WaterHistory where NPCID == \'%d\' group by QQ' % id)
            r = c.fetchall()
            def _cmp(k1, k2):
                if k1[1] != k2[1]:
                    return 2 * int(k1[1] > k2[1]) - 1
                t1 = self._getHistory('visit', k1[0])
                t2 = self._getHistory('visit', k2[0])
                if not t1 or not t2:
                    return -1
                r1 = datetime.datetime.strptime(t1[-2], '%Y-%m-%d %H:%M:%S')
                r2 = datetime.datetime.strptime(t2[-2], '%Y-%m-%d %H:%M:%S')
                return 2 * int(r1 < r2) - 1 #浇水较早的先到达
            r.sort(key=cmp_to_key(_cmp), reverse=True)
            # rankList = []
            # rank = 1
            # lastExp = r[0][1]
            # for i in range(len(r)):
            #     if lastExp > r[i][1]:
            #         rank += 1
            #     rankList.append((rank, r[i]))
            return history, (*treeExp, self._getLv('TreeLevel', treeExp[1])[1]), r
        c.execute('select ID, TREENAME, TREELIKING from NPCdata ORDER BY TREELIKING DESC')
        rankList = []
        r = c.fetchall()
        for i in range(len(r)):
            lv = self._getLv('TreeLevel', r[i][2])
            nextLevelExp = self.d['TreeLevel'][lv[0] + 1]['TotalExp']
            rankList.append((r[i][1], r[i][2], lv[1], nextLevelExp))
        return history, rankList

    def queryFame(self, qq):
        #声望及声望等级
        c = self.conn.cursor()
        fame = self._getFame(qq)
        fameLevel = self._getLv('FameLevel', fame)
        r = self._getHistory('visit', qq)
        if r:
            _, time, v_fame = r
            return fame, fameLevel, time, v_fame
        return 0, 0, None, None

    #获取最近一次访问记录
    #visit, water
    def _getHistory(self, history_type: str, qq: int, name: str =None):
        converter = {'visit':'VisitHistory', 'water': 'WaterHistory'}
        history_type = history_type.lower()
        if history_type not in converter:
            return None
        c = self.conn.cursor()
        additional = ''
        if history_type == 'water' and name:
            c.execute('SELECT ID FROM NPCdata WHERE NPCNAME == \'%s\' or TREENAME == \'%s\'' % (name, name))
            r = c.fetchall()
            if len(r) > 0:
                additional = 'and NPCID == \'%d\'' % r[0][0]
        c.execute(('SELECT * FROM %s WHERE QQ == \'%d\'' % (converter[history_type], qq)) + additional)
        r = c.fetchall()
        min_time = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
        res = None
        for i in r:
            #time
            t = datetime.datetime.strptime(i[-2], '%Y-%m-%d %H:%M:%S')
            if min_time < t:
                res = i
                min_time = t
        return res

    def _getAllNPC(self):
        c = self.conn.cursor()
        c.execute('select NPCNAME from NPCdata')
        r = c.fetchall()
        return [i[0] for i in r]

    def queryLiking(self, qq: int, name: str = None):
        c = self.conn.cursor()
        if name:
            # 查找对应人物的浇水历史
            history = self._getHistory('water', qq, name)
            id = self._getNPCID(name)
            if not id:
                return False, '该名字不存在'
            # 查找所有成员对该人物的好感度
            c.execute('select QQ, LIKING from Liking where NPCID == \'%d\'' % id)
            l = c.fetchall()
            def _cmp(k1, k2):
                if k1[1] != k2[1]:
                    return 2 * int(k1[1] > k2[1]) - 1
                t1 = self._getHistory('water', k1[0])
                t2 = self._getHistory('water', k2[0])
                if not t1 or not t2:
                    return -1
                r1 = datetime.datetime.strptime(t1[-2], '%Y-%m-%d %H:%M:%S')
                r2 = datetime.datetime.strptime(t2[-2], '%Y-%m-%d %H:%M:%S')
                return 2 * int(r1 < r2) - 1#浇水较早的先到达
            l.sort(key=cmp_to_key(_cmp), reverse=True)
            res = []
            for i in range(len(l)):
                lv = self._getLv('CharacterExp', l[i][1])
                nextLv = self.d['CharacterExp'][lv[0]]['TotalExp']
                res.append((l[i][0], lv[1], l[i][1], nextLv)) #qq, lv, currentExp, nextLevelExp
            return history, res
        # 缺省值, 获取最近一次浇水的记录
        history = self._getHistory('water', qq)
        # 查询与所有人物的好感度
        c.execute(
            'select NPCNAME, LIKING from Liking left join NPCdata NC on Liking.NPCID = NC.ID where QQ == \'%d\'' % qq)
        r = {i[0]: i[1] for i in c.fetchall()}
        npcs = self._getAllNPC()
        rankList = []
        for npc in npcs:
            if npc in r:
                lv = self._getLv('CharacterExp', r[npc])
                rankList.append((npc, lv[1], r[npc], self.d['CharacterExp'][lv[0]]['TotalExp']))
            else:
                lv = self._getLv('CharacterExp', 0)
                rankList.append((npc, lv[1], 0, 0))
        rankList.sort(key=lambda x: x[2], reverse=True)
        return history, rankList