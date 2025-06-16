import csv
import json
import os
from flask import Flask, request, jsonify, Response
from parametros import (TOKEN_AUTENTICACION, ARCHIVO_USUARIOS,
                        ARCHIVO_PARTIDAS, ARCHIVO_PARTIDAS_USUARIOS,
                        CARPETA_CONJUNTOS)

app = Flask(__name__)

# Utilidades

def leer_usuarios():
    usuarios = {}
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, newline='') as f:
            for nombre, estado in csv.reader(f):
                usuarios[nombre] = estado == 'True'
    return usuarios


def escribir_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, 'w', newline='') as f:
        writer = csv.writer(f)
        for nombre, estado in usuarios.items():
            writer.writerow([nombre, estado])


@app.route('/rankings')
def rankings():
    nombre = request.args.get('nombre')
    cantidad = int(request.args.get('cantidad', 5))
    datos = []
    if os.path.exists(ARCHIVO_PARTIDAS):
        with open(ARCHIVO_PARTIDAS, newline='') as f:
            for fila in csv.reader(f):
                datos.append({'id': fila[0], 'duracion': fila[1], 'conjunto': fila[2], 'ganador': fila[3]})
    return jsonify(datos[:cantidad])


@app.route('/conjuntos')
def conjuntos():
    conjuntos = []
    if os.path.isdir(CARPETA_CONJUNTOS):
        for archivo in os.listdir(CARPETA_CONJUNTOS):
            path = os.path.join(CARPETA_CONJUNTOS, archivo)
            with open(path) as f:
                lineas = f.read().splitlines()
            if lineas:
                conjuntos.append({'nombre': archivo[:-4], 'descripcion': lineas[0], 'cantidad': len(lineas) - 1})
    return jsonify(conjuntos)


def autenticar(req):
    token = req.headers.get('Authorization')
    return token == TOKEN_AUTENTICACION


@app.route('/users', methods=['POST', 'GET', 'PATCH'])
def users():
    if not autenticar(request):
        return Response('unauthorized', status=401)
    usuarios = leer_usuarios()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        usuarios[nombre] = True
        escribir_usuarios(usuarios)
        return Response(status=200)
    if request.method == 'GET':
        nombre = request.args.get('nombre')
        if nombre not in usuarios:
            return Response('no existe', status=404)
        return jsonify({'nombre': nombre, 'conectado': usuarios[nombre]})
    if request.method == 'PATCH':
        nombre = request.form.get('nombre')
        estado = request.form.get('estado') == 'True'
        if nombre not in usuarios:
            return Response('no existe', status=404)
        usuarios[nombre] = estado
        escribir_usuarios(usuarios)
        return Response(status=200)


@app.route('/games', methods=['POST'])
def games():
    if not autenticar(request):
        return Response('unauthorized', status=401)
    data = request.get_json(force=True)
    if os.path.exists(ARCHIVO_PARTIDAS_USUARIOS):
        with open(ARCHIVO_PARTIDAS_USUARIOS) as f:
            partidas = json.load(f)
    else:
        partidas = []
    partidas.append(data)
    with open(ARCHIVO_PARTIDAS_USUARIOS, 'w') as f:
        json.dump(partidas, f)
    return Response(status=200)
