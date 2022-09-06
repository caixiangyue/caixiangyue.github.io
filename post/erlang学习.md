#### hello world.
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

#### 元组
``` erlang
1> Point = {4, 5}.
{4,5}
2> {X, Y} = Point.
{4,5}
3> X.
4
4> Y.
5
5> {point, Point}.
{point,{4,5}}
```


#### 列表
基本操作
``` erlang
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

#### 位语法
``` erlang
11> Color = 16#FF00AA.
16711850
12> Pixel = <<Color:24>>.
<<255,0,170>>
13> <<R:8, Rest/binary>> = Pixel.
<<255,0,170>>
14> R.
255
```

#### 函数
创建`same.erl`
``` erlang
-module(same).
-compile(export_all).

same(X, X)->
    true;
same(_,_)->
    false.
```
运行
``` erlang
1> c(same).
same.erl:2:2: Warning: export_all flag enabled - all functions will be exported
%    2| -compile(export_all).
%     |  ^

{ok,same}
2> same:same(1,1).
true
3> same:same(1,2).
false
```