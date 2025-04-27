import sqlite3
import datetime
import os

# Configuración de la ruta de la base de datos
DB_NAME = os.path.join(os.path.dirname(__file__), 'chat_messages.db')

class DatabaseHandler:
    # Clase que maneja todas las operaciones relacionadas con la base de datos
    
    @staticmethod
    def initialize_database():
        # Inicializa la base de datos SQLite para almacenar los mensajes
        # Crea la tabla si no existe
        # Retorna: True si la operación fue exitosa, False en caso contrario
        try:
            # Asegurar que el directorio exista
            os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
            
            # Conectar a la base de datos (la crea si no existe)
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # Crear tabla de mensajes con los campos requeridos: id, contenido, fecha_envio, ip_cliente
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TIMESTAMP NOT NULL,
                ip_cliente TEXT NOT NULL
            )
            ''')
            
            # Guardar cambios y cerrar conexión
            conn.commit()
            conn.close()
            print("[+] Base de datos inicializada correctamente")
            return True
        except sqlite3.Error as error:
            # Manejo de errores de base de datos
            print(f"[!] Error al inicializar la base de datos: {error}")
            return False
    
    @staticmethod
    def save_message(message, client_ip):
        # Guarda un mensaje en la base de datos SQLite
        # Parámetros:
        #   message: El mensaje a guardar
        #   client_ip: La dirección IP del cliente
        # Retorna: Tupla (exito, timestamp)
        try:
            # Obtener la fecha y hora actual
            timestamp = datetime.datetime.now()
            
            # Conectar a la base de datos
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # Insertar el mensaje en la tabla
            cursor.execute('''
            INSERT INTO messages (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
            ''', (message, timestamp, client_ip))
            
            # Guardar cambios y cerrar conexión
            conn.commit()
            conn.close()
            print(f"[+] Mensaje guardado en la base de datos: {message}")
            return True, timestamp
        except sqlite3.Error as error:
            # Manejo de errores al guardar en la base de datos
            print(f"[!] Error al guardar el mensaje en la base de datos: {error}")
            return False, None