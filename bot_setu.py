import nonebot
import importlib
from removed.dhsMgrInit import init

if __name__ == '__main__':
    nonebot.init(importlib.import_module('config'))
    nonebot.get_bot().server_app.before_serving(init)
    nonebot.load_plugins('./plugins','plugins')
    nonebot.run(host='0.0.0.0', port=6666)
