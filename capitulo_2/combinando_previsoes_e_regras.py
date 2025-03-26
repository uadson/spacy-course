"""
Previsões estatísticas versus regras

                        |  Modelos estatísticos 	                        | Sistemas baseados em regras
-----------------------------------------------------------------------------------------------------------------------
Casos de uso 	        |  aplicação precisa generalizar a                  |
                        |  partir de exemplos 	                            | dicionário com número finito de exemplos
-----------------------------------------------------------------------------------------------------------------------
Exemplos do mundo real 	|  nomes de produtos, nomes de pessoas, relações    |
                        |  sujeito/objeto                                   | países do mundo, cidades, nomes de
                        |                                                   | remédios, raças caninas
-----------------------------------------------------------------------------------------------------------------------
Recursos da spaCy 	    |  reconhec. de entidades, análise sintática,       |
                        |  tag. de classes gramaticais                      | toquenizador, Matcher, PhraseMatcher
                        |                                                   |
-----------------------------------------------------------------------------------------------------------------------

Modelos estatísticos são úteis se sua aplicação necessita generalizar a partir de alguns exemplos.

Por exemplo, a tarefa de identificar produtos ou nomes de pessoas pode se beneficiar de um modelo treinado.
Ao invés de prover uma lista de todos os possíveis nomes de pessoas, sua aplicação poderá prever se uma partição
de tokens é um nome próprio. De maneira similar, é possível prever termos sintáticos e identificar relações entre
sujeito e objeto.
Para alcançar esse objetivo você pode usar alguns recursos da biblioteca spaCy: reconhecimento de entidades,
analisador sintático e o tagueador de classes gramaticais.

Por outro lado, estratégias baseadas em regras são úteis se há um número finito de ocorrências que você deseja
identificar. Por exemplo, todos os países ou cidades do mundo, nomes de remédios ou raças de cachorros.

Na biblioteca spaCy, você pode alcançar esse objetivo com regras de toquenização personalizadas,
bem como usando o Comparador (Matcher) e o Comparador de frases (PhraseMatcher).

No último capítulo você aprendeu a utilizar o comparador baseado em regras para identificar padrões complexos em seus
textos.

Recapitulando: o Comparador é inicializado com o vocabulário compartilhado, geralmente o nlp.vocab.

Expressões são listas de dicionários, e cada dicionário descreve um token e seus atributos.
Expressões podem ser adicionadas ao Comparador utilizando o método matcher.add.

Operadores permitem que você especifique a frequência de correspondência de um token.
Por exemplo: "+" significa uma ou mais ocorrências.

Chamar o Comparador em um objeto Doc retornará uma lista de correspondências.
Cada correspondência é uma tupla consistindo de um identificador ID, e o índice do início e final do token no documento.

"""

print("\n1")
import spacy
import json
import os
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

nlp = spacy.load("pt_core_news_md")
matcher = Matcher(nlp.vocab)

# Expressões são listas de dicionários descrevendo os tokens
pattern = [{"LEMMA": "amar", "POS": "VERB"}, {"LOWER": "gatos"}]
matcher.add("LOVE_CATS", [pattern])

# Operadores podem determinar a frequência de correspondência de um token
pattern = [{"TEXT": "muito", "OP": "+"}, {"TEXT": "feliz"}]
matcher.add("VERY_HAPPY", [pattern])

# Chamar o comparador no documento doc retorna uma lista com tuplas (match_id, start, end)
doc = nlp("Eu amo gatos e estou muito muito feliz")
matches = matcher(doc)

for match_id, start, end in matches:
    match_span = doc[start:end]
    print(f"Correspondências: {match_span.text}")

"""
Adicionando previsões estatísticas

Esse é um exemplo de uma regra do Comparador para "golden retriever".

Se iterarmos nas correspondências retornadas pelo Comparador, podemos obter o identificador da correspondência 
e o índice do início e do final da partição correspondente. 
Podemos então analisar melhor o resultado. 
Objetos Span nos dão acesso ao documento original e a todos os outros atributos e anotações linguísticas 
previstas por um modelo.

Por exemplo, podemos obter o token raiz de uma partição. 
Se a partição consiste de um ou mais tokens, este é o token que define a categoria da frase. 
Por exemplo, o token raiz de "Golden Retriever" é "Retriever". 
Podemos também obter o token cabeçalho de um token raiz. Este é o "pai" sintático que governa a frase. 
Neste exemplo, o token cabeçalho é o verbo "tive".

E finalmente podemos obter o token anterior e seus atributos. 
Neste exemplo, é um determinante, o artigo "um".
"""
print("\n2")
matcher = Matcher(nlp.vocab)
matcher.add("DOG", [[{"LOWER": "golden"}, {"LOWER": "retriever"}]])
doc = nlp("Eu nunca tive um Golden Retriever")

for match_id, start, end in matcher(doc):
    span = doc[start:end]
    print(f"Partição: {span.text}")
    # Obter o token raiz e o token cabeçalho da partição
    print(f"Raiz do token: {span.root.text}")
    print(f"Cabeção do token: {span.root.head.text}")
    # Obter o token anterior e seu marcador de classe gramatical
    print(f"Token anterior: {doc[start - 1].text, doc[start - 1].pos_}")

