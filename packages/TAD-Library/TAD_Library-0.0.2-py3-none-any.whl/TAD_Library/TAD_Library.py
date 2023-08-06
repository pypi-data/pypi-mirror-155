import socket

global client_socket

def TD_Connect(ip, port):
    global client_socket


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

def TD_SendCmd(cmd):
    global  client_socket

    client_socket.send(cmd)
