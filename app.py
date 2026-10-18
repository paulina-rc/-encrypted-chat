# ============================================================
#  app.py
#  Chat de encriptación de mensajes - Servidor (Flask)
#
#  Cómo funciona:
#   - Esta computadora es el SERVIDOR.
#   - Las personas entran al chat abriendo el link en el navegador:
#         http://IP_DEL_SERVIDOR:5000
#   - Cada mensaje se ENCRIPTA con Fernet apenas llega al servidor
#     y se guarda solamente encriptado.
#   - Cuando la otra persona lo recibe, el servidor lo DESENCRIPTA.
# ============================================================

import socket
from datetime import datetime
from flask import Flask, render_template, request, jsonify  # type: ignore
from encriptacion import encriptar, desencriptar

app = Flask(__name__)

# Lista donde se guardan los mensajes (solo la versión encriptada)
mensajes = []


def hora_actual():
    return datetime.now().strftime("%H:%M:%S")


def obtener_ip():
    """Busca la IP de esta computadora dentro de la red local (LAN)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def paso(texto, tipo, extra=""):
    """Crea una línea para la consola y también la muestra en la terminal."""
    linea = {"hora": hora_actual(), "texto": texto, "tipo": tipo, "extra": extra}
    print(f"[{linea['hora']}] {texto} {extra}")
    return linea


# ---------------- Rutas ----------------

@app.route("/")
def inicio():
    """Página del chat. Es lo que se abre con el link."""
    return render_template("index.html", ip_servidor=obtener_ip(), mi_ip=request.remote_addr)


@app.route("/enviar", methods=["POST"])
def enviar():
    """Recibe un mensaje nuevo, lo encripta y lo guarda."""
    texto = request.json.get("texto", "").strip()
    if texto == "":
        return jsonify({"ok": False})

    consola = []
    consola.append(paso("[1] Enviando mensaje:", "enviando", texto))
    consola.append(paso("[2] Encriptando mensaje...", "encriptando"))

    texto_encriptado = encriptar(texto)

    mensajes.append({
        "id": len(mensajes) + 1,
        "de": request.remote_addr,          # IP de quien lo envió
        "encriptado": texto_encriptado,     # solo se guarda encriptado
        "hora": datetime.now().strftime("%H:%M"),
    })
    consola.append(paso("[3] Mensaje encriptado enviado", "enviado", texto_encriptado))

    return jsonify({"ok": True, "consola": consola})


@app.route("/mensajes")
def ver_mensajes():
    """El navegador pregunta cada segundo si hay mensajes nuevos.
    Los mensajes de la otra persona se desencriptan aquí."""
    desde = int(request.args.get("desde", 0))
    mi_ip = request.remote_addr
    respuesta = []

    for m in mensajes[desde:]:
        if m["de"] == mi_ip:
            # Es un mensaje mío: ya lo tengo, solo lo muestro en el chat
            respuesta.append({"id": m["id"], "mio": True, "hora": m["hora"],
                              "texto": desencriptar(m["encriptado"]), "consola": []})
        else:
            # Es un mensaje de la otra persona: se recibe y se desencripta
            consola = []
            consola.append(paso(f"[1] Nuevo mensaje de {m['de']}", "nuevo", m["encriptado"]))
            consola.append(paso("[2] Desencriptando mensaje...", "desencriptando"))
            texto = desencriptar(m["encriptado"])
            consola.append(paso("[3] Mensaje recibido", "recibido"))
            if texto is None:
                consola.append(paso("[4] Error: el mensaje fue alterado o la clave no coincide", "error"))
                texto = "(mensaje dañado)"
            else:
                consola.append(paso("[4] Mensaje desencriptado:", "desencriptado", texto))
            respuesta.append({"id": m["id"], "mio": False, "hora": m["hora"],
                              "de": m["de"], "texto": texto, "consola": consola})

    return jsonify(respuesta)


# ---------------- Inicio del servidor ----------------

if __name__ == "__main__":
    ip = obtener_ip()
    print("=" * 50)
    print("  Chat de encriptación de mensajes")
    print(f"  Link para entrar al chat: http://{ip}:5000")
    print("=" * 50)
    # host="0.0.0.0" permite que otras computadoras de la red se conecten
    app.run(host="0.0.0.0", port=5000)
