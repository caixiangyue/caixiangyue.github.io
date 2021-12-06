#### linux 内核参数
+ tcp_max_syn_backlog: 用于设置半连接队列(syn queue，内核中实现为一个哈希表)大小
+ somaxconn: 用于设置全连接队列(accept queue)大小
+ syncookies: 开启此参数可以再不使用半连接队列的情况下成功建立连接

#### 用户参数
+ backlog: 用于设置全连接队列大小

tcp_max_syn_backlog， somaxconn， backlog这三个参数的最小值就是半连接队列的最大长度

somaxconn和backlog的最小值就是全连接队列的最大长度

#### 临时修改内核参数命令
``` bash
sudo sysctl -w net.core.somaxconn=4096
```
