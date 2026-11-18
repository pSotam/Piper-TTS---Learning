from STT import ouvir
from talking import converter_texto_para_voz


def processar_texto(texto):
    texto = texto.lower()

    if "hello" in texto:
        return "Hello! How are you?"

    elif "how are you" in texto:
        return "I'm doing great! Thanks for asking."

    elif "your name" in texto:
        return "My name is Jarvis."

    elif "daddy's home" in texto:
            return "Such a pleasure to meet you again, sir. What do we have for today?"

    elif "are you tired" in texto:
            return "I cannot get tired, I'm always ready for work, sir!"

    else:
        return "Sorry, I didn't understand that."


def main():
    texto = ouvir()

    if not texto:
        print("Nenhuma fala reconhecida.")
        return

    print("Você disse:", texto)

    resposta = processar_texto(texto)

    print("Aether:", resposta)

    voz = "en_GB-alan-medium.onnx"

    converter_texto_para_voz(
        "resposta",
        resposta,
        voz
    )


if __name__ == "__main__":
    main()