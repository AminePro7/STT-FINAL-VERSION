import vosk
import sys
import os
import wave
import json

# --- Configuration ---
MODEL_PATH = "vosk-model-fr-0.22/vosk-model-fr-0.22"  # Path to your French model
AUDIO_FILE = "recorded_audio.wav"  # Your recorded audio file

if not os.path.exists(MODEL_PATH):
    print(f"Model path '{MODEL_PATH}' not found. Please check the path to your French model.")
    sys.exit(1)

if not os.path.exists(AUDIO_FILE):
    print(f"Audio file '{AUDIO_FILE}' not found. Please check the path to your recording.")
    sys.exit(1)

# Check audio file format
try:
    wf = wave.open(AUDIO_FILE, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Warning: Audio format may not be optimal.")
        print("Expected: WAV, Mono, PCM 16-bit, 16000 Hz")
    sample_rate = wf.getframerate()
    print(f"Audio sample rate: {sample_rate} Hz")
except Exception as e:
    print(f"Error opening audio file: {e}")
    sys.exit(1)

# Load Vosk model
vosk.SetLogLevel(-1)  # Reduce logging
try:
    model = vosk.Model(MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)  # Enable word timestamps
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

print("Starting transcription...")
print(f"Processing file: {AUDIO_FILE}")

# Process audio file
results = []
try:
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result_json = recognizer.Result()
            results.append(json.loads(result_json))

    # Get final result
    final_result_json = recognizer.FinalResult()
    results.append(json.loads(final_result_json))

    # Extract and display full text
    print("\n=== Transcription ===")
    full_text = ""
    for res in results:
        if 'text' in res and res['text']:
            full_text += res['text'] + " "
    
    print("\nTexte transcrit:")
    print(full_text.strip())

    # Display word timings
    print("\nDétails des mots (avec timing):")
    for res in results:
        if 'result' in res:
            for word in res['result']:
                start_time = word['start']
                end_time = word['end']
                conf = word['conf']
                word_text = word['word']
                print(f"{word_text}: {start_time:.2f}s - {end_time:.2f}s (conf: {conf:.2f})")

except Exception as e:
    print(f"Error during transcription: {e}")
finally:
    wf.close()

print("\n=== Transcription terminée ===")
