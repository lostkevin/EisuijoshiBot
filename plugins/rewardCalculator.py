from nonebot import on_command, CommandSession

@on_command('补偿计算', only_to_me=False)
async def _(session: CommandSession):
    def f(x):
        try:
            x = x[:-1] + '0000' if x[-1] in ['w', 'W', '万'] else x
            x = x[:-1] + '000' if x[-1] in ['k', 'K', '千'] else x
            return int(x)
        except ValueError as e:
            return False
    args = session.current_arg.split(' ')
    reward = 20
    if 'cn' in args:
        reward = 10
    print(args)
    args = list(map(f, filter(f, args)))
    if len(args) > 3 or len(args) < 2:
        return await session.send('输入错误!用法: 补偿计算 jp/cn/tw 剩余血量 伤害 剩余时间(不输入时为0, 单位秒)')
    # 剩余血量 超杀伤害 剩余时间
    total_time = 90 - (args[2] if len(args) == 3 else 0)
    remain_life = args[0]
    damage = args[1]
    EPS = 1e-10
    res = min(90, int(90 + reward - total_time * remain_life / damage - EPS) + 1)
    return await session.send('预计补偿时间: {}秒'.format(res))
