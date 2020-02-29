from .priconne_data import _PriconneData

NAME2ID = {}

def gen_name2id():
    NAME2ID.clear()
    for k, v in _PriconneData.CHARA.items():
        for s in v:
            if s not in NAME2ID:
                NAME2ID[normname(s)] = k

def normname(name:str) -> str:
    name = name.lower().replace('（', '(').replace('）', ')')
    return name

class Chara:
    
    UNKNOWN = 1000
    
    def __init__(self, id_, star=3, equip=0):
        self.id = id_
        self.star = star
        self.equip = equip


    @staticmethod
    def fromid(id_, star=3, equip=0):
        '''Create Chara from her id. The same as Chara()'''
        return Chara(id_, star, equip)


    @staticmethod
    def fromname(name, star=3, equip=0):
        '''Create Chara from her name.'''
        id_ = Chara.name2id(name)
        return Chara(id_, star, equip)

    @property
    def name(self):
        return _PriconneData.CHARA[self.id][0] if self.id in _PriconneData.CHARA else _PriconneData.CHARA[Chara.UNKNOWN][0]

    @staticmethod
    def name2id(name):
        name = normname(name)
        if not NAME2ID:
            gen_name2id()
        return NAME2ID[name] if name in NAME2ID else Chara.UNKNOWN
