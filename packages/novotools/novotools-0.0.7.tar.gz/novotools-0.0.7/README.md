# 工作常用工具包

## 简介

该python包包括两部分的内容，一个部分是常用的一些函数的总结，包括文件操作，进程操作,log日志，发送和接收邮件，时间转换和运算等内容；
另一部分则是几个常用的小工具，有文本文件与excel相互转换的工具，有可以很好的展示较长文件Title，并按照Title名称来选取列
的工具。

## 项目仓库

https://gitee.com/biocoder/novotools/tree/master

## 下载方式

```shell

pip install novotools

```

## 函数功能简介

### 可用的函数

```python

>>> import novotools.utils as tools

>>> dir(tools)

['DocxApi', 'IMAPEmail', 'TimeParser', 'TitleParser', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'basic_log', 'datasize_convert', 'email_opt', 'logging_opt', 'make_colors', 'multi_logger', 'multi_process', 'process_and_thread', 'process_pool', 'progress_bar', 'run_cmd', 'send_email', 'string_format_and_file_opt', 'time_opt']

```

| 函数名称 | 功能 |
| ---- | ---- |
| DocxApi | 创建或修改一个word文档的类|
| IMAPEmail | 查收邮件或下载附件的类|
| send_email | 发送邮件并携带附件 |
| TimeParser | 时间格式转换 |
| TitleParser | 根据文件Title来获取对应列的内容 |
| run_cmd | 开启子进程运行命令 |
| make_colors | 输出有颜色的字符 |
| datasize_convert | B/KB/MB/GB/TB/PB之间的转换 |
| basic_log | 日志函数 |
| muti_logger | 日志函数 |
| thread_enhance | 为多线程提供异常处理和信号量的装饰器 |
| muti_process | 多进程函数 |
| process_pool | 进程池函数 |


详细的使用方法及示例请见 [test.md](https://gitee.com/biocoder/novotools/tree/master/test/test.md)

### 小工具

- [excel2text.py](https://gitee.com/biocoder/novotools/tree/master/novotools/tools/excel2text.py)
查看excel中的各个sheet并提取一个或多个sheet，仅支持2007及以上版本的excel
- [text2excel.py](https://gitee.com/biocoder/novotools/tree/master/novotools/tools/text2excel.py)
将一个或多个文本文件合并为一个excel文件，仅支持2007及以上版本的excel
- [getcol.py](https://gitee.com/biocoder/novotools/tree/master/novotools/tools/getcol.py)
展示一个文件的title，或按照title来提取其中的一列或几列，类似于Linux下的cut函数的功能
