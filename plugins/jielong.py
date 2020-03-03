from pypinyin import lazy_pinyin, Style
from utils.listm import yuntop,ptoyun,listma,idicon
from nonebot import CommandSession, on_command
from os import path, mkdir
from utils.JielongSearch import choiceEval
yuntoicron = {}
same = ['jh','ch','sh','r','z','c','s']
same3 = ['ㄓ', 'ㄔ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄘ', 'ㄙ']
xiuzhen = {
'iu':'ou' ,'uen':'un',
've':'yue','van':'yuan','vn':'yun'
}
same2 = {'zhi':'jh','chi':'ch','shi':'sh','ri':'r','zi':'z','ci':'c','si':'s'}

from PIL import Image
im = Image.open("./resource/icons.png")
for i in listma:
    y = i[3]
    p = yuntop[y]

    if p in same:
        p = 'same'

    if p not in yuntoicron:
        yuntoicron[p] = [[i[0], i[4]]]
    else:
        yuntoicron[p].append([i[0], i[4]])

def normalizePinyin(text):
    tailtext = text[-1]
    a = lazy_pinyin(tailtext, Style.FINALS)
    b = lazy_pinyin(tailtext)
    p = same2[b[-1]] if b[-1] in same2 else a[-1]
    if a[-1] in xiuzhen:
        p = xiuzhen[a[-1]]
    return p

def trans_text_tolist(text):
    tailtext = text[-1]
    a = lazy_pinyin(tailtext, Style.FINALS)
    b = lazy_pinyin(tailtext)
    # print(a[-1],b[-1])
    p = a[-1]
    if b[-1] in same2:
        p = 'same'
    elif a[-1] in xiuzhen:
        p = xiuzhen[a[-1]]
    return yuntoicron[p]

def get_single_icon(id_):
    index = idicon[id_]
    box = (index[0]+2,index[1]+2,index[0]+78,index[1]+78)
    region = im.crop(box)
    return region

def image_merge(images, score):
    width, height = 76,76
    nums = len(images)
    if nums > 5:
        new_width = 5 * width
        new_height = int(1 + nums/5) * height

    new_img = Image.new('RGB', (new_width, new_height), (255,255,255)) 
    res = sorted(score.items(), key=lambda x:x[1])
    x = y = 0
    if len(res) > 0:
        for tuple in res:
            img = eval(tuple[0])
            new_img.paste(img, (x, y))
            x += width
            if x >= width * 5:
                x = 0
                y += height
    else:
        for img in images:
            new_img.paste(img, (x, y))
            x += width
            if x >= width * 5:
                x = 0
                y += height
    return new_img
  
@on_command('接龙公屏')
async def _(session: CommandSession):
    if session.ctx['sender']['user_id'] in session.bot.config.SUPERUSERS:
        session.bot.config.jielongState = True if session.current_arg == '关闭' else False

@on_command('接龙', only_to_me=False)
async def _(session: CommandSession):
    if hasattr(session.bot.config, 'jielongState') and session.bot.config.jielongState:
        return
    session.current_arg = session.current_arg.split(' ')
    x = trans_text_tolist(session.current_arg[0])
    res = {}
    if len(session.current_arg) > 1:
        pin = [session.current_arg[0][-1], session.current_arg[1][0]]
        yun = [
            ptoyun[normalizePinyin(pin[i])] for i in range(0, len(pin))
        ]
        res = choiceEval(yun[0], yun[1])
    imgs = []
    levels = {}
    count = 0
    for i in x:
        imgs.append(get_single_icon(i[0]))
        if len(session.current_arg) > 1:
            levels['images[%d]' % count] = res['same' if i[1] in same3 else i[1]]
            count+=1
    result = image_merge(imgs, levels)
    if not path.isdir('./data/tmp'):
        mkdir('./data/tmp')
    result.save(path.join("./data/tmp", "jielong.png"))
    p = path.abspath(path.join("./data/tmp", "jielong.png"))
    await session.send("[CQ:image,file=file:///" + ("Z:/" if p.startswith('/') else "") + p + "]")
    return










