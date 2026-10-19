const cajaMensajes = document.getElementById("mensajes");
const consola = document.getElementById("consola");
const formulario = document.getElementById("formulario");
const campoTexto = document.getElementById("texto");

// tiempo entre cada paso de la consola (milisegundos)
const PAUSA = 900;

let ultimoMensaje = 0;
let ocupado = false;

// limpiar html
function limpiar(texto) {
    const div = document.createElement("div");
    div.textContent = texto;
    return div.innerHTML;
}

function esperar(ms) {
    return new Promise(resolver => setTimeout(resolver, ms));
}

function horaActual() {
    return new Date().toLocaleTimeString("es", { hour12: false });
}

// burbuja
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

// consola: muestra las lineas una por una, con pausa
async function mostrarEnConsola(lineas) {
    for (const linea of lineas) {
        let html = `<div class="linea"><span class="t">${horaActual()}</span><span class="p-${linea.tipo}">${linea.texto}</span></div>`;
        // texto encriptado
        if (linea.extra) {
            html += `<span class="cifrado">${limpiar(linea.extra)}</span>`;
        }
        consola.insertAdjacentHTML("beforeend", html);
        consola.scrollTop = consola.scrollHeight;
        await esperar(PAUSA);
    }
}

// enviar
formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const texto = campoTexto.value.trim();
    if (texto === "" || ocupado) return;

    ocupado = true;
    try {
        const respuesta = await fetch("/enviar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        });
        const datos = await respuesta.json();

        if (datos.ok) {
            campoTexto.value = "";
            await mostrarEnConsola(datos.consola);
        }
    } finally {
        ocupado = false;
    }
    revisarMensajes();
});

// revisar mensajes
async function revisarMensajes() {
    if (ocupado) return;
    ocupado = true;
    try {
        const respuesta = await fetch(`/mensajes?desde=${ultimoMensaje}`);
        const nuevos = await respuesta.json();

        for (const mensaje of nuevos) {
            if (mensaje.id <= ultimoMensaje) continue;
            if (!mensaje.mio) {
                await mostrarEnConsola(mensaje.consola);
            }
            mostrarBurbuja(mensaje);
            ultimoMensaje = mensaje.id;
        }
    } catch (error) {
        console.log("No se pudo conectar con el servidor");
    } finally {
        ocupado = false;
    }
}

// cada segundo
setInterval(revisarMensajes, 1000);
revisarMensajes();
