#!/usr/bin/python3

import socket
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))
Error404 = "404".encode()

def createHeader(**kwargs):
    default = {"Host": "localhost", "Status": "200 OK"}
    default.update(kwargs)
    return ("HTTP/1.1 " + default['Status'] +" \n" + "\n".join([key + ": " + value for key, value in default.items()])).encode()

def printResult(f):
    def func(*args, **kwargs):
        res = f(*args, **kwargs)
        print(res)
        return res
    return func

@printResult
def get_response(request):
    def refine(line):
        if ': ' in line:
            index = line.index(': ')
            return (line[:index], line[index + 2:])
        else:
            return ("", "")
        
    lines = request.decode().split('\r')
    props = dict([refine(line.strip()) for line in lines])
    method, path, _ = lines[0].split(' ')
    
    if method != 'GET':
        text = "Method not allowed"
        return createHeader(**{"Status": "405 Method not allowed", "Content-length": str(len(text))}) + ("\n\n" + text).encode()
    
    print("path =", path)
    if path == "/":
        return ("Hello mister!\nYou are: " + props['User-Agent']).encode()
    elif path == "/media":
        return '\n'.join(os.listdir('../files')).encode()
    elif path == "/test":
        return request
    elif path.startswith('/media/'):
        try:
            with open('../files/' + path[path.rindex('/'):]) as I:
                text = I.read().encode()
                header = createHeader(**{"Content-length": str(len(text))})
                return header + "\n\n".encode() + text
        except FileNotFoundError:
            text = "File not found"
            return createHeader(**{"Status": "404 Not Found", "Content-length": str(len(text))}) + ("\n\n" + text).encode()
    else:
        text = "Page not found"
        return createHeader(**{"Status": "404 Not Found", "Content-length": str(len(text))}) + ("\n\n" + text).encode()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# связываем server_socket c 8000 портом
server_socket.bind(('localhost', 8000))  
server_socket.listen(0)  # слушаем, что нам отправит клиент

print('Started')

while True:
    try:
        (client_socket, address) = server_socket.accept()
        # печатаем клиентский сокет
        print('Got new client', client_socket.getsockname())
        request_string = client_socket.recv(2048)  # принимаем 2048 байт
        client_socket.send(get_response(request_string))  # отправляем ответ
        client_socket.close()
    except KeyboardInterrupt:  # если пользователь нажал Ctrl+C
        print('Stopped')
        server_socket.close()  # закрываем соединение
        exit()
 
