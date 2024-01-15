1. 集群调用函数
``` erlang
执行命令
rp(tool:rpc({application, get_env, [message_store, is_use_channel_sync]}, 'msync@ebs')).
查日志
tool:log_search_rpc("2022-07-05 15:18:27", 7200, "1028405512963623676", 20, "ejabberd@ebs").

查聊天室
[MucPid] = easemob_muc_router:get_router(<<"easemob-demo#easeim_185068033212417">>).
rp(tool:get_state("<55333.5711.7675>")).
```

```
config:load_env("/data/apps/opt/msync/releases/23.3.1.0/sys.config").
easemob_traffic_control_sup:stop(),easemob_traffic_control_sup:start().
```

2. trace
```erlang
{ok, Dev} = file:open("/tmp/trace",[write]).
recon_trace:calls({queue, in, fun(_) -> return_trace() end}, 3, [{io_server, Dev}]).

recon_trace:calls({easemob_user_channel, read, fun(_) -> return_trace() end}, 100, [{return_to, true}, {scope, local}]).
```
3. kafka
``` shell
./kafka-consumer-groups.sh --bootstrap-server hsb-didi-guangzhou-mesos-master2:9092 --list

./kafka-consumer-groups.sh --bootstrap-server hsb-didi-guangzhou-mesos-master2:9092 --describe --group msync-channel-outgoing
```

```
rm /Users/one/easemob/msync/apps/msync/src/msync.appup.src
```

4. msync kafka

msync_log, easemob_log， easemob_log_worker: kafka的生产者

- 用户发送的消息，支持的消息类型有上行，下行，离线，ack
- 用户的状态
- 好友操作
- 用户禁言操作
- 敏感词
- ...

easemob_rest_event: 消费redis/kafka，发送多人聊天事件消息 (发现聊天室/群组kafka消费处于空转状态)
msync_easemob_sendmsg: 消费redis/kafka发消息

easemob_kafka: 读写kafka的核心模块

相关配置
- kafka_client_module brod | ekaf
- queue_log_module kafka | redis
- kafka_log_async true | false

## 测试
1. 登陆（长链接/websocket） 信波
3. 单聊，禁言，消息撤回，消息透传和扩展，reaction）蔡相跃
4. 群聊 （thread）嘉豪
5. 聊天室 一凡

问题：
1. 无法设置app_config
2. 无法访问存储
3. 定时跑，还是手动运行

## 群组压测

2000人群，2000下行，不在线，43%->62%
2000人群，4000下行，不在线，43%->99.7%
2000人群，2000下行，1000在线，77%->99.7%

大群
1000人，1000下行，1000在线， 80%->82%
1000人，2000下行，1000在线， 93.5%->99.7%
1000人，0下行，不在线     15%->15.6%
1000人，2000下行，500在线     68%->99.7%

配置：ticket_max(2000), timeout(30000)

|  压测场景   | 预期  | 启用限流(true/false) | 是否在线(true/false)
|  ----  | ----  | ---- |
| 2000人群，每秒2000下行，持续60s | 平稳运行，观察cpu，内存等指标，不会丢消息 | false |
| 2000人群，每秒2000下行，持续60s | 平稳运行，观察cpu，内存等指标，不会丢消息 | true |
| 2000人群，每秒4000下行，持续20s | cpu会很高，并且停止服务，会丢消息 | false |
| 2000人群，每秒4000下行，持续20s | 平稳运行，观察cpu，内存等指标，不会丢消息 | true |
| 2000人群，每秒10000下行，持续20s | cpu会很高，并且停止服务，会丢消息 | false |
| 2000人群，每秒10000下行，持续20s | 平稳运行，观察cpu，内存等指标，会丢消息 | true |
