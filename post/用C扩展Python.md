> 用C语言写一个最简单的python扩展。

## 一. 上代码
1. hello.c

``` c
#include<Python.h>

static PyObject *say_hello(PyObject *self, PyObject *args) {
    return Py_BuildValue("s", "hello from c.");
}

static PyMethodDef methods[] = {
    {"say_hello", say_hello, METH_VARARGS, "say hello."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_def =
{
    PyModuleDef_HEAD_INIT,
    "hello",
    "say hello",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_hello(void) {
    return PyModule_Create(&module_def);
}
``` 

2. setup.py

``` python
from distutils.core import setup, Extension

module = Extension('hello', sources = ['hello.c'])

setup(name = 'say hello', version = '0.0.1', ext_modules = [module])
```

## 二. 编译
``` shell
$ python setup.py build
```
## 三. 调用
**注** 此时想要调用需要把`hello.so`共享库加到PYTHONPATH环境变量中。

``` python
#!/usr/bin/env python3
import hello
print(hello.say_hello()) 
```
## 四. 参考
+ https://docs.python.org/3/extending/extending.html