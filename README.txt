==============================================================
            CHAT DE ENCRIPTACIÓN DE MENSAJES
==============================================================

Chat web para dos personas en la misma red local (Wi-Fi o router).
Cada mensaje se encripta con Fernet apenas llega al servidor y se
guarda SOLO en su versión encriptada. Al entregarlo a la otra persona,
el servidor lo desencripta. La interfaz muestra paso a paso lo que
pasa con cada mensaje (enviar -> encriptar -> recibir -> desencriptar).


--------------------------------------------------------------
 REQUISITOS
--------------------------------------------------------------
   - Python 3.8 o superior
   - Librerías: flask y cryptography (están en requirements.txt)
   - Dos computadoras conectadas a la misma red


--------------------------------------------------------------
 INSTALACIÓN Y USO
--------------------------------------------------------------
1. Instalar dependencias (solo en la computadora que será el servidor):

       pip install -r requirements.txt

2. Iniciar el servidor:

       python app.py

   En la terminal aparece el link para entrar, por ejemplo:

       Link para entrar al chat: http://192.168.1.10:5000

3. Las dos personas abren ese link en el navegador
   (la persona del servidor también).

4. Escribir un mensaje y presionar Enviar. Los mensajes nuevos
   se actualizan solos cada segundo.

Prueba rápida de la encriptación (sin abrir el chat):

       python encryted.py


--------------------------------------------------------------
 CÓMO FUNCIONA LA ENCRIPTACIÓN
--------------------------------------------------------------
   Algoritmo: Fernet (librería cryptography)
     - AES-128 en modo CBC para cifrar el texto
     - HMAC-SHA256 para firmar el mensaje y detectar cambios

   Clave: se guarda en clave.key. Si no existe, se genera sola
   la primera vez que se ejecuta el programa.

   Si un mensaje fue alterado o la clave no coincide, Fernet lo
   detecta y el chat muestra "(mensaje dañado)".


--------------------------------------------------------------
 ESTRUCTURA DEL PROYECTO
--------------------------------------------------------------
   app.py                 Servidor Flask y rutas del chat
                            /          -> página del chat
                            /enviar    -> recibe y encripta un mensaje
                            /mensajes  -> entrega mensajes desencriptados
   encryted.py            Funciones encriptar() y desencriptar()
   clave.key              Clave secreta de Fernet
   requirements.txt       Dependencias de Python
   templates/index.html   Página del chat
   static/style.css       Estilos de la interfaz
   static/chat.js         Lógica del navegador (enviar, recibir, consola)


--------------------------------------------------------------
 PROBLEMAS COMUNES
--------------------------------------------------------------
   * La otra computadora no carga el link
       -> Verificar que estén en la misma red.
       -> Permitir Python en el Firewall de Windows (red privada).

   * "Falta la dependencia 'cryptography'"
       -> Ejecutar: pip install -r requirements.txt

   * El puerto 5000 está ocupado
       -> Cerrar el otro programa que lo usa o cambiar el puerto
          en la última línea de app.py.


--------------------------------------------------------------
 NOTAS
--------------------------------------------------------------
   - Los mensajes se guardan en memoria: al cerrar el servidor
     se borran.
   - clave.key es secreta. Quien la tenga puede leer los mensajes,
     así que no se debe compartir ni subir a repositorios públicos.
   - Proyecto educativo: la conexión usa HTTP (sin HTTPS), por lo
     que no está pensado para usarse fuera de una red de confianza.
