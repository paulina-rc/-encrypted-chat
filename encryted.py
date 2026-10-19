import os

try:
    from cryptography.fernet import Fernet, InvalidToken  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Falta la dependencia 'cryptography'. Instálala con: pip install cryptography"
    ) from exc

ARCHIVO_CLAVE = "clave.key"


def cargar_clave():
    # si no hay clave se crea una
    if not os.path.exists(ARCHIVO_CLAVE):
        clave = Fernet.generate_key()
        with open(ARCHIVO_CLAVE, "wb") as archivo:
            archivo.write(clave)
    with open(ARCHIVO_CLAVE, "rb") as archivo:
        return archivo.read()


fernet = Fernet(cargar_clave())


def encriptar(mensaje):
    mensaje_bytes = mensaje.encode("utf-8")
    mensaje_encriptado = fernet.encrypt(mensaje_bytes)
    return mensaje_encriptado.decode("utf-8")


def desencriptar(mensaje_encriptado):
    # si la clave no coincide devuelve none
    try:
        mensaje_bytes = fernet.decrypt(mensaje_encriptado.encode("utf-8"))
        return mensaje_bytes.decode("utf-8")
    except InvalidToken:
        return None


# prueba
if __name__ == "__main__":
    original = "Hola, esto es una prueba"
    cifrado = encriptar(original)
    print("Original:     ", original)
    print("Encriptado:   ", cifrado)
    print("Desencriptado:", desencriptar(cifrado))
