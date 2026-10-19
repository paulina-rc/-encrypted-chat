#  Encrypted Chat

> Two computers. One Wi-Fi. Secret messages.

This is a small web chat for **two people on the same network**.
Every message is locked (encrypted) before it is saved, and you can **watch it happen** in a live console under the chat.

---


And this is what you see in the console:

```
14:32:05  Enviando mensaje...
14:32:06  Encriptando mensaje...
14:32:07  Mensaje enviado
          gAAAAABn3kQx8f2...
```

On the other side:

```
14:32:08  Mensaje recibido
          gAAAAABn3kQx8f2...
14:32:09  Desencriptando mensaje...
14:32:10  Mensaje desencriptado
```

The steps show up one by one, slowly, so you can follow them.

---

##  Start in 3 steps

**1. Install** (only on the computer that will be the server)

```bash
pip install -r requirements.txt
```

**2. Run**

```bash
python app.py
```

**3. Open the link** that shows up in the terminal, on both computers:

```
Link para entrar al chat: http://192.168.1.10:5000
```

---

##  The secret key

The lock and the key are made with **Fernet** (from the `cryptography` library):

| What           | How                                        |
| -------------- | ------------------------------------------ |
| Lock the text  | AES-128                                    |
| Detect changes | HMAC-SHA256 (a kind of digital seal)       |
| The key        | Saved in `clave.key`, made automatically the first time |

If someone changes a message, or the key is not the same, the chat shows **`(mensaje dañado)`** instead of the text.

---

## What's inside

```
 chat_encriptacion
├── app.py              → the server (Flask)
├── encryted.py         → lock and unlock functions
├── requirements.txt    → what to install
├── templates/
│   └── index.html      → the chat page
└── static/
    ├── style.css       → how it looks
    └── chat.js         → send, receive, and the console
```


