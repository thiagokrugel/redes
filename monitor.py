#!/usr/bin/env python3
import socket
import sys
import threading
import mmonitor

console = threading.Thread(target=mmonitor.Console)
console.start()

porta = int(input('Porta para ouvir sensores: '))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(('', porta))
except:
   print('# erro de bind')
   sys.exit()

s.listen(5)
 
print('aguardando sensores em ', porta)

while True:
    conn, addr = s.accept()
    print('recebi uma conexao de ', addr)
    conn.send(input('oie!').encode('utf-8'))
    t = threading.Thread( target=mmonitor.TrataSensor, args=(conn,addr,))
    t.start()

print('o servidor encerrou!')
s.close()