import json
import socket
from threading import Thread
from parametros import HOST, PUERTO, API_PORT
from api import app

def manejar_cliente(conn, addr):
    print('Cliente conectado:', addr)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Recibido:', data.decode())
            conn.sendall(data)
    finally:
        conn.close()
        print('Cliente desconectado:', addr)

def escuchar_api():
    app.run(host=HOST, port=API_PORT)

def main():
    with open('conexion.json') as f:
        config = json.load(f)
    server_socket = socket.socket()
    server_socket.bind((config['host'], config['puerto']))
    server_socket.listen()
    print('Servidor escuchando')
    api_thread = Thread(target=escuchar_api, daemon=True)
    api_thread.start()
    try:
        while True:
            conn, addr = server_socket.accept()
            Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print('Apagando servidor')
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
