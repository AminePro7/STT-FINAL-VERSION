# French Audio Transcription Tool

A Python script for transcribing French audio files using the Vosk speech recognition toolkit.

## Setup

1. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the French Vosk model:
- Visit https://alphacephei.com/vosk/models
- Download `vosk-model-fr-0.22`
- Extract the model to your preferred location

## Configuration

Edit `transcribe_fr.py` and update:
- `MODEL_PATH`: Path to your downloaded Vosk French model
- `AUDIO_FILE`: Path to your French audio file (WAV format)

## Audio File Requirements

- Format: WAV
- Channels: Mono
- Sample Rate: 16000 Hz
- Bit Depth: 16-bit PCM

## Usage

```bash
python transcribe_fr.py
```

The script will output:
- Full text transcription
- Word-level timing information (optional)