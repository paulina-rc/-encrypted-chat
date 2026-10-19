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
    consola.append(paso("Enviando mensaje...", "enviando"))
    consola.append(paso("Encriptando mensaje...", "encriptando"))

    texto_encriptado = encriptar(texto)

    mensajes.append({
        "id": len(mensajes) + 1,
        "de": request.remote_addr,
        "encriptado": texto_encriptado,
        "hora": datetime.now().strftime("%H:%M"),
    })
    consola.append(paso("Mensaje enviado", "enviado", texto_encriptado))

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
            consola.append(paso("Mensaje recibido", "recibido", m["encriptado"]))
            consola.append(paso("Desencriptando mensaje...", "desencriptando"))
            texto = desencriptar(m["encriptado"])
            if texto is None:
                consola.append(paso("Error: no se pudo desencriptar", "error"))
                texto = "(mensaje dañado)"
            else:
                consola.append(paso("Mensaje desencriptado", "desencriptado"))
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
