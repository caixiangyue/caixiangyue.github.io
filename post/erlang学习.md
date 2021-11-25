## hello world.
创建一个源文件`hello.erl`
``` erlang
-module(hello).
-export([hello/0]).

hello()->
    io:format("hello world.~n").
```

编译运行
``` erlang
$ erl
Erlang/OTP 24 [erts-12.1.5] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Eshell V12.1.5  (abort with ^G)
1> c(hello).
{ok,hello}
2> hello:hello().
hello world.
ok
```

## 列表
``` erlang
基本操作
> L = [1, 2, 3].
[1,2,3]
2> [H|T] = L.
[1,2,3]
3> H.
1
4> T.
[2,3]
5> N = [1]++T.
[1,2,3]
6> N--[1].
[2,3]
```
列表推导
``` erlang
10> N.
[1,2,3]
11> [ 2*X || X <- N ]. 
[2,4,6]

15> W = [1, a, b, 2, 3].          
[1,a,b,2,3]
16> [ 2*X || X <- W, integer(X) ].
[2,4,6]
```