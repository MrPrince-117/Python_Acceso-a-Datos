import socket
import threading
import time


def main():
    host = "192.168.30.20"  # Dirección IP del servidor
    port = 1234  # Puerto del servidor

    def conectar_y_manejar():
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((host, port))
                    print("Conectado al servidor.")

                    # Hilo para recibir mensajes del servidor
                    def recibir_mensajes():
                        try:
                            while True:
                                mensaje_servidor = client_socket.recv(1024).decode("utf-8")
                                if mensaje_servidor:
                                    print(f"Servidor: {mensaje_servidor}")
                                else:
                                    print("El servidor cerró la conexión.")
                                    break
                        except Exception as e:
                            print(f"Error recibiendo mensajes: {e}")

                    thread = threading.Thread(target=recibir_mensajes, daemon=True)
                    thread.start()

                    # Enviar mensajes al servidor
                    while True:
                        mensaje = input("Tu mensaje: ").strip()
                        if mensaje.lower() == "salir":
                            print("Cerrando conexión...")
                            return
                        client_socket.sendall((mensaje + "\n").encode("utf-8"))

                        # Mensaje keep-alive
                        time.sleep(10)  # Enviar un latido cada 10 segundos
                        client_socket.sendall(b"KEEP_ALIVE\n")

            except (ConnectionError, socket.error) as e:
                print(f"Error de conexión: {e}. Reintentando en 5 segundos...")
                time.sleep(5)  # Esperar antes de reintentar la conexión

    conectar_y_manejar()


if __name__ == "__main__":
    main()
