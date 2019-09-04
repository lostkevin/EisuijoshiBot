import nonebot
from EisuijoshiBot import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins('./plugins','plugins')
    nonebot.run(host='0.0.0.0', port=888)
