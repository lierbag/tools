# tools
常用的工具脚本

## http server
使用ThreadingMixIn类和HTTPServer类实现了一个非常简单的多线程server
- server使用方法如demo.py中所示, 启动: ./demo.py 2>/dev/null &
- server预处理了get和post参数，具体业务逻辑可在__do_get()和__do_post()方法中实现
- __do_get(self, get)中get参数是dict类型，包含了所有的get参数
- __do_post(self,post)中post参数是字符串类型，包含post请求的包体数据
- 调用__send_response(self, data)返回数据给客户端，其中data是返回结果，字符串类型
- 日志处理也比较简单，直接输入在当前目录下run.log中
- 静态文件放在static目录下，请求静态文件时uri path必须以static开头. eq: hostname:port/static/xxx.html 则会将static/xxx.html返回

几个要注意的地方：
+ get参数处理不够健壮，如果get参数不符合规范，处理可能出错
+ 处理post请求时，请求头部中必须有Content-Length，否则将读不到post的包体数据
+ 使用捕获异常的方式，保证了处理get，post请求时不会出现服务器错误，返回码总是200
+ 注意启动时需要将标准错误定向到 /dev/null，因为默认的handler会输出一些信息到标准错误
