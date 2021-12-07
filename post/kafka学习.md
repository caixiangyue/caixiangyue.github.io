#### 环境搭建
docker-compose.yml
``` yaml
version: "2"

services:
  zookeeper:
    image: docker.io/bitnami/zookeeper:3.7
    ports:
      - "2181:2181"
    volumes:
      - "zookeeper_data:/bitnami"
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes
  kafka:
    image: docker.io/bitnami/kafka:3
    ports:
      - "9092:9092"
    volumes:
      - "kafka_data:/bitnami"
    environment:
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://127.0.0.1:9092
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CREATE_TOPICS=mytopic
    depends_on:
      - zookeeper

volumes:
  zookeeper_data:
    driver: local
  kafka_data:
    driver: local
```

启动
``` shell
$ docker-compose up -d
```

消费者
``` python
from kafka import KafkaConsumer

consumer = KafkaConsumer('mytopic', bootstrap_servers= ['127.0.0.1:9092'])
for msg in consumer:
    print(msg)
```

生产者
``` python
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])
future = producer.send('mytopic' , key= b'test', value= b'test', partition=0)
result = future.get(timeout= 10)
print(result)
```