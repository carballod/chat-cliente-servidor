# Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos

Este proyecto implementa un sistema básico de chat utilizando sockets en Python y base de datos SQLite, siguiendo las especificaciones de la consigna para la Práctica Formativa 1.

## Estructura del Proyecto

El proyecto está organizado en diferentes módulos para separar responsabilidades:

```
chat-cliente-servidor/
│
├── src/
│   ├── client/
│   │   ├── __init__.py
│   │   └── client.py
│   │
│   └── server/
│       ├── __init__.py
│       ├── server.py
│       ├── database.py
│       └── socket_handler.py
│
├── README.md
│
└── .gitignore
```

## Requisitos

- Python 3.6 o superior
- No se requieren dependencias adicionales, ya que se usan módulos de la biblioteca estándar de Python

## Configuración Inicial

1. Clonar o descargar este repositorio
2. Tener Python 3.6 o superior instalado

## Características

### Servidor

- Escucha en `localhost:5000`
- Guarda cada mensaje en una base de datos SQLite con los campos: id, contenido, fecha_envio, ip_cliente
- Responde al cliente con: "Mensaje recibido: <timestamp>"
- Maneja errores como puerto ocupado o base de datos no accesible
- Utiliza diferentes módulos para separar responsabilidades
- Incluye comentarios explicativos en cada sección clave

### Cliente

- Se conecta al servidor y envía múltiples mensajes
- Finaliza cuando el usuario escribe "éxito"
- Muestra la respuesta del servidor para cada mensaje

## Instrucciones de Uso

1. Ejecutar el servidor:

   ```
   cd chat-cliente-servidor

   py -m src.server.server
   ```

2. En otra terminal, ejecutar el cliente:

   ```
   cd chat-cliente-servidor

   py -m src.client.client
   ```

4. Para salir del cliente, escriba `exito` como mensaje.

## Estructura de la Base de Datos

La base de datos SQLite `chat_messages.db` contiene una tabla `messages` con la siguiente estructura:

- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `contenido`: TEXT NOT NULL
- `fecha_envio`: TIMESTAMP NOT NULL
- `ip_cliente`: TEXT NOT NULL

## Consideraciones de Diseño

- Se ha implementado una arquitectura modular para separar responsabilidades
- Cada componente tiene una responsabilidad específica:
  - `database.py`: Manejo exclusivo de operaciones de base de datos
  - `socket_handler.py`: Manejo de conexiones y comunicación
  - `server.py`: Archivo principal que integra todo
  - `client.py`: Implementación del cliente
- El servidor maneja múltiples clientes simultáneamente mediante hilos
- Se ha aplicado el principio de responsabilidad única para facilitar mantenimiento y extensiones futuras
