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

### channel 相关命令

get all user channel: **zrevrangebyscore**
get all channel cursors: **hgetall**
get channel index: **lrange**

write user channel: **zadd, zcard, zremrangebyrank, expire**
write channel index: **lpush, llen, ltrim, expire**
write channel cursor: **hset, hlen, hdel, expire**

