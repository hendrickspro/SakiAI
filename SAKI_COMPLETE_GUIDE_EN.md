------------------------------------------------------------------------

# Source: README.md

# 🎀 Saki Kimura - Waifu AI Voice Assistant

An AI voice assistant with personality! Saki is a snarky but caring
anime girl powered by Claude AI, Whisper, and So-VITS.

## ✨ Features

-   🎤 **Voice Input**: Push-to-talk or auto-detection
-   🧠 **Claude AI**: Natural, personality-driven conversations
-   🗣️ **Custom Voice**: So-VITS for anime-style voice synthesis
-   💾 **Memory**: Remembers conversation context
-   🎨 **Customizable**: Easy personality configuration

## 📋 Prerequisites

### 1. Python 3.9+

``` bash
python --version
```

### 2. So-VITS Server

You need a running So-VITS server. Options: -
[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) -
[So-VITS-SVC](https://github.com/svc-develop-team/so-vits-svc)

### 3. API Keys

-   Anthropic API key (for Claude)

## 🚀 Installation

### 1. Clone & Setup

``` bash
unzip waifu_project_saki.zip
cd waifu_project_saki
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Rename `.env.example` to `.env` and add your API key:

``` env
ANTHROPIC_API_KEY=sk-ant-your-key-here
SOVITS_URL=http://127.0.0.1:9880
```

### 3. Add Voice Sample

Place your reference audio in:

    character_files/main_sample.wav

### 4. Start So-VITS Server

Follow your So-VITS installation instructions to start the server on
port 9880.

## 🎮 Usage

### Test Installation

``` bash
python test_modules.py
```

### Basic Voice Chat

``` bash
python main.py
```

Press **SPACE** to talk, release to process.

### Streamlit Web Interface

``` bash
streamlit run streamlit_voice_app.py
```

Or for vision:

``` bash
streamlit run streamlit_vision_app.py
```

## 📁 Project Structure

    waifu_project_saki/
    ├── main.py                    # Main voice loop
    ├── streamlit_voice_app.py    # Web voice interface
    ├── streamlit_vision_app.py   # Web vision interface
    ├── test_modules.py           # Testing script
    ├── .env.example              # Environment template
    ├── .gitignore               # Git ignore rules
    ├── requirements.txt         # Dependencies
    ├── README.md               # This file
    │
    ├── audio/                  # Temporary audio files
    │   └── .gitkeep
    ├── character_files/        # Voice samples & config
    │   ├── character_config.yaml
    │   └── README.txt
    ├── data/                   # Conversation history
    │   └── .gitkeep
    ├── logs/                   # Application logs
    │   └── .gitkeep
    │
    └── process/                # Processing modules
        ├── __init__.py
        ├── asr_func/          # Speech recognition
        │   ├── __init__.py
        │   └── asr_push_to_talk.py
        ├── llm_funcs/         # LLM integration
        │   ├── __init__.py
        │   └── llm_scr.py
        └── tts_func/          # Text-to-speech
            ├── __init__.py
            └── sovits_ping.py

## ⚙️ Configuration

Edit `character_files/character_config.yaml`:

``` yaml
name: Saki Kimura
system_prompt: |
  You are Saki Kimura...
  [customize personality here]

sovits_config:
  text_lang: en
  ref_audio_path: character_files/main_sample.wav
  ...

personality_traits:
  snarky_level: 7
  helpfulness: 9
  tsundere_mode: true
```

## 🎯 Commands

While chatting: - Say **"exit"**, **"quit"**, or **"goodbye"** to end

## 🐛 Troubleshooting

### "Could not connect to So-VITS"

-   Ensure So-VITS server is running on port 9880
-   Check `SOVITS_URL` in `.env`

### "Whisper transcription empty"

-   Speak louder/clearer
-   Check microphone permissions
-   Try `method="auto_stop"` in config

### "Claude API error"

-   Verify `ANTHROPIC_API_KEY` in `.env`
-   Check API quota/billing

### "Module not found"

-   Activate virtual environment: `source venv/bin/activate`
-   Install dependencies: `pip install -r requirements.txt`

## 📝 License

MIT License

## 🙏 Credits

-   Claude AI by Anthropic
-   Whisper by OpenAI
-   So-VITS community

------------------------------------------------------------------------

Made with ❤️ and a bit of tsundere energy\~

------------------------------------------------------------------------

# Source: INSTALLATION.md

# 🔧 Guía de Instalación - Saki Kimura

## Instalación Paso a Paso

### 1. Preparar el Entorno

``` bash
# Descomprimir el proyecto
unzip waifu_project_saki.zip
cd waifu_project_saki

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 2. Instalar Dependencias

``` bash
# Instalar dependencias principales
pip install -r requirements.txt
```

**Si obtienes errores:**

#### Error con `faster-whisper`:

``` bash
# Intenta primero actualizar pip
pip install --upgrade pip setuptools wheel

# Luego instala faster-whisper
pip install faster-whisper
```

#### Error con `sounddevice`:

**En Linux (Ubuntu/Debian):**

``` bash
sudo apt-get update
sudo apt-get install libportaudio2 portaudio19-dev
pip install sounddevice
```

**En macOS:**

``` bash
brew install portaudio
pip install sounddevice
```

**En Windows:** Generalmente funciona sin problemas. Si falla:

``` bash
pip install sounddevice --no-cache-dir
```

#### Error con `keyboard`:

**En Linux necesitas permisos root para usar keyboard:**

``` bash
# Opción 1: Ejecutar con sudo (no recomendado)
sudo python main.py

# Opción 2: Agregar tu usuario al grupo input
sudo usermod -a -G input $USER
# Luego cierra sesión y vuelve a entrar
```

**Alternativa sin keyboard:** Puedes modificar el código para usar otra
forma de input.

### 3. Configurar Variables de Entorno

``` bash
# Copiar el template
cp .env.example .env

# Editar .env con tu editor favorito
nano .env
# o
code .env
# o
vim .env
```

Agregar tu API key:

``` env
ANTHROPIC_API_KEY=sk-ant-api-key-aqui
SOVITS_URL=http://127.0.0.1:9880
```

### 4. Agregar Voz de Referencia

Coloca un archivo de audio WAV en:

    character_files/main_sample.wav

Requisitos del archivo: - Formato: WAV - Duración: 5-15 segundos -
Calidad: Sin ruido de fondo - Contenido: Voz clara hablando naturalmente

### 5. Instalar y Ejecutar So-VITS

Necesitas un servidor So-VITS corriendo. Opciones:

#### Opción A: GPT-SoVITS (Recomendado)

``` bash
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS
# Seguir instrucciones del repositorio
```

#### Opción B: So-VITS-SVC

``` bash
git clone https://github.com/svc-develop-team/so-vits-svc.git
cd so-vits-svc
# Seguir instrucciones del repositorio
```

Asegúrate de que el servidor esté en el puerto 9880.

### 6. Probar la Instalación

``` bash
# Ejecutar tests
python test_modules.py
```

Deberías ver:

    ✅ Todos los imports exitosos!
    ✅ Estructura de directorios OK!
    ✅ Variables requeridas OK!
    🎉 ¡Todos los tests pasaron!

### 7. Ejecutar Saki

``` bash
python main.py
```

## 🐛 Solución de Problemas Comunes

### "ModuleNotFoundError: No module named 'X'"

``` bash
# Asegúrate de que el entorno virtual esté activado
# Verifica con:
which python  # En Linux/macOS
where python  # En Windows

# Debería mostrar una ruta dentro de tu carpeta venv/
```

### "ANTHROPIC_API_KEY no encontrada"

``` bash
# Verifica que .env exista y tenga la key
cat .env

# Asegúrate de que .env esté en el mismo directorio que main.py
ls -la
```

### "No se puede conectar a So-VITS"

``` bash
# Verifica que So-VITS esté corriendo
curl http://127.0.0.1:9880/

# Si no responde, inicia el servidor So-VITS primero
```

### "Error con keyboard en Linux"

``` bash
# Opción 1: Ejecutar con sudo (temporal)
sudo venv/bin/python main.py

# Opción 2: Agregar permisos permanentes
sudo usermod -a -G input $USER
# Cierra sesión y vuelve a entrar
```

### "Whisper no transcribe nada"

-   Habla más fuerte y claro
-   Verifica que tu micrófono funcione
-   Prueba con `method="auto_stop"` en el código
-   Verifica permisos del micrófono en tu OS

## 📦 Instalación Mínima (Sin TTS)

Si solo quieres probar Claude sin voz:

``` bash
# Instalar solo lo esencial
pip install anthropic python-dotenv

# Crear un script simple
cat > test_claude.py << 'EOF'
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hi Saki!"}]
)

print(message.content[0].text)
EOF

python test_claude.py
```

## 🎯 Instalación Recomendada por OS

### Windows

``` bash
# Todo debería funcionar out-of-the-box
pip install -r requirements.txt
```

### macOS

``` bash
# Instalar homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias del sistema
brew install portaudio

# Instalar requirements
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

``` bash
# Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential

# Instalar requirements
pip install -r requirements.txt
```

## 💡 Tips

1.  **Usa Python 3.9+**: Algunas librerías no funcionan bien en
    versiones antiguas
2.  **Entorno virtual**: SIEMPRE usa venv para evitar conflictos
3.  **Actualiza pip**: `pip install --upgrade pip` antes de instalar
4.  **Internet estable**: La instalación descarga bastantes datos
5.  **Espacio en disco**: Whisper descarga modelos (100MB-3GB según el
    modelo)

## 📞 Soporte

Si sigues teniendo problemas: 1. Revisa que tu Python sea 3.9+:
`python --version` 2. Verifica que pip funcione: `pip --version` 3.
Intenta instalar paquetes uno por uno para identificar cuál falla 4.
Busca el error específico en Google/Stack Overflow

¡Buena suerte, senpai! 🎀

------------------------------------------------------------------------

# Source: MACOS_FIX.md

# 🍎 INSTRUCCIONES ESPECIALES PARA macOS

## Problema: bus error con keyboard

El módulo `keyboard` causa conflictos en macOS. He creado una versión
modificada.

## 🔧 Solución:

### 1. Desinstalar keyboard

``` bash
pip uninstall keyboard -y
```

### 2. Reemplazar el archivo ASR

Reemplaza el archivo:

    process/asr_func/asr_push_to_talk.py

Con el archivo adjunto:

    asr_push_to_talk_macos.py

``` bash
# En terminal:
cp asr_push_to_talk_macos.py process/asr_func/asr_push_to_talk.py
```

### 3. Instalar requirements sin keyboard

``` bash
pip install -r requirements_macos.txt
```

O manualmente:

``` bash
pip install anthropic python-dotenv sounddevice soundfile numpy faster-whisper requests pyyaml
```

## 📝 Cambios en el uso:

### Antes (con keyboard):

-   Mantener presionada la barra espaciadora para grabar

### Ahora (sin keyboard):

-   Presionar ENTER para comenzar a grabar
-   Presionar ENTER de nuevo para detener

## 🎮 Métodos de grabación disponibles:

### 1. Enter (Default - Recomendado)

``` python
# Presionas Enter, hablas, presionas Enter de nuevo
record_and_transcribe(whisper_model, output_path, method="enter")
```

### 2. Auto-stop (Detección de silencio)

``` python
# Presionas Enter, hablas, se detiene automáticamente después de silencio
record_and_transcribe(whisper_model, output_path, method="auto_stop")
```

### 3. Fixed duration (Tiempo fijo)

``` python
# Presionas Enter, graba 5 segundos automáticamente
record_and_transcribe(whisper_model, output_path, method="fixed", duration=5)
```

## ✅ Verificar instalación:

``` bash
python test_simple.py
```

Deberías ver:

    ✓ numpy
    ✓ soundfile
    ✓ sounddevice
    ✓ faster-whisper
    All tests completed without crash

## 🎯 Ejecutar el programa:

``` bash
python main.py
```

Cuando veas:

    🎤 Presiona ENTER para comenzar a grabar...

1.  Presiona ENTER
2.  Habla
3.  Presiona ENTER de nuevo para detener

¡Eso es todo! 🎀

------------------------------------------------------------------------

# Source: SOVITS_SETUP_GUIDE.md

# 🔊 Solución al Error de So-VITS

## ❌ El Error:

    ❌ No se puede conectar a So-VITS en http://127.0.0.1:9880

## ✅ Dos Opciones:

------------------------------------------------------------------------

## **Opción 1: TTS Nativo (MÁS FÁCIL)** ⭐ RECOMENDADO

Usa voz de sistema sin necesidad de servidor externo.

### Instalación:

``` bash
pip install pyttsx3
```

### Uso:

``` bash
python main_simple_tts.py
```

### Ventajas:

-   ✅ Funciona inmediatamente
-   ✅ No requiere servidor externo
-   ✅ Offline (no necesita internet)
-   ✅ Gratuito
-   ✅ Bajo uso de recursos

### Desventajas:

-   ❌ Voz menos natural (robótica)
-   ❌ No es personalizable
-   ❌ No suena como anime

------------------------------------------------------------------------

## **Opción 2: So-VITS (VOZ PERSONALIZADA)** 🎨

Voz de anime personalizada con So-VITS.

### ¿Qué es So-VITS?

Un sistema de clonación de voz que puede hacer que Saki suene como un
personaje de anime real.

### Requisitos:

-   Python 3.10+
-   CUDA (GPU NVIDIA recomendada, pero funciona en CPU)
-   \~5GB de espacio en disco
-   Muestra de voz de referencia (5-15 segundos)

------------------------------------------------------------------------

## 🚀 Instalación de So-VITS:

### Método 1: GPT-SoVITS (Recomendado)

GPT-SoVITS es más moderno y fácil de usar.

``` bash
# 1. Clonar repositorio
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Descargar modelos pre-entrenados
# Sigue las instrucciones en el README del repo
```

### Método 2: So-VITS-SVC

``` bash
# 1. Clonar
git clone https://github.com/svc-develop-team/so-vits-svc.git
cd so-vits-svc

# 2. Instalar
pip install -r requirements.txt

# 3. Descargar modelos
# Descargar desde releases de GitHub
```

------------------------------------------------------------------------

## 🎤 Preparar Audio de Referencia:

Necesitas un clip de audio de la voz que quieres para Saki.

### Opción A: Usar voz de personaje de anime

1.  Busca clips de diálogo en YouTube (sin música)
2.  Descarga el audio
3.  Usa un editor para extraer 5-15 segundos de habla clara
4.  Convierte a WAV mono 16kHz

``` bash
# Convertir con ffmpeg
ffmpeg -i input.mp3 -ar 16000 -ac 1 saki_voice.wav
```

### Opción B: Grabar tu propia voz

Si quieres que Saki tenga tu voz o la de alguien más:

``` bash
# En macOS
# 1. QuickTime Player → Nueva grabación de audio
# 2. Habla 10-15 segundos con entonación natural
# 3. Guarda como saki_voice.wav
```

------------------------------------------------------------------------

## ▶️ Ejecutar Servidor So-VITS:

### GPT-SoVITS:

``` bash
cd GPT-SoVITS
source venv/bin/activate

# Ejecutar WebUI
python webui.py

# O ejecutar API server
python api.py --port 9880
```

### So-VITS-SVC:

``` bash
cd so-vits-svc
source venv/bin/activate

# Ejecutar servidor
python server.py --port 9880
```

Deberías ver:

    🎤 So-VITS server running on http://127.0.0.1:9880

------------------------------------------------------------------------

## 🔗 Configurar Saki para usar So-VITS:

Una vez que el servidor esté corriendo:

### 1. Edita `Config.swift` (si usas iOS) o `config.py`:

``` python
SOVITS_URL = "http://127.0.0.1:9880"
USE_SOVITS = True
```

### 2. Coloca tu audio de referencia:

``` bash
cp saki_voice.wav character_files/main_sample.wav
```

### 3. Ejecuta Saki:

``` bash
python main.py  # La versión original con So-VITS
```

------------------------------------------------------------------------

## 🧪 Probar So-VITS:

``` bash
# Test rápido
curl -X POST http://127.0.0.1:9880/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello senpai, this is a test!",
    "text_lang": "en",
    "ref_audio_path": "character_files/main_sample.wav"
  }' \
  --output test.wav
