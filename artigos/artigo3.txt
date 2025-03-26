"""
Por que usar o Comparador e não somente expressões regulares?

    - Permite a comparação com objetos Doc e não apenas texto (strings)
    - Permite a comparação com os tokens e seus atributos
    - Utiliza a previsão de um modelo
    - Exemplo: "duck" (verbo) vs. "duck" (substantivo)

Além de comparar com texto (strings), que é o caso das expressões regulares, o Comparador(Matcher) também analisa os
objetos Doc e Token.
Ele é bem mais flexível: você pode fazer a comparação no texto mas também nos seus atributos léxicos.
Você pode até criar regras que usam previsões de um modelo.
Por exemplo, você pode procurar a palavra "duck" (em inglês) somente se for um verbo e não um substantivo.

--- Expressões de correspondência ---

    Listas de dicionários, uma por token

    Corresponde exatamente ao texto de um token:
    [{"TEXT": "iPhone"}, {"TEXT": "X"}]

    Corresponde a atributos léxicos:
    [{"LOWER": "iphone"}, {"LOWER": "x"}]

    Corresponde a qualquer atributo de um token:
    [{"LEMMA": "buy"}, {"POS": "NOUN"}]


As expressões de correspondência são listas de dicionários.
Cada dicionário se relaciona a um token.
As chaves são os nomes dos atributos dos tokens, mapeadas para os valores esperados.
Neste exemplo, estamos procurando por dois tokens com o texto: "iPhone" e "X".
Podemos fazer a correspondência de acordo com outros atributos dos tokens.
Neste exemplo estamos procurando dois tokens cuja forma em letras minúsculas corresponda a "iphone" e "x".
Podemos até escrever expressões usando atributos previstos por um modelo.
Neste exemplo estamos procurando um token cujo lema seja "comprar" seguido de um substantivo.
O lema é o formato base da palavra, então esta expressão terá correspondência com frases como "comprar livros"
ou "comprando livros".
"""

"""
Para usar uma expressão, devemos importar o comparador spacy.matcher.
É necessário carregar um fluxo (pipeline) de processamento e criar um objeto nlp.
O comparador será inicializado com o vocabulário nlp.vocab. 
O método matcher.add permite adicionar uma expressão ao comparador. 
O primeiro argumento é o identificador único da expresssão que terá correspondência no texto. 
O segundo argumento é uma lista de expressões de correspondência.
Para fazer a correspondência de uma expressão em um texto, chame o comparador (matcher) e passe o texto como parâmetro.
Ele retornará as correspondências.
"""
print("\n1")
import spacy

# Importa o comparador (Matcher)
from spacy.matcher import Matcher

# Carregar o fluxo (pipeline) de processamento e criar o objeto nlp
nlp = spacy.load("pt_core_news_md")

# Inicializar o comparador com o vocabulário
matcher = Matcher(nlp.vocab)

# Adicionar a expressão ao comparador
pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
matcher.add("IPHONE_PATTERN", [pattern])

# Processar um texto
doc = nlp("Data de lançamento do iPhone X vazada")

# Chamar o matcher no doc
matches = matcher(doc)

"""
Quando você usa o comparador em um documento (doc), ele retorna uma lista de tuplas.
Cada tupla consiste em três valores: o ID a expressão, o índice inicial e o índice final da partição em que houve 
correspondência.
Desta forma é possível iterar nas correspondências e criar um objeto partição Span : a parte do texto correspondente 
(do índice inicial até o índice final).
"""

# Iterar nas correspondências
for token in doc:
    print(token.text, token.pos_)

print("\n")
for match_id, start, end in matches:
    # Selecionar a partição que houve correspondência
    matched_span = doc[start:end]
    print(f"Correspondências: {matched_span.text}")

print("\n2")
"""
---- Expressões com atributos léxicos ----

Este é um exemplo de uma expressão mais complexa que utiliza atributos léxicos.
Estamos procurando por cinco tokens:
Um token constituído de apenas dígitos.
Três tokens sem diferenciação de maísculas e minúsculas de "fifa", "mundo" e "copa".
E um token que é uma pontuação.
Esta expressão tem correspondência com "Copa do Mundo FIFA 2002:".
"""

# Carregar o fluxo (pipeline) de processamento e criar o objeto nlp
nlp = spacy.load("pt_core_news_md")

# Inicializar o comparador com o vocabulário
matcher = Matcher(nlp.vocab)

pattern = [
    {"LOWER": "copa"},
    {"LOWER": "do"},
    {"LOWER": "mundo"},
    {"LOWER": "fifa"},
    {"IS_DIGIT": True},
    {"IS_PUNCT": True},
]

matcher.add("COPA_DO_MUNDO_FIFA_PATTERN", [pattern])

