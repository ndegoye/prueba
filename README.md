# DCCaida de palabras (Esqueleto)

Este repositorio contiene un ejemplo minimo del proyecto **DCCaída de palabras**.
Se incluye una estructura simple de cliente y servidor que establece una
conexion por `socket` y un servicio web usando `Flask`.

```
cliente/
  main.py         Cliente TCP basico
  parametros.py   Parametros de conexion
  conexion.json   Datos de host/puerto

servidor/
  main.py         Servidor que acepta clientes y expone una API
  parametros.py   Parametros del servidor
  conexion.json   Datos de host/puerto
```

Para probarlo se deben instalar las dependencias de `Flask` y ejecutar:

```
python servidor/main.py
python cliente/main.py
```

El cliente puede enviar mensajes que son respondidos por el servidor y
consultar la API REST que expone el servidor en `http://<host>:8000`.

Se incluyeron archivos de ejemplo dentro de `datos/` para ilustrar el
formato de usuarios y partidas. La API implementa algunos de los endpoints
descritos en el enunciado, como `/conjuntos`, `/rankings` y `/users`.
