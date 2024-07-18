## Estructurar el Proyecto

project/
  app/
    main.py
    modelo_entrenado.json
    preprocessor.pkl
    requirements.txt

Es necesario tener nuestra estructura de archivos. Dependeiendo de lo que tengamos que hacer cambiara la estructura que estemos utilizando

## Dockerfile
Para escribir el Dockerfile, en este caso primero necesitamos usar la imagen de python con FROM python:3.9 

Establecer el directorio de trabajo: WORKDIR /app define /app como el directorio principal del contenedor, donde se copiaran los archivos.

Utilizamos COPY para copiar los archivos desde tu directorio local al directorio del contenedor /app.

En este caso podemos instalar dependencias
RUN pip install --no-cache-dir -r ./app/requirements.txt  

El flag --no-cache-dir evita el almacenamiento en caché de los paquetes descargados, esto mantiene limpio el contenedor.

Exponemos el puerto con 
EXPOSE 8000 
este escuchará en el puerto 8000. No se enlaza con la maquina host, pero es bueno comentarlo en el dockerfile.

Usamos
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] define el comando que se ejecutará cuando se inicie el contenedor. 

uvicorn se utiliza para servir la aplicación FastAPI en el puerto 8000, escuchando en todas las interfaces de red (0.0.0.0).

## Constuir Imagen
El comando que podemos ingresar en la terminal:

docker build -t nombre_imagen

docker build: Iniciara el proceso de construccion de la imagen

-t nombre_imagen: Se le Asigna un nombre de tu preferencia a la Imagen

## Ejecutar Imagen
Cuando la imagen se construya podemos usar el siguiente comando:
docker run -p 8000:8000 nombre_imagen

docker run: Inicia el contenedor

-d: Ejecuta el contenedor en segundo plano

-p: 8000:8000 El contenedor se enlaza desde el puerto 8000 al puerto host 8000, permitiendo la comuniacion, puedes escoger distintos puertos que conozcas estan libres

nombre_imagen: El nombre que se asigno anteriormente cuando se construyo

Tambien tenemos otras flags que se usan a menudo en Docker

-v: ruta_local:ruta_contenedor  Para Montar un directorio desde el host

-it ___ /bin/bash: Abrir la terminal dentro del contenedor

--memory: Asignar o limitar la memoria Ram en el contenedor

## Comandos Basicos de docker

docker pull : Descarga una imagen desde Docker Hub u otro registro

docker images: Listar las imágenes descargadas

docker ps: Listar los contenedores en ejecucion

docker start : Iniciar un contenedor detenido

docker stop: Detener un contenedor

docker rm : Eliminar un contenedor

docker rmi : Eliminar una imagen
