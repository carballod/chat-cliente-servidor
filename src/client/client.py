import socket

class ChatClient:
    # Clase que implementa el cliente del chat
    
    def __init__(self, host='localhost', port=5000):
        # Inicializa el cliente con la dirección y puerto del servidor
        self.host = host
        self.port = port
        self.client_socket = None
    
    def initialize_socket(self):
        # Inicializa el socket del cliente
        # Retorna: True si la inicialización fue exitosa, False en caso contrario
        try:
            # Crear un socket TCP/IP
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return True
        except socket.error as e:
            print(f"[!] Error al crear el socket: {e}")
            return False
    
    def connect_to_server(self):
        # Conecta el socket del cliente al servidor
        # Retorna: True si la conexión fue exitosa, False en caso contrario
        try:
            # Conectar al servidor en la dirección y puerto configurados
            self.client_socket.connect((self.host, self.port))
            print(f"[+] Conectado al servidor en {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"[!] Error al conectar con el servidor: {e}")
            return False
    
    def send_message(self, message):
        # Envía un mensaje al servidor y recibe la respuesta
        # Parámetros: message - El mensaje a enviar
        # Retorna: La respuesta del servidor o None si hubo un error
        try:
            # Enviar mensaje al servidor
            self.client_socket.sendall(message.encode('utf-8'))
            
            # Recibir respuesta del servidor
            response = self.client_socket.recv(1024).decode('utf-8')
            return response
        except socket.error as e:
            print(f"[!] Error al enviar/recibir datos: {e}")
            return None
    
    def close(self):
        # Cierra la conexión con el servidor
        if self.client_socket:
            self.client_socket.close()
            print("[-] Conexión cerrada")
    
    def run(self):
        # Ejecuta el cliente - método principal que inicia todo el proceso
        # Retorna: True si la operación fue exitosa, False en caso contrario
        
        # Inicializar el socket
        if not self.initialize_socket():
            print("[!] No se pudo inicializar el socket del cliente. Abortando.")
            return False
        
        # Conectar al servidor
        if not self.connect_to_server():
            print("[!] No se pudo conectar al servidor. Abortando.")
            return False
        
        try:
            # Mostrar instrucciones al usuario
            print("Instrucciones:")
            print("- Escribe tus mensajes y presiona Enter para enviarlos")
            print("- Escribe 'exito' para salir")
            print("-" * 50)
            
            # Bucle principal para enviar mensajes
            while True:
                # Solicitar mensaje al usuario
                message = input("Mensaje > ")
                
                # Verificar si el usuario quiere salir
                if message.lower() == 'exito':
                    print("[+] ¡Hasta pronto!")
                    break
                
                # Enviar el mensaje y recibir respuesta
                response = self.send_message(message)
                
                # Mostrar la respuesta del servidor
                if response:
                    print(f"Servidor: {response}")
                else:
                    print("[!] No se recibió respuesta del servidor")
        
        except KeyboardInterrupt:
            # Manejar interrupción por teclado (Ctrl+C)
            print("\n[!] Cliente detenido por el usuario")
        except Exception as error:
            # Manejar cualquier otro error
            print(f"[!] Error inesperado: {error}")
        finally:
            # Cerrar conexión en cualquier caso
            self.close()
        
        return True

def main():
    # Función principal que ejecuta el cliente
    print("[*] Iniciando cliente de chat...")
    
    # Crear y ejecutar el cliente
    client = ChatClient()
    client.run()

if __name__ == "__main__":
    main()