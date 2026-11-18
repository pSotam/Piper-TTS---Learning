import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

modelo = Model("vosk-model-small-en-us-0.15")

reconhecedor = KaldiRecognizer(modelo, 16000)

def listen():
    print('Say something...')

    audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype="int16")

    sd.wait()

    reconhecedor.AcceptWaveform(audio.tobytes())

    resultado = json.loads(reconhecedor.Result())

    print("You said:", resultado["text"])

listen()
