import json
import socket
from threading import Thread
import requests
from parametros import HOST, PUERTO, API_PORT


def escuchar_cliente(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print('Servidor dice:', data.decode())
    finally:
        sock.close()

def main():
    with open('conexion.json') as f:
        config = json.load(f)
    sock = socket.socket()
    try:
        sock.connect((config['host'], config['puerto']))
        print('Conectado al servidor')
        # Obtener conjuntos desde la API
        try:
            r = requests.get(f'http://{HOST}:{API_PORT}/conjuntos')
            print('Conjuntos disponibles:', r.json())
        except Exception:
            print('No se pudo consultar API')
        escucha = Thread(target=escuchar_cliente, args=(sock,), daemon=True)
        escucha.start()
        while True:
            mensaje = input('> ')
            if mensaje == 'quit':
                break
            sock.sendall(mensaje.encode())
    except ConnectionRefusedError:
        print('No se pudo conectar al servidor')
    finally:
        sock.close()


if __name__ == '__main__':
    main()
