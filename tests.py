import pyaudio
import wave


audio = pyaudio.PyAudio()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SECONDS = 5
DIRECTORY = "assets/recordings/output.wav"

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

audio_data = []


for i in range(0, int(RATE/CHUNK*SECONDS)):
    data = stream.read(CHUNK)
    audio_data.append(data)

stream.stop_stream()
stream.close()
audio.terminate()

wf = wave.open(DIRECTORY, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(audio_data))
wf.close()