// ============================================================
//  chat.js
//  Lógica del chat en el navegador:
//   - Enviar mensajes al servidor
//   - Preguntar cada segundo si hay mensajes nuevos
//   - Mostrar los pasos en la consola
// ============================================================

const cajaMensajes = document.getElementById("mensajes");
const consolaEnvio = document.getElementById("consola-envio");
const consolaRecibo = document.getElementById("consola-recibo");
const formulario = document.getElementById("formulario");
const campoTexto = document.getElementById("texto");

let ultimoMensaje = 0;   // cuántos mensajes ya se mostraron

// Evita que se pueda meter código HTML dentro de un mensaje
function limpiar(texto) {
    const div = document.createElement("div");
    div.textContent = texto;
    return div.innerHTML;
}

// Agrega una burbuja al chat
function mostrarBurbuja(mensaje) {
    const vacio = document.getElementById("vacio");
    if (vacio) vacio.remove();

    let html = "";
    if (!mensaje.mio) {
        html += `<div class="quien">${mensaje.de}</div>`;
    }
    const clase = mensaje.mio ? "enviado" : "recibido";
    html += `<div class="burbuja ${clase}">${limpiar(mensaje.texto)}<span class="hora">${mensaje.hora}</span></div>`;

    cajaMensajes.insertAdjacentHTML("beforeend", html);
    cajaMensajes.scrollTop = cajaMensajes.scrollHeight;
}

// Escribe las líneas de un proceso en la consola
function mostrarEnConsola(lineas, consola) {
    for (const linea of lineas) {
        let html = `<div class="linea"><span class="t">${linea.hora}</span><span class="p-${linea.tipo}">${linea.texto}</span>`;

        // El texto encriptado va en una línea aparte; el texto normal va al lado
        if (linea.tipo === "enviado" || linea.tipo === "nuevo") {
            html += `</div><span class="cifrado">${limpiar(linea.extra)}</span>`;
        } else if (linea.extra) {
            html += ` <span class="blanco">"${limpiar(linea.extra)}"</span></div>`;
        } else {
            html += `</div>`;
        }
        consola.insertAdjacentHTML("beforeend", html);
    }
    consola.scrollTop = consola.scrollHeight;
}

// Enviar un mensaje
formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const texto = campoTexto.value.trim();
    if (texto === "") return;

    const respuesta = await fetch("/enviar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: texto })
    });
    const datos = await respuesta.json();

    if (datos.ok) {
        campoTexto.value = "";
        mostrarEnConsola(datos.consola, consolaEnvio);
        revisarMensajes();
    }
});

// Revisar si hay mensajes nuevos
async function revisarMensajes() {
    try {
        const respuesta = await fetch(`/mensajes?desde=${ultimoMensaje}`);
        const nuevos = await respuesta.json();

        for (const mensaje of nuevos) {
            if (mensaje.id <= ultimoMensaje) continue;
            mostrarBurbuja(mensaje);
            if (!mensaje.mio) {
                mostrarEnConsola(mensaje.consola, consolaRecibo);
            }
            ultimoMensaje = mensaje.id;
        }
    } catch (error) {
        console.log("No se pudo conectar con el servidor");
    }
}

// Preguntar al servidor cada segundo
setInterval(revisarMensajes, 1000);
revisarMensajes();
