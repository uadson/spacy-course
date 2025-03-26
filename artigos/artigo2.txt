"""
---- FLUXOS (PIPELINES) DE PROCESSAMENTO TREINADOS ----
Agora vamos adicionar alguns poderes especiais ao objeto nlp
"""

"""
O que são fluxos (pipelines) de processamento treinados ?

    Modelos que permitem que a spaCy faça previsões de atributos linguísticos em contexto:
        - Marcadores de classes gramaticais
        - Dependências sintáticas
        - Entidades nomeadas
    São treinados com exemplos de textos rotulados.
    Podem ser atualizados com mais exemplos para um ajuste fino das previsões.
    
Algumas das análises mais interessantes são aquelas específicas a um contexto. 
Por exemplo: se uma palavra é um verbo ou se uma palavra é o nome de uma pessoa.

Os fluxos (pipelines) de processamento possuem modelos estatísticos que permitem que a spaCy faça previsões dentro de um
contexto. Isso normalmente inclui marcadores de classes gramaticais, dependências sintáticas e entidades nomeadas.

Os fluxos (pipelines) de processamento são treinados em grandes conjuntos de dados com textos de exemplos já rotulados.
Os modelos podem ser atualizados com mais exemplos para fazer um ajuste fino nas previsões, como por exemplo, melhorar 
os resultados em um conjunto de dados específico.
"""

"""
Pacotes dos fluxos (pipelines) de processamento

A biblioteca spaCy oferece vários pacotes de fluxos (pipelines) de processamento que você pode baixar usando o comando 
spacy download. 
Por exemplo, o pacote "en_core_web_sm" é um fluxo de processamento pequeno em inglês que foi treinado com texto da 
internet e possui diversos recursos.

O método spacy.load carrega o pacote de um fluxo (pipeline) de processamento a partir do seu nome e retorna um objeto 
nlp.

O pacote contém os pesos binários que permitem que a spaCy faça as previsões.

Também inclui o vocabulário, metadados com informações sobre o fluxo (pipeline) de processamento e um arquivo de 
configuração utilizado para treiná-lo. 
Ele informa qual o idioma a ser utilizado e como configurar o fluxo de processamento (pipeline).
"""

"""
Vamos dar uma olhada nas previsões do modelo. Neste exemplo, estamos usando a spaCy para prever as classes gramaticais, 
que são os tipos de palavras em seu contexto.
Primeiramente, carregamos o fluxo(pipeline) de processamento pequeno do português no objeto nlp.
Em seguida, processamos o texto: "O Palmeiras não tem mundial".
Para cada token no doc, podemos imprimir o texto e o atributo .pos_, que é a classe gramatical prevista.
Na spaCy, atributos que retornam strings normalmente terminam com um sublinhado (underscore) e atributos sem o 
sublinhado retornam um inteiro.
Neste exemplo, o modelo previu corretamente "Palmeiras" como um nome próprio e "tem" como um verbo.

"""
import spacy

# Carregamento do fluxo (pipeline) de processamento em português
nlp = spacy.load("pt_core_news_md")

# Processar um texto
doc = nlp("O Palmeiras não tem mundial.")

print("\n1")
# Iterar nos tokens
for token in doc:
    # Imprimir o texto e a classe gramatical prevista
    print(token.text, token.pos_)

# Saída:
"""
O DET
Palmeiras PROPN
não ADV
tem VERB
mundial ADJ
. PUNCT
"""

"""
Previsão de termos sintáticos

Em adição à previsão de classes gramaticais, podemos prever como as palavras estão relacionadas. 
Por exemplo, se uma palavra é o sujeito ou o predicado de uma sentença.

O atributo .dep_ retorna o marcador de dependência (ou termo sintático) previsto.
O atributo .head retorna o índice do token principal. Você pode pensar nele como o "pai" ao 
qual a palavra está conectada.
"""

print("\n2")

for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)

"""
Para descrever as dependências sintáticas, a spaCy usa um esquema com marcadores padronizados. 
Esse é um exemplo dos marcadores mais comuns:
O nome próprio (PROPN) "Palmeiras" é um sujeito simples (nsubj) relacionado com um verbo 
(VERB), neste exemplo "tem".
"""
# Saída
"""
O DET det Palmeiras
Palmeiras PROPN nsubj tem
não ADV advmod tem
tem VERB ROOT tem
mundial ADJ obj tem
. PUNCT punct tem
"""

print("\n3")
"""
Previsão de Entidades Nomeadas

Entidades nomeadas são "objetos do mundo real" que possuem um nome. 
Por exemplo: uma pessoa, uma organização ou um país.
A propriedade doc.ents permite o acesso às entidades nomedas identificadas (previstas) pelo modelo de reconhecimento 
de entidades nomeadas
Ela retorna um iterável de objetos do tipo Span, possibilitando o acesso ao texto e ao marcador através do atributo 
.label_.
Neste caso, o modelo previu corretamente "Apple" como uma organização, "Reino Unido" como uma entidade geopolítica.
"""

# Processar um texto
doc = nlp("A Apple está pensando em comprar uma startup do Reino Unido por U$1 bilhão")

# Iterar nas entidades previstas
for ent in doc.ents:
    # Imprimir o texto da entidade e seu marcador
    print(ent.text, ent.label_)

# Saída:
"""
Apple ORG
Reino Unido LOC
"""
print("\n4")
"""
Uma dica: Para obter a definição dos marcadores mais comuns, você pode usar a função auxiliar spacy.explain.
Por exemplo, a sigla "GPE" para entidade geopolítica (geopolitical entity) não é muito intuitiva, mas o comando 
spacy.explain irá lhe explicar que se refere a países, cidades e estados.
O mesmo vale para marcadores de classes gramaticais e termos sintáticos.
"""
print(spacy.explain("PROPN"))
print(spacy.explain("NOUN"))
print(spacy.explain("ADJ"))
print(spacy.explain("DET"))
print(spacy.explain("GPE"))
