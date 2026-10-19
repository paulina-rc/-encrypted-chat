// partes de la pagina
const cajaMensajes = document.getElementById("mensajes");
const consola = document.getElementById("consola");
const formulario = document.getElementById("formulario");
const campoTexto = document.getElementById("texto");

// tiempo entre cada paso de la consola (milisegundos)
const PAUSA = 900;

// id del ultimo mensaje que ya se mostro
let ultimoMensaje = 0;

// true mientras se envia o se muestra algo
// evita que se mezclen los pasos en la consola
let ocupado = false;

// limpiar html
// para que nadie pueda meter codigo en un mensaje
function limpiar(texto) {
    const div = document.createElement("div");
    div.textContent = texto;
    return div.innerHTML;
}

// pausa
function esperar(ms) {
    return new Promise(resolver => setTimeout(resolver, ms));
}

// hora para la consola
function horaActual() {
    return new Date().toLocaleTimeString("es", { hour12: false });
}

// burbuja
// azul a la derecha si es mio, gris a la izquierda si es del otro
function mostrarBurbuja(mensaje) {
    const vacio = document.getElementById("vacio");
    if (vacio) vacio.remove();

    let html = "";
    // ip de quien lo mando
    if (!mensaje.mio) {
        html += `<div class="quien">${mensaje.de}</div>`;
    }
    const clase = mensaje.mio ? "enviado" : "recibido";
    html += `<div class="burbuja ${clase}">${limpiar(mensaje.texto)}<span class="hora">${mensaje.hora}</span></div>`;

    cajaMensajes.insertAdjacentHTML("beforeend", html);
    // bajar al ultimo mensaje
    cajaMensajes.scrollTop = cajaMensajes.scrollHeight;
}

// consola: muestra las lineas una por una, con pausa
async function mostrarEnConsola(lineas) {
    for (const linea of lineas) {
        // el tipo da el color
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
    // que no se recargue la pagina
    evento.preventDefault();
    const texto = campoTexto.value.trim();
    if (texto === "" || ocupado) return;

    ocupado = true;
    try {
        // se manda al servidor, alla se encripta
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
    // para que aparezca mi burbuja
    revisarMensajes();
});

// revisar mensajes
// pide solo los mensajes nuevos al servidor
async function revisarMensajes() {
    if (ocupado) return;
    ocupado = true;
    try {
        const respuesta = await fetch(`/mensajes?desde=${ultimoMensaje}`);
        const nuevos = await respuesta.json();

        for (const mensaje of nuevos) {
            if (mensaje.id <= ultimoMensaje) continue;
            // primero los pasos, luego la burbuja
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
// asi llegan los mensajes sin recargar la pagina
setInterval(revisarMensajes, 1000);
revisarMensajes();
