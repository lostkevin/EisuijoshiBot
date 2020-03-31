import nonebot
import importlib

if __name__ == '__main__':
    nonebot.init(importlib.import_module('config'))
    nonebot.load_plugins('./plugins','plugins')
    nonebot.run(host='0.0.0.0', port=1234)


