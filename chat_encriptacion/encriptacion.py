# ============================================================
#  encriptacion.py
#  Funciones para encriptar y desencriptar los mensajes del chat
#  Algoritmo: Fernet (AES-128 en modo CBC + HMAC-SHA256)
# ============================================================

import os
from cryptography.fernet import Fernet, InvalidToken

ARCHIVO_CLAVE = "clave.key"


def cargar_clave():
    """Carga la clave secreta desde el archivo clave.key.
    Si el archivo no existe (primera vez que se corre el programa),
    crea una clave nueva y la guarda para usar siempre la misma."""
    if not os.path.exists(ARCHIVO_CLAVE):
        clave = Fernet.generate_key()          # clave aleatoria de 32 bytes en Base64
        with open(ARCHIVO_CLAVE, "wb") as archivo:
            archivo.write(clave)
    with open(ARCHIVO_CLAVE, "rb") as archivo:
        return archivo.read()


# Se crea el objeto Fernet una sola vez con la clave
fernet = Fernet(cargar_clave())


def encriptar(mensaje):
    """Recibe el mensaje normal (texto plano) y devuelve el mensaje encriptado.
    1. Convierte el texto a bytes (encode)
    2. Fernet lo cifra con AES-128 y le agrega una firma HMAC
    3. Devuelve el resultado como texto para poder guardarlo y mostrarlo"""
    mensaje_bytes = mensaje.encode("utf-8")
    mensaje_encriptado = fernet.encrypt(mensaje_bytes)
    return mensaje_encriptado.decode("utf-8")


def desencriptar(mensaje_encriptado):
    """Recibe el mensaje encriptado y devuelve el texto original.
    Si alguien modificó el mensaje o la clave no es la correcta,
    Fernet lo detecta (la firma HMAC no coincide) y se devuelve None."""
    try:
        mensaje_bytes = fernet.decrypt(mensaje_encriptado.encode("utf-8"))
        return mensaje_bytes.decode("utf-8")
    except InvalidToken:
        return None


# Prueba rápida: ejecutar "python encriptacion.py"
if __name__ == "__main__":
    original = "Hola, esto es una prueba"
    cifrado = encriptar(original)
    print("Original:     ", original)
    print("Encriptado:   ", cifrado)
    print("Desencriptado:", desencriptar(cifrado))