```

Si funciona, deberías obtener un archivo `test.wav` con la voz.

------------------------------------------------------------------------

## 🐛 Troubleshooting So-VITS:

### "Connection refused"

→ El servidor no está corriendo → Ejecuta `python server.py` o
`python webui.py`

### "Port 9880 already in use"

→ Ya hay algo corriendo en ese puerto → Cambia el puerto: `--port 9881`
→ Actualiza `SOVITS_URL` en tu config

### "Model not found"

→ No descargaste los modelos pre-entrenados → Lee el README del repo de
So-VITS

### "CUDA out of memory"

→ GPU no tiene suficiente memoria → Usa CPU: agrega `--device cpu` al
comando

### "Audio quality is bad"

→ El audio de referencia es de mala calidad → Usa un clip más limpio y
claro → Asegúrate de que sea WAV 16kHz mono

------------------------------------------------------------------------

## 📊 Comparación:

  Feature           TTS Nativo       So-VITS
  ----------------- ---------------- -------------------------
  Instalación       ⚡ Instantánea   ⏱️ \~30 min
  Calidad           😐 Robótica      🎤 Natural/Anime
  Personalización   ❌ No            ✅ Totalmente
  Recursos          💻 Bajo          🖥️ Alto (GPU ideal)
  Latencia          ⚡ Rápido        ⏱️ \~2-5s por respuesta
  Costo             💚 Gratis        💚 Gratis (open source)

------------------------------------------------------------------------

## 💡 Recomendación:

### Para empezar:

1.  **Usa `main_simple_tts.py`** (TTS nativo)
2.  Prueba que todo funcione
3.  Familiarízate con Saki

### Cuando quieras mejor voz:

1.  Dedica tiempo a configurar So-VITS
2.  Busca/graba un buen audio de referencia
3.  Experimenta con diferentes voces
4.  Cambia a `main.py` (versión con So-VITS)

------------------------------------------------------------------------

## 🔄 Cambiar entre TTS Nativo y So-VITS:

### Usar TTS Nativo:

``` bash
python main_simple_tts.py
```

### Usar So-VITS (cuando esté configurado):

``` bash
# Terminal 1: Ejecutar So-VITS
cd GPT-SoVITS
python api.py --port 9880

# Terminal 2: Ejecutar Saki
cd waifu_project_saki
python main.py
```

------------------------------------------------------------------------

## 📝 Dependencias Adicionales:

Para TTS nativo:

``` bash
pip install pyttsx3

# macOS
brew install espeak

# Linux
sudo apt-get install espeak
```

Para So-VITS:

``` bash
pip install torch torchaudio  # GPU support
pip install librosa soundfile numpy
pip install flask  # Para API server
```

------------------------------------------------------------------------

## 🎀 Resumen:

**TL;DR:** - Error = So-VITS no está corriendo - **Solución rápida**:
Usa `main_simple_tts.py` (TTS nativo) - **Solución avanzada**: Configura
So-VITS para voz de anime

¿Qué prefieres usar por ahora? 🎤
