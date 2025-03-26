import random
import os
from countries import COUNTRIES as paises

filepath = os.path.join(os.getcwd(), "capitulo_2", "paises.txt")


def gerar_texto_com_paises(nome_arquivo=filepath, linhas=100, paises=paises):
    """
    Gera um arquivo de texto com nomes de países espalhados em frases aleatórias.

    Args:
        nome_arquivo: O nome do arquivo .txt a ser criado.
        linhas: O número de linhas no arquivo.
    """

    palavras = [
        "a",
        "o",
        "de",
        "que",
        "e",
        "do",
        "da",
        "em",
        "para",
        "é",
        "com",
        "não",
        "uma",
        "os",
        "no",
        "se",
        "na",
        "por",
        "mais",
        "as",
        "dos",
        "como",
        "mas",
        "ao",
        "ele",
        "era",
        "nas",
        "tem",
        "sido",
        "entre",
        "sem",
        "meu",
        "bem",
        "seu",
        "tão",
        "onde",
        "nunca",
        "sempre",
        "muito",
        "também",
        "agora",
        "antes",
        "depois",
        "porque",
        "quando",
        "enquanto",
        "senão",
        "assim",
        "então",
        "assim",
    ]

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        for _ in range(linhas):
            num_paises = random.randint(0, 2)  # Quantidade de países por linha (0 a 2)
            paises_na_linha = random.sample(paises, num_paises)

            frase = " ".join(
                random.choice(palavras) for _ in range(random.randint(5, 15))
            )  # Frase com palavras aleatórias
            for pais in paises_na_linha:
                frase = frase.replace(
                    random.choice(frase.split()), pais, 1
                )  # Substitui palavras aleatórias por países.

            arquivo.write(frase.capitalize() + ".\n")  # Escreve a frase no arquivo.


# Exemplo de uso:  Cria o arquivo "paises.txt" com 100 linhas.
gerar_texto_com_paises()
print("Arquivo 'paises.txt' gerado com sucesso.")
