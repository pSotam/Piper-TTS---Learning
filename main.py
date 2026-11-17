
import subprocess
import sys
from pathlib import Path


def converter_texto_para_voz(nome, conteudo, voz):
    print("Convertendo texto para voz...")

    arquivo_saida = Path(f"{nome}.wav")

    try:
        processo = subprocess.run(
            [
                sys.executable,
                "-m",
                "piper",
                "-m",
                voz,
                "-f",
                str(arquivo_saida),
            ],
            input=conteudo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )

        print(f"Áudio criado com sucesso: {arquivo_saida.resolve()}")

    except subprocess.CalledProcessError as erro:
        print("Erro ao executar o Piper:")
        print("Código:", erro.returncode)
        print("STDOUT:", erro.stdout)
        print("STDERR:", erro.stderr)

    except FileNotFoundError as erro:
        print("Arquivo ou executável não encontrado:", erro)


def main():
    nome = "audio"
    conteudo = "Olivia Newton John"
    voz = "pt_BR-faber-medium.onnx"

    converter_texto_para_voz(nome, conteudo, voz)


if __name__ == "__main__":
    main()
