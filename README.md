# 🎙️ Speech-to-Text Comparison Tool

[![GitHub](https://img.shields.io/badge/GitHub-AminePro7-blue?style=flat&logo=github)](https://github.com/AminePro7)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)

A comprehensive toolkit for comparing different speech-to-text (STT) engines for French language transcription.

## 📋 Overview

This project provides a comparison between three popular speech-to-text engines:

1. **OpenAI Whisper** - State-of-the-art multilingual speech recognition model
2. **Faster Whisper** - Optimized version of Whisper using CTranslate2
3. **VOSK** - Offline speech recognition toolkit with word-level timestamps

All implementations are configured for French language transcription with easy-to-use command-line interfaces.

## 🔍 Comparison Results

Here's a sample comparison of the three engines transcribing the same audio file:

### OpenAI Whisper (Base model)
```
Je vous ai dit bonjour, j'ai un problème dans le PC, je veux lui aussi un problème dans le Router, ça possible. Je sais que tu es amassé.
```
*Transcription time: 2.43 seconds*

### Faster Whisper (Base model)
```
Bonsoir donc j'ai été bonjour, j'ai un problème d'en repisser, je veux lui aussi un problème d'en reproteur et ça possible, je sais que tu es amassé.
```
*Transcription time: 3.20 seconds*

### VOSK (French model 0.22)
```
cent jours donc j'ai dit bonjour j'ai un problème dans le péché et jésus les autres aussi un problème dont le routeur sabre cible je sais que tu vis un
```
*With detailed word-level timestamps*

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed (required for audio processing)
- Sufficient disk space for models (varies by model size)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AminePro7/STT-FINAL-VERSION.git
   cd STT
   ```

2. Set up each engine in its respective directory:

   **OpenAI Whisper:**
   ```bash
   cd "Whisper Base"
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install openai-whisper
   pip install ffmpeg-python
   ```

   **Faster Whisper:**
   ```bash
   cd "Faster Whisper Base"
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install faster-whisper
   pip install ffmpeg-python
   ```

   **VOSK:**
   ```bash
   cd VOSK
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install vosk
   ```

3. Download the required models:
   - For VOSK, download the French model from [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models) and extract it to the VOSK directory
   - Whisper and Faster Whisper will download models automatically on first use

## 📊 Usage

### OpenAI Whisper

```bash
cd "Whisper Base"
.\venv\Scripts\Activate.ps1
python transcrire_fr.py -m base path/to/your/audio.wav
```

Options:
- `-m, --model`: Model size (tiny, base, small, medium, large)
- `-o, --output`: Optional path to save transcription as text file

### Faster Whisper

```bash
cd "Faster Whisper Base"
.\venv\Scripts\Activate.ps1
python transcrire_fr.py -m base path/to/your/audio.wav
```

Options:
- `-m, --model`: Model size (tiny, base, small, medium, large-v2)
- `-o, --output`: Optional path to save transcription as text file

### VOSK

```bash
cd VOSK
.\venv\Scripts\Activate.ps1
python transcribe_fr.py
```

Note: Edit the `transcribe_fr.py` file to change the input audio file path.

## 🔧 Customization

- **Audio Format**: All engines work best with WAV files (16kHz, mono, 16-bit PCM)
- **Model Size**: Larger models provide better accuracy but require more computational resources
- **Language**: All implementations are configured for French but can be modified for other languages

## 📈 Performance Considerations

- **OpenAI Whisper**: Best overall accuracy, moderate speed
- **Faster Whisper**: Similar accuracy to Whisper with improved speed
- **VOSK**: Fastest performance, detailed word-level timestamps, but lower accuracy

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [VOSK](https://github.com/alphacep/vosk-api)
