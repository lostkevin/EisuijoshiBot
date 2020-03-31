from removed.listm import *
import numpy as np

same = ['ㄓ', 'ㄔ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄘ', 'ㄙ']
vName = {}
def IDtoYun(id: int)->str:
    return [i for i in vName.keys()][id] if len(vName.keys()) > 0 else ''
def yunToID(yun: str)-> int:
    return vName['same' if yun in same else yun] if len(vName) > 0 else -1
def generateGraph():
    count = 0
    for vn in  [item[3] for item in listma]:
        if vn in vName:
            continue
        if not vn in same:
            vName[vn] = count
        else:
            if not 'same' in vName.keys():
                vName['same'] = count
            else:
                count -= 1
        count = count + 1
    mat = np.zeros((len(vName), len(vName)))
    flag = np.zeros((len(vName), len(vName)))
    for item in listma:
        mat[yunToID(item[3])][yunToID(item[4])] += 1
        flag[yunToID(item[3])][yunToID(item[4])] = 1
    for row in range(0, len(vName)):
        mat[row] /= sum(mat[row])
    return [len(vName), len(vName)], mat, flag

#Input: 起始韵母, 目标韵母
def choiceEval(src: str, dst: str) -> dict:
    res = {}
    shape, K, flag = generateGraph()
    src = yunToID(src)
    dst = yunToID(dst)
    #假设vb储存着本轮移动到某点的价值, 初值为随机移动至目标韵母的概率
    vb = np.transpose(K[:, dst])
    vw = np.zeros(shape[0])
    #迭代数次获取较稳定的值,次数过大后会收敛至1
    for loop in range(0, 5):
        #选择最大概率的移动
        for i in range(0, shape[0]):
            vw[i] = max(flag[i] * vb) if i != dst else 1
        #NPC随机选择一个点移动
        for i in range(0, shape[0]):
            vb[i] = sum(flag[i] * vw) / sum(flag[i])
    #输出结果
    return {IDtoYun(i):(vb * flag[src])[i] for i in range(0, shape[0])}