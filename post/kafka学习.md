#### 环境搭建
启动`zookeeper`
```
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```
启动`kafka`
```
$ bin/kafka-server-start.sh config/server.properties
```
创建topic
```
$ bin/kafka-topics.sh --create --topic t1 --bootstrap-server localhost:12346 --partitions 1 --replication-factor 1

Created topic t1
```
生产消息
```
$ bin/kafka-console-producer.sh --topic t1 --bootstrap-server localhost:12346
```
消费消息
```
$ bin/kafka-console-consumer.sh --topic t1 --from-beginning --bootstrap-server localhost:12346
```
