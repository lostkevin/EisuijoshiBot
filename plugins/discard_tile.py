from nonebot import on_command, CommandSession
import os
import subprocess
js = open('./plugins/discard.js', encoding='utf-8').read()

@on_command('pl', only_to_me=False)
async def pl(session: CommandSession):
    #result = js2py.eval_js( js + 'getResult(\"' +  session.current_arg + '\")')
    file = os.open('./tmp.js', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(file, (js + "\nconsole.log(getResult(\"" + session.current_arg + "\"))").encode('utf-8'))
    os.close(file)
    result = subprocess.Popen("node ./tmp.js", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    result, _ = result.communicate()
    result = result.decode('utf-8')
    await session.send(result.strip('\n'))

