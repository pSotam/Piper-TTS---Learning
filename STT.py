
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import time
import audioop

SAMPLE_RATE = 16000
TEMPO_SILENCIO = 3
LIMIAR = 500

q = queue.Queue()

def callback(indata, frames, time_info, status):
    q.put(bytes(indata))


modelo = Model("vosk-model-small-en-us-0.15")
reconhecedor = KaldiRecognizer(modelo, SAMPLE_RATE)

print("Aether está ouvindo...")

ultimo_som = time.monotonic()
texto_completo = []

try:
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        while True:
            data = q.get()

            # Mede o volume do áudio
            volume = audioop.rms(data, 2)

            if volume > LIMIAR:
                ultimo_som = time.monotonic()

            # Envia o áudio para o Vosk
            if reconhecedor.AcceptWaveform(data):
                resultado = json.loads(reconhecedor.Result())
                texto = resultado.get("text", "")

                if texto:
                    texto_completo.append(texto)

            # Verifica se passaram 3 segundos de silêncio
            if time.monotonic() - ultimo_som >= TEMPO_SILENCIO:
                break

    resultado = json.loads(reconhecedor.FinalResult())
    texto = resultado.get("text", "")

    if texto:
        texto_completo.append(texto)

    print("Você disse:", " ".join(texto_completo))

except KeyboardInterrupt:
    print("\nEscuta interrompida.")
