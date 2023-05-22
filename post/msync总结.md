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

### channel 相关命令

get all user channel: **zrevrangebyscore**
get all channel cursors: **hgetall**
get channel index: **lrange**

write user channel: **zadd, zcard, zremrangebyrank, expire**
write channel index: **lpush, llen, ltrim, expire**
write channel cursor: **hset, hlen, hdel, expire**

delete user channel: **zrem**

## 会话列表
### 数据结构
![](../img/20221013/1.jpg)

1. zset 存储某个用户所有的会话

    key: im:user:channel:userid

    score: 最后一条消息的id

    member: channelid (userid/groupid)
2. hash 存储某个用户所有会话的cursor

    key: im:channel:cursor:userid

    field: channelid

    value: 已读消息id
3. list 存储某个会话所有的消息id

    key: im:channel:index:from:to / im:channel:index:to@conference.easemob.com

    element: 消息id

### 操作会话列表的时机
1. 发消息 (单聊, 群聊, rest api) (写channel, index, cursor)
2. channel_ack  (单聊, 群聊) (写cursor)
3. 收消息 (单聊, 群聊) (写channel) 注: 这里没有区分消息类型
4. 撤回消息 (单聊, 群聊, rest api) (删 index)
5. POST /user_channel_delete 接口 (删channel, 写cursor)
6. POST /conversation_delete 接口 (删channel, index, cursor) 注: 仅支持单聊
7. DELETE /users 接口 (删 channel, cursor)
8. GET /user_channel 接口 (读 channel, index, cursor)

### app级别配置
- is_use_channel_sync (默认 false)
- user_channel_limit  (默认 10)
- channel_index_limit (默认 100)
- channel_cursor_limit (默认 10)
- easemob_channel_ttl (默认 604800, 7天)
- is_rest_msg_write_to_channel (默认 false)
- is_use_channel_double_read (默认 false)

发消息(rest，单聊，群聊), channel_ack, 删会话，撤回消息