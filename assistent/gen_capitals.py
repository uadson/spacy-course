import json
import requests
import os

filepath = os.path.join(os.getcwd(), "capitals.json")


def gerar_json_capitais_api(nome_arquivo=filepath):
    """
    Gera um arquivo JSON com uma lista de capitais do mundo, obtendo os dados de uma API.

    Args:
        nome_arquivo (str, opcional): O nome do arquivo JSON a ser criado.
            Padrão: "capitais_do_mundo.json"
    """

    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP (4xx ou 5xx)
        data = response.json()

        capitais = []
        for country in data:
            if (
                "capital" in country and country["capital"]
            ):  # Verifica se o país tem uma capital definida
                capitais.extend(country["capital"])  # use extend to avoid nested lists
        # Remove duplicatas, mantendo a ordem
        capitais = list(dict.fromkeys(capitais))

        dados = {"capitais": capitais}

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo_json:
            json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)
        print(f"Arquivo JSON '{nome_arquivo}' gerado com sucesso usando dados da API.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição à API: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar a resposta JSON: {e}")
    except Exception as e:
        print(f"Erro ao gerar o arquivo JSON: {e}")


if __name__ == "__main__":
    gerar_json_capitais_api()
