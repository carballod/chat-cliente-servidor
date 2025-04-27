import sys
from .database import DatabaseHandler
from .socket_handler import SocketHandler

def main():
    # Función principal que inicia el servidor
    print("[*] Iniciando servidor de chat...")
    
    # Inicializar la base de datos
    if not DatabaseHandler.initialize_database():
        print("[!] No se pudo inicializar la base de datos. Abortando.")
        sys.exit(1)
    
    # Inicializar el socket del servidor
    socket_handler = SocketHandler(host='localhost', port=5000)
    if not socket_handler.initialize_socket():
        print("[!] No se pudo inicializar el socket del servidor. Abortando.")
        sys.exit(1)
    
    try:
        # Aceptar conexiones de clientes
        socket_handler.accept_connections()
    except KeyboardInterrupt:
        # Manejar interrupción por teclado (Ctrl+C)
        print("\n[!] Servidor detenido por el usuario")
    finally:
        # Cerrar recursos
        socket_handler.close()

if __name__ == "__main__":
    main()