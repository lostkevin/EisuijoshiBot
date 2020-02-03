# EisuijoshiBot

永水高校使用的QQ管理机器人,用于简化报名\注册等一系列日常工作
## Environment
+ Docker
+ Wine CoolQ
    + wine coolQPro安装见[发布页面](https://github.com/CoolQ/docker-wine-coolq)
+ CQHttpApi
    + 下载[Release](https://github.com/richardchien/coolq-http-api/releases)并复制到数据目录内的app文件夹下
    + 安装[语音插件](https://dlcq.cqp.me/cq/cqc_1.0.1.zip)
    + 首次登录后编辑data\app\io.github.richardchien.coolqhttpapi(或app\io.github.richardchien.coolqhttpapi)下的配置文件,格式见开发文档,一个示例配置见下
+ mySQL + python connector
    + pip install pymysql

## CQHttpApi
主动调用Api使用以下指令:
    
    await get_bot().call_action(action, **params)

如:

    params = {'group_id': session.ctx['group_id']}
    await get_bot().call_action('set_group_leave', **params)
具体使用方式以及参数说明见[CQHttpApi](https://cqhttp.cc/docs/)文档

## Config配置
Windwos端的json

    {
        "host": "[::]",
        "port": 5700,
        "use_http": true,
        "ws_host": "[::]",
        "ws_port": 6700,
        "use_ws": false,
        "ws_reverse_url": "",
        "ws_reverse_api_url": "ws://127.0.0.1:888/ws/api/",
        "ws_reverse_event_url": "ws://127.0.0.1:888/ws/event/",
        "ws_reverse_reconnect_interval": 50,
        "ws_reverse_reconnect_on_code_1000": true,
        "use_ws_reverse": true,
        "post_url": "",
        "access_token": "",
        "secret": "",
        "post_message_format": "string",
        "serve_data_files": false,
        "update_source": "github",
        "update_channel": "stable",
        "auto_check_update": false,
        "auto_perform_update": false,
        "show_log_console": true,
        "log_level": "info"
    }
    
docker将保存为ini

    [机器人QQ号]
        serve_data_files = yes
        ws_reverse_api_url = ws://172.17.0.1:888/ws/api/
        ws_reverse_event_url = ws://172.17.0.1:888/ws/event/
        use_ws_reverse = yes
        ws_reverse_reconnect_interval = 50

