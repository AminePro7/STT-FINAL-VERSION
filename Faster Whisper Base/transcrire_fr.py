import argparse
import os
import time
import wave
import sys
import subprocess
from faster_whisper import WhisperModel

# Définir le chemin vers FFmpeg
FFMPEG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          "ffmpeg-7.1.1-essentials_build", "bin", "ffmpeg.exe")

# Liste des modèles Faster Whisper disponibles
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large-v2"]

def verify_audio_file(audio_path):
    """Verify if the audio file exists and is readable"""
    try:
        print(f"\nVérification du fichier audio:")
        print(f"- Chemin absolu: {os.path.abspath(audio_path)}")
        print(f"- Fichier existe: {os.path.exists(audio_path)}")
        print(f"- Taille du fichier: {os.path.getsize(audio_path)} bytes")
        
        # Try to open as WAV to verify format
        try:
            with wave.open(audio_path, 'rb') as wav_file:
                print(f"- Format WAV valide")
                print(f"- Canaux: {wav_file.getnchannels()}")
                print(f"- Sample width: {wav_file.getsampwidth()}")
                print(f"- Framerate: {wav_file.getframerate()}")
        except Exception as e:
            print(f"- Erreur lecture WAV: {str(e)}")
            
        return True
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier: {str(e)}")
        return False

def transcribe_audio_french(audio_path, model_name="base", output_file=None):
    """
    Transcrit un fichier audio en utilisant Faster Whisper, en forçant la langue française.
    """
    # Convert to absolute path
    audio_path = os.path.abspath(audio_path)
    
    print(f"Chemin du fichier audio: {audio_path}")
    
    if not verify_audio_file(audio_path):
        return None

    if model_name not in AVAILABLE_MODELS:
        print(f"Erreur : Modèle '{model_name}' non valide. Modèles disponibles : {AVAILABLE_MODELS}")
        return None

    print(f"\nChargement du modèle Faster Whisper '{model_name}'...")
    try:
        # Initialiser le modèle Faster Whisper
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        print(f"Modèle '{model_name}' chargé.")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle '{model_name}': {e}")
        print("Assurez-vous d'avoir assez de RAM/VRAM pour ce modèle.")
        return None

    print(f"\nDébut de la transcription de '{audio_path}' (cela peut prendre du temps)...")
    start_time = time.time()

    try:
        # Transcription avec Faster Whisper
        segments, info = model.transcribe(
            audio_path,
            language="fr",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        # Assembler le texte complet
        transcription_text = ""
        for segment in segments:
            transcription_text += segment.text + " "
        
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"Transcription terminée en {processing_time:.2f} secondes.")

        print("\n--- Transcription ---")
        print(transcription_text.strip())
        print("---------------------\n")

        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(transcription_text.strip())
                print(f"Transcription sauvegardée dans '{output_file}'")
            except IOError as e:
                print(f"Erreur lors de l'écriture dans le fichier '{output_file}': {e}")

        return transcription_text.strip()

    except FileNotFoundError:
        print(f"Erreur : Le fichier audio '{audio_path}' n'a pas été trouvé lors de la transcription.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue pendant la transcription : {e}")
        print("Vérifiez que ffmpeg est installé et accessible dans le PATH.")
        print("Vérifiez que le fichier audio est dans un format supporté (wav, mp3, m4a, etc.).")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcrire un fichier audio en français avec Faster Whisper.")
    
    parser.add_argument("audio_file", 
                        help="Chemin vers le fichier audio à transcrire (ex: mon_audio.wav)")
    
    parser.add_argument("-m", "--model", 
                        default="base", 
                        choices=AVAILABLE_MODELS,
                        help=f"Modèle Faster Whisper à utiliser (défaut: 'base'). "
                             f"Plus gros modèles = plus précis mais plus lents/gourmands. "
                             f"Choix: {', '.join(AVAILABLE_MODELS)}")
                             
    parser.add_argument("-o", "--output", 
                        default=None, 
                        help="Chemin optionnel vers un fichier .txt pour sauvegarder la transcription.")

    args = parser.parse_args()

    # Verify FFmpeg installation
    try:
        subprocess.run([FFMPEG_PATH, '-version'], capture_output=True)
        print("FFmpeg est installé et accessible.")
    except FileNotFoundError:
        print("ERREUR: FFmpeg n'est pas installé ou n'est pas dans le PATH.")
        print("Veuillez installer FFmpeg: https://ffmpeg.org/download.html")
        sys.exit(1)

    # Ajouter le dossier bin de FFmpeg au PATH
    os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ["PATH"]

    transcribe_audio_french(args.audio_file, args.model, args.output)
