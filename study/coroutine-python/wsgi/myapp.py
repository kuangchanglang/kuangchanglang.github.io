# coding=utf-8

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world']

# environ:          一个包含请求信息及环境信息的字典，server 端会详细说明
# start_response:   一个接受两个参数`status, response_headers`的方法:
# status:           返回状态码，如http 200、404等
# response_headers: 返回信息头部列表
