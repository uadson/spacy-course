import json
import os
from countries import COUNTRIES


def create_countries_json(filepath, countries):
    """
    Cria um arquivo JSON contendo uma lista de nomes de países.

    Args:
        filepath (str): O caminho completo para o arquivo JSON a ser criado.
        countries (list): Lista com o nome de todos os países do mundo.
    """

    # Certifica-se de que o diretório existe
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filepath, "w", encoding="utf-8") as f:  # Especifica a codificação UTF-8
        json.dump(
            countries, f, ensure_ascii=False, indent=4
        )  # ensure_ascii=False para caracteres Unicode


if __name__ == "__main__":
    filepath = os.path.join(os.getcwd(), "capitulo_2", "countries.json")
    create_countries_json(filepath, COUNTRIES)
    print(f"Arquivo countries.json criado em: {filepath}")
