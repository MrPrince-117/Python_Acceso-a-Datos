import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, filedialog

class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente TCP")

        # Variables para el socket
        self.client_socket = None
        self.conectado = False
        self.jugando = False

        # Crear la interfaz
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=50)
        self.text_area.pack(pady=10)

        self.boton_conectar = tk.Button(self.root, text="1. Conectar al servidor", command=self.conectar)
        self.boton_conectar.pack(pady=5)

        self.boton_enviar = tk.Button(self.root, text="2. Enviar mensaje", command=self.enviar_mensaje, state=tk.DISABLED)
        self.boton_enviar.pack(pady=5)

        self.boton_jugar = tk.Button(self.root, text="3. Jugar al 3 en raya", command=self.jugar_tres_en_raya, state=tk.DISABLED)
        self.boton_jugar.pack(pady=5)

        self.boton_enviar_archivo = tk.Button(self.root, text="4. Enviar archivo", command=self.enviar_archivo, state=tk.DISABLED)
        self.boton_enviar_archivo.pack(pady=5)

        self.boton_salir = tk.Button(self.root, text="5. Salir", command=self.salir)
        self.boton_salir.pack(pady=5)

        self.thread_recibir = None

    def conectar(self):
        if self.conectado:
            messagebox.showinfo("Info", "Ya estás conectado.")
            return

        host = simpledialog.askstring("Conectar", "Ingrese la IP del servidor:", initialvalue="192.168.30.20")
        port = simpledialog.askinteger("Conectar", "Ingrese el puerto del servidor:", initialvalue=1234)

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.conectado = True
            self.agregar_mensaje("Conectado al servidor.")

            # Habilitar botones
            self.boton_enviar.config(state=tk.NORMAL)
            self.boton_jugar.config(state=tk.NORMAL)
            self.boton_enviar_archivo.config(state=tk.NORMAL)

            # Iniciar hilo para recibir mensajes
            self.thread_recibir = threading.Thread(target=self.recibir_mensajes, daemon=True)
            self.thread_recibir.start()

        except Exception as e:
            self.agregar_mensaje(f"Error al conectar: {e}")
            self.conectado = False

    def recibir_mensajes(self):
        try:
            while self.conectado:
                mensaje = self.client_socket.recv(1024).decode("utf-8")
                if mensaje:
                    self.agregar_mensaje(f"Servidor: {mensaje}")
                else:
                    self.agregar_mensaje("El servidor cerró la conexión.")
                    self.desconectar()
                    break
        except Exception as e:
            self.agregar_mensaje(f"Error recibiendo mensajes: {e}")
            self.desconectar()

    def enviar_mensaje(self):
        if not self.conectado:
            messagebox.showwarning("Advertencia", "No estás conectado al servidor.")
            return

        mensaje = simpledialog.askstring("Enviar mensaje", "Escribe tu mensaje:")
        if mensaje:
            try:
                self.client_socket.sendall((mensaje + "\n").encode("utf-8"))
                self.agregar_mensaje(f"Tú: {mensaje}")
            except Exception as e:
                self.agregar_mensaje(f"Error al enviar mensaje: {e}")
                self.desconectar()

    def enviar_archivo(self):
        if not self.conectado:
            messagebox.showwarning("Advertencia", "No estás conectado al servidor.")
            return

        archivo = filedialog.askopenfilename(title="Seleccionar archivo")
        if not archivo:
            return  # Usuario canceló la selección

        try:
            with open(archivo, "rb") as f:
                contenido = f.read()

            # Enviar encabezado con el nombre del archivo
            nombre_archivo = archivo.split("/")[-1]
            self.client_socket.sendall(f"ARCHIVO {nombre_archivo}\n".encode("utf-8"))
            self.client_socket.sendall(contenido)
            self.agregar_mensaje(f"Archivo '{nombre_archivo}' enviado.")

        except Exception as e:
            self.agregar_mensaje(f"Error al enviar archivo: {e}")

    def agregar_mensaje(self, mensaje):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, mensaje + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)

    def jugar_tres_en_raya(self):
        # Implementación del juego tres en raya (anteriormente discutida)
        pass

    def desconectar(self):
        self.conectado = False
        if self.client_socket:
            self.client_socket.close()
        self.client_socket = None
        self.boton_enviar.config(state=tk.DISABLED)
        self.boton_jugar.config(state=tk.DISABLED)
        self.boton_enviar_archivo.config(state=tk.DISABLED)

    def salir(self):
        if self.conectado:
            self.desconectar()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()
