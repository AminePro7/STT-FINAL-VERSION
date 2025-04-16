import pyaudio
import wave
import sys
import time
import array
import math

def record_audio(output_filename="recorded_audio.wav", duration=5, sample_rate=16000, volume_multiplier=4.0):
    """
    Record audio from microphone and save as WAV file with amplified volume.
    
    Args:
        output_filename (str): Name of output WAV file
        duration (int): Recording duration in seconds
        sample_rate (int): Sample rate in Hz (16000 required for Vosk)
        volume_multiplier (float): Factor to increase volume (1.0 = original volume)
    """
    # Audio recording parameters
    CHANNELS = 1        # Mono audio
    CHUNK = 1024       # Record in chunks of 1024 samples
    FORMAT = pyaudio.paInt16  # 16-bit resolution

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    print('Recording...')

    # Open microphone stream
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=sample_rate,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []

    # Record audio in chunks and append to frames
    for i in range(0, int(sample_rate / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
        # Show progress
        sys.stdout.write(f"\rRecording: {i*CHUNK/sample_rate:.1f}s / {duration}s")
        sys.stdout.flush()

    print("\nFinished recording!")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Amplify the audio
    amplified_frames = []
    for frame in frames:
        # Convert bytes to array of integers
        samples = array.array('h', frame)
        
        # Amplify each sample
        for i in range(len(samples)):
            # Amplify and clip to prevent overflow
            sample = samples[i] * volume_multiplier
            sample = max(min(sample, 32767), -32768)  # Clip to 16-bit range
            samples[i] = int(sample)
        
        amplified_frames.append(samples.tobytes())

    # Save the amplified audio as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(amplified_frames))

    print(f'Audio saved to: {output_filename}')
    
    # Print audio file properties
    with wave.open(output_filename, 'rb') as wf:
        print('\nAudio file properties:')
        print(f'Channels: {wf.getnchannels()}')
        print(f'Sample width: {wf.getsampwidth() * 8} bits')
        print(f'Sample rate: {wf.getframerate()} Hz')
        print(f'Duration: {wf.getnframes() / wf.getframerate():.1f} seconds')

if __name__ == "__main__":
    # Update requirements.txt to include pyaudio
    try:
        with open('requirements.txt', 'a') as f:
            f.write('\npyaudio==0.2.13\n')
    except:
        pass

    # Get recording duration from command line argument or use default
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    
    # Record audio with amplified volume
    record_audio(duration=duration, volume_multiplier=4.0)
