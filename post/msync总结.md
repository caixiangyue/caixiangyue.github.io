1. 集群调用函数
``` erlang
rp(tool:rpc({application, get_env, [message_store, is_use_channel_sync]}, 'msync@ebs')).
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