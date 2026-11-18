import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import time
import audioop

SAMPLE_RATE = 16000
TEMPO_SILENCIO = 3
TEMPO_MAXIMO = 15
LIMIAR = 1000

modelo = Model("vosk-model-small-en-us-0.15")


def ouvir():
    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        q.put(bytes(indata))

    reconhecedor = KaldiRecognizer(modelo, SAMPLE_RATE)

    print("Aether está ouvindo...")

    inicio = time.monotonic()
    ultimo_som = None
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
                # Evita ficar preso esperando áudio indefinidamente
                try:
                    data = q.get(timeout=0.5)
                except queue.Empty:
                    continue

                volume = audioop.rms(data, 2)

                if volume > LIMIAR:
                    ultimo_som = time.monotonic()

                if reconhecedor.AcceptWaveform(data):
                    resultado = json.loads(reconhecedor.Result())
                    texto = resultado.get("text", "")

                    if texto:
                        texto_completo.append(texto)

                agora = time.monotonic()

                # Encerra se não houver fala dentro do tempo máximo
                if agora - inicio >= TEMPO_MAXIMO and ultimo_som is None:
                    break

                # Encerra após 3 segundos de silêncio depois da fala
                if ultimo_som is not None:
                    if agora - ultimo_som >= TEMPO_SILENCIO:
                        break

        resultado = json.loads(reconhecedor.FinalResult())
        texto = resultado.get("text", "")

        if texto:
            texto_completo.append(texto)

        return " ".join(texto_completo)

    except KeyboardInterrupt:
        print("\nEscuta interrompida.")
        return ""