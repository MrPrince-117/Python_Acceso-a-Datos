import socket
import threading

def main():
    try:
        # Conectar al servidor en la IP y puerto especificados
        host = "192.168.30.20"  # Dirección IP del servidor
        port = 1234             # Puerto del servidor

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print("Conectado al servidor.")

            # Enviar credenciales de administrador
            credenciales = "admin:password123"  # Ejemplo de credencial
            client_socket.sendall((credenciales + "\n").encode("utf-8"))
            print("Credenciales enviadas para privilegios de administrador.")

            # Esperar respuesta del servidor
            respuesta = client_socket.recv(1024).decode("utf-8")
            if respuesta.lower() == "autenticación exitosa":
                print("Privilegios de administrador otorgados.")
            else:
                print(f"Error de autenticación: {respuesta}")
                return  # Finalizar si no se autentica correctamente

            # Hilo para recibir mensajes del servidor
            def recibir_mensajes():
                try:
                    while True:
                        mensaje_servidor = client_socket.recv(1024).decode("utf-8")
                        if mensaje_servidor:
                            print(f"Servidor: {mensaje_servidor}")  # Imprime mensajes del servidor
                        else:
                            print("El servidor cerró la conexión.")
                            break
                except Exception as e:
                    print(f"Error recibiendo mensajes: {e}")
                    client_socket.close()

            thread = threading.Thread(target=recibir_mensajes, daemon=True)
            thread.start()

            # Leer y enviar mensajes desde la consola
            while True:
                mensaje = input("Tu mensaje (como admin): ").strip()  # Leer mensaje desde la consola
                if mensaje.lower() == "salir":
                    print("Cerrando conexión...")
                    break
                client_socket.sendall((mensaje + "\n").encode("utf-8"))  # Enviar mensaje al servidor

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
