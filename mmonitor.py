CONSOLE = None
SENSORES = {}

def Console():
  global CONSOLE
  global SENSORES

  import socket
  import sys
  print('função do console ligada com sucesso')
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind(('127.0.0.1', 8888))
  except:
    print('# erro de bind')
    sys.exit()

  s.listen(1)

  while True:
    conn, addr = s.accept()
    print('console ativado ')
    CONSOLE = conn

    ID = CONSOLE.recv(10).decode()
   
    CONSOLE.send(f'{ID}\r\n'.encode()) 
    while True:
        data = CONSOLE.recv(200).decode()
        if not data:
            print('Console encerrou')
            CONSOLE = None
            break
        if(len(data) < 4):
            # ignorar quebras de linha do Putty
            continue
        try:
            (sensor, comando) = data.split(' ', 1)
            if sensor in SENSORES:
                SENSORES[sensor].send(comando.encode())
            else:
                CONSOLE.send('Esse sensor nao existe\r\n'.encode())
                CONSOLE.send(f'Sensores existentes: {SENSORES.keys()}')              
        except:
            CONSOLE.send('Digite SENSOR_ID COMANDO\r\n'.encode()) 
            print(data)


def TrataSensor(conn, addr):
  global CONSOLE  
  global SENSORES 
  print('iniciei a função trataSensor')
  # O sensor deve enviar seu ID apos a conexao
  sensor = conn.recv(10).decode()
  SENSORES[sensor] = conn

  print('o sensor ', sensor, ' registrado no socket', conn.getpeername())
 
  while True:
        try:
          data = conn.recv(100)
          if not data:
            break

          print('sensor ', sensor, ' enviou ', data.decode())

          print('esqueci de fazer o exercicio 2C')
          if CONSOLE is not None:
            CONSOLE.send(f'sensor {sensor} enviou {data.decode()}')          

        except:
          break
       
  conn.close()     
  print('O sensor ', sensor, ' encerrou')
  SENSORES.pop(sensor)


