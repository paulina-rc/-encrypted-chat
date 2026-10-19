import socket
from datetime import datetime
from flask import Flask, render_template, request, jsonify  # type: ignore
from encryted import encriptar, desencriptar

app = Flask(__name__)

# mensajes encriptados
mensajes = []


def hora_actual():
    return datetime.now().strftime("%H:%M:%S")


def obtener_ip():
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
    linea = {"hora": hora_actual(), "texto": texto, "tipo": tipo, "extra": extra}
    print(f"[{linea['hora']}] {texto} {extra}")
    return linea


# rutas
@app.route("/")
def inicio():
    return render_template("index.html", ip_servidor=obtener_ip(), mi_ip=request.remote_addr)


@app.route("/enviar", methods=["POST"])
def enviar():
    texto = request.json.get("texto", "").strip()
    if texto == "":
        return jsonify({"ok": False})

    consola = []
    consola.append(paso("[1] Enviando mensaje:", "enviando", texto))
    consola.append(paso("[2] Encriptando mensaje...", "encriptando"))

    texto_encriptado = encriptar(texto)

    mensajes.append({
        "id": len(mensajes) + 1,
        "de": request.remote_addr,
        "encriptado": texto_encriptado,
        "hora": datetime.now().strftime("%H:%M"),
    })
    consola.append(paso("[3] Mensaje encriptado enviado", "enviado", texto_encriptado))

    return jsonify({"ok": True, "consola": consola})


@app.route("/mensajes")
def ver_mensajes():
    desde = int(request.args.get("desde", 0))
    mi_ip = request.remote_addr
    respuesta = []

    for m in mensajes[desde:]:
        if m["de"] == mi_ip:
            # mensaje mio
            respuesta.append({"id": m["id"], "mio": True, "hora": m["hora"],
                              "texto": desencriptar(m["encriptado"]), "consola": []})
        else:
            # mensaje del otro
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


if __name__ == "__main__":
    ip = obtener_ip()
    print("=" * 50)
    print("  Chat de encriptación de mensajes")
    print(f"  Link para entrar al chat: http://{ip}:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000)
