import socket
import threading
from .database import DatabaseHandler

class SocketHandler:
    # Clase que maneja todas las operaciones relacionadas con los sockets
    
    def __init__(self, host='localhost', port=5000):
        # Inicializa el manejador de sockets
        # Parámetros:
        #   host: Dirección IP del servidor
        #   port: Puerto en el que escuchar
        self.host = host
        self.port = port
        self.server_socket = None
        self.db_handler = DatabaseHandler()
    
    def initialize_socket(self):
        # Inicializa el socket del servidor
        # Retorna: True si la inicialización fue exitosa, False en caso contrario
        try:
            # Crear un socket TCP/IP
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Permitir reutilizar la dirección y el puerto
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Vincular el socket al puerto y dirección especificados
            self.server_socket.bind((self.host, self.port))
            
            # Escuchar conexiones entrantes (5 conexiones en cola como máximo)
            self.server_socket.listen(5)
            
            print(f"[+] Servidor iniciado en {self.host}:{self.port}")
            return True
        except socket.error as error:
            # Manejo de errores de socket
            print(f"[!] Error al inicializar el socket: {error}")
            return False
    
    def handle_client(self, client_socket, client_address):
        # Maneja la conexión con un cliente
        # Parámetros:
        #   client_socket: El socket del cliente
        #   client_address: La dirección del cliente (ip, puerto)
        client_ip = client_address[0]
        print(f"[+] Nueva conexión aceptada de {client_ip}")
        
        try:
            while True:
                # Recibir datos del cliente
                data = client_socket.recv(1024)
                if not data:
                    break

                # Decodificar el mensaje recibido
                message = data.decode('utf-8')
                print(f"[+] Mensaje recibido de {client_ip}: {message}")
                
                # Guardar el mensaje en la base de datos
                success, timestamp = self.db_handler.save_message(message, client_ip)
                
                # Enviar respuesta al cliente
                if success:
                    response = f"Mensaje recibido: {timestamp}"
                else:
                    response = "Error al procesar el mensaje"
                    
                client_socket.sendall(response.encode('utf-8'))
        
        except Exception as e:
            # Manejo de errores de conexión
            print(f"[!] Error al manejar la conexión con el cliente {client_ip}: {e}")
        
        finally:
            # Cerrar la conexión con el cliente
            client_socket.close()
            print(f"[-] Conexión cerrada con {client_ip}")
    
    def accept_connections(self):
        # Acepta conexiones entrantes y maneja cada una en un hilo separado
        try:
            while True:
                # Esperar por una conexión
                client_socket, client_address = self.server_socket.accept()
                
                # Crear un nuevo hilo para manejar la conexión
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        
        except KeyboardInterrupt:
            # Manejar interrupción por teclado (Ctrl+C)
            print("\n[!] Servidor detenido por el usuario")
        except Exception as error:
            # Manejar otros errores
            print(f"[!] Error al aceptar conexiones: {error}")
        finally:
            # Cerrar el socket del servidor
            if self.server_socket:
                self.server_socket.close()
                print("[-] Socket del servidor cerrado")
    
    def close(self):
        # Cierra el socket del servidor
        if self.server_socket:
            self.server_socket.close()
            print("[-] Socket del servidor cerrado")