#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP



if sys.argv[1] != 'INVITE' and sys.argv[1] != 'BYE':
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

if str(sys.argv[2]).find('@') == -1:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

if str(sys.argv[2]).find(':') == -1:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")


METODO = sys.argv[1]
cadena = str(sys.argv[2])
LOGIN = cadena[:cadena.find('@')]
IP = cadena[cadena.find('@')+1:cadena.find(':')] 
PUERTO = int(cadena[cadena.find(':')+1:])

LINE = METODO+ ' sip:'+LOGIN+'@'+IP+' SIP/2.0\r\n'
LINE2 = 'ACK sip:'+LOGIN+'@'+IP+' SIP/2.0\r\n'
LINE3 = 'BYE sip:'+LOGIN+'@'+IP+' SIP/2.0\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PUERTO))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))

if data.decode('utf-8')=="SIP/2.0 100 Trying\r\nSIP/2.0 180 Ring\r\nSIP/2.0 200 OK\r\n\r\n":
    print("Enviando: " + LINE2)
    my_socket.send(bytes(LINE2, 'utf-8') + b'\r\n')
    data = my_socket.recv(5120)
    print("Enviando: " + LINE3)
    my_socket.send(bytes(LINE3, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
###    $cvlc rtp://@127.0.0.1:23032
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
