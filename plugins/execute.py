import pymysql
from nonebot import on_command, CommandSession

@on_command('sql', only_to_me=False)
async def executeSQL(session: CommandSession):
    db = pymysql.connect("localhost", "bot")
    cursor = db.cursor()
    if hasattr(session.bot.config, 'PROGRAMMERS'):
        if session.ctx['sender']['user_id'] in session.bot.config.PROGRAMMERS:
            cursor.execute(session.current_arg)
            data = cursor.fetchone()
            await session.send(data[0])
    db.close()