print("\n3")
"""
Correspondência eficiente de frases

O Comparador de frases é outra ferramenta útil para identificar sequências de palavras em seus textos.
Ele realiza uma busca por palavras-chave no documento, mas ao invés de apenas procurar por strings, 
ele permite acesso aos tokens e os contextos.

Ele recebe o objeto Doc como expressão.
E também é muito rápido.
Por tudo isso ele é muito útil para comparar longos dicionários e listas de palavras em grandes volumes de texto.


    O Comparador de frases PhraseMatcher é similar a expressões regulares ou a busca por palavras-chave, 
    mas com acesso aos tokens!
    Recebe o objeto Doc como expressão
    Mais eficiente e mais rápido que o Comparador Matcher
    Excelente para comparar listas grandes de palavras.
    
Aqui está um exemplo:

O Comparador de frases pode ser importado a partir de spacy.matcher e segue a mesma lógica que o Comparador padrão.
Ao invés de uma lista de dicionários, passamos um objeto Doc como expressão.
Nós podemos iterar nos resultados da comparação, que contêm o identificador (ID) da comparação, e o início e o 
final da equivalência. Isso permite criar objetos partição Span e analisá-los em um contexto.
"""

matcher = PhraseMatcher(nlp.vocab)
pattern = nlp("Golden Retriever")
matcher.add("DOG", [pattern])
doc = nlp("Eu nunca tive um Golden Retriever")

# Iterar nas correspondências
for match_id, start, end in matcher(doc):
    # Obter a participação que houve correspondência
    span = doc[start:end]
    print(f"Partição: {span.text}")

print("\n4")
"""
Pattern 1. Correspondência de todas as combinações de maiúsculas e minúsculas de "Amazon" seguido de um substantivo próprio
iniciado com letra maiúscula.

Pattern 2. Correspondência de todas as combinações maiúsculas e minúsculas de "sem anúncios", precedido de um
substantivo.
"""

doc = nlp(
    " Twitch Prime, um programa de regalias para os membros da Amazon Prime que "
    " oferece saques gratuitos, jogos e outros benefícios, está abandonando uma "
    " de suas melhores funcionalidades: visualização sem anúncios . De acordo com "
    " um email enviado hoje aos membros da Amazon Prime, a partir de 14 de Setembro, "
    " a visualização sem anúncios não estará mais inclusa no Twitch Prime para novos "
    " membros. No entanto, membros com assinaturas anuais poderão desfrutar da "
    " visualização sem anúncios até o momento da renovação da assinatura. Aqueles com "
    " assinaturas mensais terão acesso à visualização sem anúncios até 15 de Outubro."
)

pattern1 = [
    {"LOWER": "amazon"},  # maiúsculas e minúsculas
    {
        "IS_TITLE": True,
        "POS": "PROPN",
    },  # seguido de um substantivo próprio iniciado com a letra maiúscula
]

pattern2 = [
    {"POS": "NOUN"},  # substantivo
    {"LOWER": "sem"},  # maiúsculas e minúsculas
    {"LOWER": "anúncios"},  # maiúsculas e minúsculas
]

matcher = Matcher(nlp.vocab)
matcher.add("PATTERN1", [pattern1])
matcher.add("PATTERN2", [pattern2])

print(f"Quantidade de correspondências: {len(matcher(doc))}")
for match_id, start, end in matcher(doc):
    print(doc.vocab.strings[match_id], doc[start:end].text)

"""
--- Localizar nomes de países no texto ---

Muitas vezes é mais eficiente fazer a correspondência exata dos textos ao invés de escrever expressões descrevendo
os tokens individualmente. Esse é o caso de categorias finitas, como por exemplo, lista dos países do mundo.
Nós já temos uma lista de países, então vamos usá-la como base para o nosso roteiro. A lista com os nomes está
disponível na variável COUNTRIES.
"""
print("\n5")

with open(
    f"{os.path.join(os.getcwd(), 'capitulo_2', 'countries.json')}", encoding="utf-8"
) as file:
    COUNTRIES = json.loads(file.read())

with open(
    f"{os.path.join(os.getcwd(), 'capitulo_2', 'paises.txt')}", encoding="utf-8"
) as file:
    TEXT = file.read()

doc = nlp("A República Tcheca deve ajudar a Eslováquia a proteger seu espaço aéreo.")

matcher = PhraseMatcher(nlp.vocab)

patterns = list(nlp.pipe(COUNTRIES))
matcher.add("COUNTRY", patterns)

matches = matcher(doc)
print(f"Correspondências: {[doc[start:end] for match_id, start, end in matches]}")

print("\n6")
"""
Vamos usar esse comparador em um texto maior, fazer análise sintática e atualizar as entidades do documento com os
países encontrados.
"""

# Criar um doc e reiniciar (zerar) as entidades existentes
doc = nlp(TEXT)
doc.ents = []

# Iterar nos resultados do combinador
for match_id, start, end in matcher(doc):
    # Criar uma partição Span com o marcador para "GPE"
    span = Span(doc, start, end, label="GPE")

    # Atualizar doc.ents com essa partição
    doc.ents = list(doc.ents) + [span]

    # Identificar o token inicial da partição
    span_root_head = span.root.head

    # Imprimir o texto to token inicial da partição e texto da partição
    print(span_root_head.text, "-->", span.text)

# Imprimir as entidades do documento
print([(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "GPE"])
