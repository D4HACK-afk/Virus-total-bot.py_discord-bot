<div align="center">

# bot_an — Security & Malware Scanner Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/Discord.py-v2.0%2B-5865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![VirusTotal](https://img.shields.io/badge/VirusTotal-API_v3-0051C3.svg?style=for-the-badge&logo=virustotal&logoColor=white)](https://www.virustotal.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

**Bot de Discord para análisis automatizado de malware mediante firmas SHA-256, API de VirusTotal y caché local en SQLite.**

</div>

---

## Descripción del Proyecto

**bot_an** es una herramienta desarrollada en Python orientada a la automatización de análisis de seguridad en comunidades de Discord[cite: 3, 5]. Permite a los usuarios verificar si archivos adjuntos (imágenes, ejecutables, documentos) contienen malware sin exponer binarios sensibles a terceros y optimizando el consumo de cuotas de API externas mediante almacenamiento en caché local[cite: 3, 4, 5].

---

## Características Destacadas

- 🔍 **Escaneo Inteligente:** Procesa archivos adjuntos calculando su huella criptográfica SHA-256 en tiempo real.
- ⚡ **Integración Asíncrona con VirusTotal:** Consulta el estado de seguridad de los archivos consumiendo la API v3 mediante peticiones asíncronas (`vt-py`).
- 💾 **Caché de Resultados (SQLite3):** Almacena las consultas previas para responder al instante si un archivo ya fue analizado, evitando llamadas innecesarias a la API[cite: 3, 4].
- 🧹 **Gestión de Archivos Temporales:** Elimina automáticamente del servidor local los adjuntos descargados una vez procesados.
- 🧮 **Módulos Adicionales:** Incluye calculadora con soporte para expresiones regulares (RegEx) e inspección de usuarios/servidor.
- 🔒 **Seguridad de Credenciales:** Manejo de Tokens y API Keys a través de variables de entorno (`.env`)[cite: 3, 4].

---

## 🛠️ Tecnologías y Librerías

| Componente | Tecnología / Librería | Función |
| :--- | :--- | :--- |
| **Lenguaje** | Python 3.10+ | Núcleo del proyecto |
| **Framework Bot** | `discord.py` | Conexión y manejo de eventos con Discord |
| **Integración API** | `vt-py` | Cliente asíncrono para VirusTotal |
| **Base de Datos** | `sqlite3` | Persistencia y caché local de resultados (`scans.db`) |
| **Seguridad / Hashes** | `hashlib` | Generación de firmas SHA-256[cite: 4] |
| **Variables de Entorno** | `python-dotenv` | Lectura segura de secretos desde `.env`[cite: 3, 4] |

---

## Flujo de Trabajo (`$scan`)

```text
       [ Adjunto enviado en Discord ]
                     │
                     ▼
        [ Descarga temporal local ]
                     │
                     ▼
         [ Generar Hash SHA-256 ]
                     │
                     ▼
         ¿Existe en SQLite (scans.db)?
          ├── SÍ ──► [ Retornar caché local ]
          └── NO ──► [ Consultar API VirusTotal ]
                            │
                            ▼
                [ Guardar resultado en DB ]
                            │
                            ▼
          [ Responder resultado al usuario ]
                            │
                            ▼
             [ Eliminar archivo temporal ]

'''
---

##1) Instalación y Configuración Local

git clone [https://github.com/tu_usuario/bot_an.git](https://github.com/tu_usuario/bot_an.git)
cd bot_an

##2) Crear y activar un entorno virtual

python3 -m venv myenv
source myenv/bin/activate

##3) Instalar dependencias

pip install -r requirements.txt

##4) Configurar variables de entorno (.env)

DISCORD_TOKEN=tu_discord_bot_token_aqui
virustotal_key=tu_virustotal_api_key_aqui

##5)Iniciar el Bot

python3 bot.py
