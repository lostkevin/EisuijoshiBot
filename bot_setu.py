import nonebot
import importlib
import sys

sys.path += ['..\\']
nonebot.init(importlib.import_module('config'))
nonebot.load_plugins('./plugins','plugins')
nonebot.run(host='0.0.0.0', port=6666)
