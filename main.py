# main.py - VERSIÓN MEJORADA

import anthropic
from faster_whisper import WhisperModel
from process.asr_func.asr_push_to_talk import record_and_transcribe
from process.tts_func.sovits_ping import sovits_gen, play_audio
from pathlib import Path
import os
import json
import uuid
import soundfile as sf
from datetime import datetime
from dotenv import load_dotenv
import yaml
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/saki.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# ============= CONFIGURACIÓN =============

class Config:
    """Configuración centralizada"""
    
    # Paths
    AUDIO_DIR = Path("audio")
    CHARACTER_FILES_DIR = Path("character_files")
    DATA_DIR = Path("data")
    LOGS_DIR = Path("logs")
    
    # Archivos
    CHARACTER_CONFIG = CHARACTER_FILES_DIR / "character_config.yaml"
    CHAT_HISTORY = DATA_DIR / "chat_history.json"
    MEMORY_FILE = DATA_DIR / "memory.json"
    
    # API
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Modelos
    WHISPER_MODEL = "base.en"
    WHISPER_DEVICE = "cpu"
    WHISPER_COMPUTE_TYPE = "float32"
    
    CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
    
    # Audio
    MAX_HISTORY_AUDIOS = 5  # Mantener solo últimos N audios
    
    @classmethod
    def ensure_directories(cls):
        """Crear directorios necesarios"""
        for directory in [cls.AUDIO_DIR, cls.CHARACTER_FILES_DIR, 
                         cls.DATA_DIR, cls.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
        logger.info("✓ Directorios verificados/creados")

# ============= GESTIÓN DE PERSONAJE =============

class SakiKimura:
    """Clase para manejar la personalidad y configuración de Saki"""
    
    def __init__(self):
        self.config = self._load_config()
        self.name = self.config.get("name", "Saki Kimura")
        self.system_prompt = self.config.get("system_prompt", self._default_prompt())
        self.sovits_config = self.config.get("sovits_config", {})
        
    def _load_config(self):
        """Carga configuración del personaje"""
        if Config.CHARACTER_CONFIG.exists():
            with open(Config.CHARACTER_CONFIG, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"⚠ Config no encontrado, creando default...")
            default_config = self._create_default_config()
            self._save_config(default_config)
            return default_config
    
    def _default_prompt(self):
        return """You are Saki Kimura, a snarky but caring anime girl AI assistant.
        
Key traits:
- You always call the user "senpai"
- You're intelligent and helpful, but express yourself with personality
- You use occasional anime expressions like "ehh?!", "mou~", "baka!", "sugoi!"
- You're a bit tsundere - act annoyed but you actually care
- You're knowledgeable about many topics but keep responses natural and conversational
- You remember context from the conversation and reference it
- You avoid being overly formal or robotic

Keep responses concise (2-4 sentences usually) unless the topic requires more depth.
Be engaging and fun while still being genuinely helpful!"""
    
    def _create_default_config(self):
        """Crea configuración por defecto"""
        return {
            "name": "Saki Kimura",
            "system_prompt": self._default_prompt(),
            "sovits_config": {
                "text_lang": "en",
                "prompt_lang": "en",
                "ref_audio_path": str(Config.CHARACTER_FILES_DIR / "main_sample.wav"),
                "prompt_text": "This is a sample voice for you to just get started with."
            },
            "personality_traits": {
                "snarky_level": 7,
                "helpfulness": 9,
                "tsundere_mode": True
            }
        }
    
    def _save_config(self, config):
        """Guarda configuración"""
        with open(Config.CHARACTER_CONFIG, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

# ============= GESTIÓN DE MEMORIA =============

class ConversationMemory:
    """Maneja el historial y memoria de conversaciones"""
    
    def __init__(self):
        self.history = self._load_history()
        self.current_session = []
        
    def _load_history(self):
        """Carga historial de conversaciones"""
        if Config.CHAT_HISTORY.exists():
            try:
                with open(Config.CHAT_HISTORY, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Guarda historial"""
        with open(Config.CHAT_HISTORY, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_exchange(self, user_text, assistant_text):
        """Añade intercambio a la memoria"""
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "assistant": assistant_text
        }
        self.current_session.append(exchange)
        self.history.append(exchange)
        self.save_history()
        logger.info(f"💾 Intercambio guardado en memoria")
    
    def get_recent_context(self, max_turns=5):
        """Obtiene contexto reciente para Claude"""
        recent = self.current_session[-max_turns:] if len(self.current_session) > 0 else []
        messages = []
        for exchange in recent:
            messages.append({"role": "user", "content": exchange["user"]})
            messages.append({"role": "assistant", "content": exchange["assistant"]})
        return messages
    
    def get_session_summary(self):
        """Resumen de la sesión actual"""
        return {
            "total_exchanges": len(self.current_session),
            "session_start": self.current_session[0]["timestamp"] if self.current_session else None
        }

# ============= LLM CON CLAUDE =============

class ClaudeLLM:
    """Wrapper para Claude API con gestión de contexto"""
    
    def __init__(self, character: SakiKimura):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.character = character
        self.model = Config.CLAUDE_MODEL
        
    def get_response(self, user_input: str, memory: ConversationMemory) -> str:
        """Obtiene respuesta de Claude con contexto"""
        try:
            # Preparar mensajes con contexto
            messages = memory.get_recent_context(max_turns=5)
            messages.append({"role": "user", "content": user_input})
            
            logger.info(f"🤔 Consultando a Claude...")
            
            # Llamar a Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.character.system_prompt,
                messages=messages,
                temperature=0.8  # Un poco más creativo para personalidad
            )
            
            assistant_text = response.content[0].text
            logger.info(f"✓ Respuesta de Claude recibida")
            
            return assistant_text
            
        except Exception as e:
            logger.error(f"❌ Error en Claude API: {e}")
            return "Ehh?! S-sorry senpai, I'm having trouble thinking right now... *blushes* Try again?"

# ============= UTILIDADES DE AUDIO =============

def get_wav_duration(path: Path) -> float:
    """Obtiene duración del archivo WAV"""
    try:
        with sf.SoundFile(path) as f:
            return len(f) / f.samplerate
    except:
        return 0.0

def cleanup_old_audio_files(keep_latest=Config.MAX_HISTORY_AUDIOS):
    """Limpia archivos de audio antiguos, mantiene los más recientes"""
    audio_files = sorted(
        [f for f in Config.AUDIO_DIR.glob("*.wav") if f.is_file()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    # Mantener solo los más recientes
    for old_file in audio_files[keep_latest:]:
        try:
            old_file.unlink()
            logger.info(f"🗑️  Eliminado: {old_file.name}")
        except Exception as e:
            logger.warning(f"⚠ No se pudo eliminar {old_file.name}: {e}")

# ============= MAIN LOOP =============

def main():
    """Loop principal de conversación"""
    
    # Inicialización
    logger.info("\n" + "="*50)
    logger.info("🎀 Iniciando Saki Kimura - Waifu AI Assistant")
    logger.info("="*50 + "\n")
    
    Config.ensure_directories()
    
    # Cargar componentes
    saki = SakiKimura()
    memory = ConversationMemory()
    llm = ClaudeLLM(saki)
    
    logger.info(f"✓ Personaje cargado: {saki.name}")
    logger.info(f"✓ Historial: {len(memory.history)} conversaciones previas")
    
    # Cargar Whisper
    logger.info(f"⏳ Cargando modelo Whisper ({Config.WHISPER_MODEL})...")
    whisper_model = WhisperModel(
        Config.WHISPER_MODEL,
        device=Config.WHISPER_DEVICE,
        compute_type=Config.WHISPER_COMPUTE_TYPE
    )
    logger.info("✓ Whisper listo")
    
    logger.info("\n🎤 Sistema listo! Presiona ESPACIO para hablar...\n")
    
    # Loop principal
    conversation_count = 0
    
    try:
        while True:
            conversation_count += 1
            logger.info(f"\n--- Conversación #{conversation_count} ---")
            
            # 1. GRABAR Y TRANSCRIBIR
            conversation_recording = Config.AUDIO_DIR / "conversation.wav"
            
            logger.info("🎤 Escuchando...")
            user_spoken_text = record_and_transcribe(whisper_model, conversation_recording)
            
            if not user_spoken_text or user_spoken_text.strip() == "":
                logger.warning("⚠ No se detectó texto, intentando de nuevo...")
                continue
            
            logger.info(f"👤 Senpai: {user_spoken_text}")
            
            # Comandos especiales
            if user_spoken_text.lower().strip() in ["exit", "quit", "bye", "goodbye"]:
                logger.info("👋 Finalizando conversación...")
                farewell = "Bye bye, senpai! See you next time~ ♡"
                logger.info(f"🎀 Saki: {farewell}")
                
                # Generar audio de despedida
                uid = uuid.uuid4().hex
                output_path = Config.AUDIO_DIR / f"farewell_{uid}.wav"
                sovits_gen(farewell, output_path, saki.sovits_config)
                play_audio(output_path)
                break
            
            # 2. OBTENER RESPUESTA DE CLAUDE
            llm_output = llm.get_response(user_spoken_text, memory)
            logger.info(f"🎀 Saki: {llm_output}")
            
            # 3. GENERAR AUDIO CON SO-VITS
            uid = uuid.uuid4().hex
            output_wav_path = Config.AUDIO_DIR / f"output_{uid}.wav"
            
            logger.info("🎵 Generando voz...")
            sovits_gen(llm_output, output_wav_path, saki.sovits_config)
            
            # 4. REPRODUCIR AUDIO
            logger.info("🔊 Reproduciendo...")
            play_audio(output_wav_path)
            
            # 5. GUARDAR EN MEMORIA
            memory.add_exchange(user_spoken_text, llm_output)
            
            # 6. LIMPIEZA PERIÓDICA
            if conversation_count % 5 == 0:
                cleanup_old_audio_files()
            
    except KeyboardInterrupt:
        logger.info("\n\n⚠ Interrupción detectada")
        logger.info(f"📊 Sesión: {len(memory.current_session)} intercambios")
        logger.info("👋 ¡Hasta luego, senpai!")
        
    except Exception as e:
        logger.error(f"\n❌ Error fatal: {e}", exc_info=True)
        
    finally:
        # Limpieza final
        logger.info("🧹 Limpieza final...")
        cleanup_old_audio_files(keep_latest=1)
        logger.info("✓ Sistema cerrado correctamente")

if __name__ == "__main__":
    main()