# Processar um texto
doc = nlp("Copa do Mundo FIFA 2002: Brasil venceu!")

# Chamar o matcher no doc
matches = matcher(doc)

# Iterar nas correspondências

for match_id, start, end in matches:
    # Selecionar a partição que houve correspondência
    matched_span = doc[start:end]
    print(f"Correspondências: {matched_span.text}")

print("\n3")
"""
Neste exemplo, estamos procurando por dois tokens:
Um verbo com o lema "amar", seguido de um substantivo.
Esta expressão terá correspondência com "amava cachorros" e "amo gatos".
"""

# Carregar o fluxo (pipeline) de processamento e criar o objeto nlp
nlp = spacy.load("pt_core_news_md")
matcher = Matcher(nlp.vocab)
pattern = [
    {"POS": "PRON"},
    {"POS": "VERB"},
    {"POS": "NOUN"},
]
matcher.add("AMO_GATOS_PATTERN", [pattern])
doc = nlp("Eu amava cachorros, mas agora eu amo gatos")
matches = matcher(doc)
for token in doc:
    print(token.text, token.pos_)
print("\n")
for match_id, start, end in matches:
    matched_span = doc[start:end]
    print(f"Correspondências: {matched_span.text}")

print("\n4")
"""
Utilizando operadores e quantificadores

Operadores e quantificadores permitem definir quantas vezes deverá haver correspondência 
com a expressão. Eles podem ser usados com a chave "OP".
Neste exemplo, o operador "?" faz com que a ocorrência seja opcional, então a expressão 
corresponderá a um token com o lema "comprar", um artigo (opcional) e um substantivo.

"OP" pode ter um dos quatro valores abaixo:

"!" nega o valor do token, então corresponde a nenhuma ocorrência.
"?" faz o token opcional, corresponde a 0 ou 1 ocorrência.
"+" corresponde ao token uma ou mais ocorrências do token.
E "*" corresponde a zero ou mais ocorrências do token.
Os operadores dão poder às suas expressões, mas por outro lado são mais complexos, 
use-os com sabedoria.

"""
pattern = [
    {"POS": "VERB"},
    {"POS": "DET", "OP": "?"},
    {"POS": "NOUN"},
]

matcher.add("COMPRANDO_SMARTPHONE_PATTERN", [pattern])
doc = nlp("Comprei um smartphone. Agora estou comprando aplicativos.")
matches = matcher(doc)
for token in doc:
    print(token.text, token.pos_)
print("\n")
for match_id, start, end in matches:
    matched_span = doc[start:end]
    print(f"Correspondências: {matched_span.text}")

print("\n5")
doc = nlp(
    "Após fazer a atualização do iOS você não irá perceber uma mudança radical "
    "na sua interface: nada parecido com a reviravolta estética que foi feita com o iOS 7. A "
    "maioria da roupagem do iOS 11 permanece a mesma que o iOS 10. Mas você irá descobrir "
    "alguns ajustes se você procurar nos detalhes."
)

pattern = [{"TEXT": "iOS"}, {"IS_DIGIT": True}]
matcher.add("IOS_VERSION_PATTERN", [pattern])
matches = matcher(doc)
print("Total de correspondências encontradas:", len(matches))
for match_id, start, end in matches:
    print("Correspondência encontrada:", doc[start:end].text)

print("\n6")
doc = nlp(
    "Eu baixei o Fortnite em meu computador e não consigo abrir o jogo de jeito algum. Me ajudem? "
    "Mas quando eu estava baixando o Minecraft, eu tinha a versão do Windows que é "
    "uma pasta .zip e eu usei o aplicativo padrão para descompactá-lo. Será que "
    "eu preciso baixar o Winzip também? "
)
pattern = [{"LEMMA": "baixar"}, {"POS": "DET"}, {"POS": "PROPN"}]
matcher.add("DOWNLOAD_THINGS_PATTERN", [pattern])
matches = matcher(doc)
print("Total de correspondências encontradas:", len(matches))
for match_id, start, end in matches:
    print("Correspondência encontrada:", doc[start:end].text)

print("\n7")
doc = nlp(
    "Os recursos do aplicativo incluem um design bonito e moderno, busca inteligente, "
    " rótulos automáticos e resposta de voz opcional."
)
pattern = [
    {"POS": "NOUN"},
    {"POS": "ADJ", "OP": "?"},
    {"TEXT": "e", "OP": "?"},
    {"POS": "ADJ"},
]
matcher.add("ADJ_NOUN_PATTERN", [pattern])
matches = matcher(doc)
print("Total de correspondências encontradas:", len(matches))
for match_id, start, end in matches:
    print("Correspondências encontradas:", doc[start:end].text)
