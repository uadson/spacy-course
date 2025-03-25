"""
Vocabulário compartilhado e armazenamento de strings

    - Vocab: armazena informações compartilhadas entre diversos documentos
    - Para economizar memória, a spaCy mapeia as strings em códigos hash
    - Strings são armazenadas apenas uma vez na StringStore via nlp.vocab.strings
    - Armazenamento de Strings: tabelas de consultas que funcionam em ambos sentidos

nlp.vocab.strings.add("coffee")
coffee_hash = nlp.vocab.strings["coffee"]
coffee_string = nlp.vocab.strings[coffee_hash]

    - Códigos hash não podem ser revertidos - por isso é preciso sempre prover o vocabulário compartilhado

# Gera um erro se a string não foi mapeada anteriomente
string = nlp.vocab.strings[3197928453018144401]

A spaCy armazena todos os dados compartilhados em um vocabulário: o Vocab.
Ele inclui palavras e também esquemas para marcadores e entidades.
Para economizar memória, todas as strings são mapedas em códigos hash. Se uma palavra ocorre mais de uma vez,
só é necessário salvá-la uma vez.
A spaCy usa uma função hash para gerar um identificador (ID) e armazena a string apenas uma vez. As strings armazenadas
estão disponíveis em nlp.vocab.strings.
Trata-se de uma tabela de consulta que pode ser utilizada nos dois sentidos. Você pode pesquisar uma string e obter o
seu código hash, ou pode pesquisar um código hash e obter a string correspondente. Internamente, a spaCy só lida com
códigos hash.

Mas os códigos hash não podem ser revertidos diretamente. Isso quer dizer que se uma palavra não estiver registrada no
vocabulário, não será possível obter sua string. Por isso é sempre necessário fazer o registro no vocabulário
compartilhado.

Para obter o código hash de uma string, podemos fazer a consulta em nlp.vocab.strings.
Para obter a string que representa um código hash, fazemos a consulta com o hash.
O objeto Doc também expõe o vocabulário compartilhados e suas strings e códigos hash.
"""

import spacy

print("\n1")
nlp = spacy.load("pt_core_news_sm")
doc = nlp("Eu gosto de café")
hash_id = nlp.vocab.strings["café"]
print(f"Valor de hash: {hash_id}")
print(f"Valor da string: {nlp.vocab.strings[hash_id]}")

print("\n2")
"""
Lexemas: entradas do vocabulário

Lexemas são entradas do vocabulário que independem do contexto.
Você obtém um lexema a partir da consulta de uma string ou código hash no vocabulário.
Lexemas possuem atributos, assim como os tokens.
Eles armazenam informações de uma palavra que são independentes de contexto: texto, se a 
palavra é composta por apenas caracteres alfabéticos, etc.
Lexemas não armazenam marcadores de classe gramatical, termo sintático ou entidade. 
Estes dependem do contexto no qual a palavra está inserida.
"""
lexeme = nlp.vocab["café"]
print(lexeme.text, lexeme.orth, lexeme.is_alpha)
"""
Contém as informações de cada palavra independente de contexto :

    Texto da palavra: lexeme.text e lexeme.orth (o código hash)
    Atributos léxicos, como por exemplo lexeme.is_alpha
    Não incluem marcadores que dependem do contexto, como classe gramatical, termo sintático ou entidade.
"""
print("\n3")
"""
Vocabulários, Strings e Hashes
"""

# Consultando strings e hashes

doc = nlp("Eu tenho um gato amarelo")
gato_hash = nlp.vocab.strings["gato"]
print(f"Hash: {gato_hash}")

gato_string = nlp.vocab.strings[gato_hash]
print(f"String: {gato_string}\n")

print("\n4")
# Consultar o marcador PERSON para obter o código hash
doc = nlp("David Bowie é uma PESSOA")

# Consultar o código hash para a string PESSOA
person_hash = nlp.vocab.strings["PESSOA"]
print(f"Hash para PESSOA: {person_hash}")

# Consultar o person_hash para obter o texto novamente
person_string = nlp.vocab.strings[person_hash]
print(f"Texto do hash: {person_string}")

"""
Doc, partição Span e Token

O objeto Doc é uma das estruturas de dados centrais da spaCy. Ele é criado automaticamente 
quando você processa um texto com o objeto nlp. Mas você também pode instanciar o objeto 
manualmente.
Após criar o objeto nlp, podemos importar a classe Doc a partir de spacy.tokens.
Aqui estamos criando um doc a partir de três palavras. 
Os espaços em branco são representados por uma lista de valores boleanos que indicam 
se a palavra é seguida por um espaço em branco ou não. 
Todos os tokens incluem essa informação, inclusive o último!
O objeto Doc tem três parâmetros: 
    o vocabulário compartilhado, as palavras e os espaços em branco.
"""
print("\n5")

import spacy

nlp = spacy.blank("pt")

# Importando a class Doc
from spacy.tokens import Doc

# As palavras e espaços em branco necessários para criar um doc:
words = ["Olá", "mundo", "!"]
spaces = [True, False, False]

# Criar um doc manualmente
doc = Doc(nlp.vocab, words=words, spaces=spaces)

"""
O objeto partição Span

Um objeto Span é uma partição do documento consistindo de um ou mais tokens. 
Ele necessita de pelo menos três parâmetros: o doc ao qual a partição se refere, 
os índices do início e do fim da partição. Lembre-se que o índice final não é incluído 
na partição!

Também é possível criar uma partição Span manualmente a partir da importação da classe 
spacy.tokens. 
Em seguida, deve-se instanciar o objeto com o doc e os índices de início e 
fim da partição, e opcionalmente um marcador.

O atributo doc.ents pode ser atualizado, sendo possível adicionar manualmente novas 
entidades a partir de uma lista de partições.
"""

from spacy.tokens import Doc, Span

# As palavras e espaços em branco necessários para criar o doc
words = ["Olá", "mundo", "!"]
spaces = [True, False, False]

# Criar um doc manualmente
doc = Doc(nlp.vocab, words=words, spaces=spaces)

# Criar uma partição span manualmente
span = Span(doc, 0, 2)

# Criar uma partição span com um marcador
span_with_label = Span(doc, 0, 2, label="SAUDACAO")

# Adicionar a partição a doc.ents
doc.ents = [span_with_label]

"""
Melhores práticas
    Doc e Span são recursos bastante poderosos e armazenam referências e relações entre 
    palavras e sentenças:
        Converta os resultados para strings o mais tarde possível
        Use os atributos dos tokens, se estiverem disponíveis. – por exemplo: token.i para 
        o índice do token
    Não se esqueça de passar o parâmetro do vocabulário compartilhado vocab
    
Algumas dicas e segredos antes de começar:

Os objetos Doc e Span são bastante poderosos e e foram otimizados para melhor performance. 
Eles te dão acesso a todas as referências e relações entre as palavras e as sentenças.

Se sua aplicação necessita de saídas em texto (strings), faça as conversões para texto o 
mais tarde possível. 
Se você fizer isso muito cedo, você corre o risco de perder todas as relações entre os 
tokens.

Para que seu projeto seja consistente, use os atributos dos tokens já existentes sempre 
que possível.

E também é preciso passar o vocabulário compartilhado como parâmetro, sempre!
"""
import spacy

nlp = spacy.blank("pt")

# Importar as classes Doc e Span
from spacy.tokens import Doc, Span

words = ["Eu", "adoro", "David", "Bowie"]
spaces = [True, True, True, False]

# Criando um doc Doc a partir das palavras words e espaçamento spaces
doc = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc.text)

# Criar uma partição para "David Bowie" a partir do doc e atribua o marcador "PERSON"
span = Span(doc, 2, 4, label="PERSON")
print(span.text, span.label_)

# Adicionar a partição às entidades do doc.
doc.ents = [span]

# Imprimir o texto e os marcadores das entidades
print([(ent.text, ent.label_) for ent in doc.ents])

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Berlin looks like a nice city")

# Este código não é eficiente
# Iterar nos tokens
token_texts = [token.text for token in doc]
pos_tags = [token.pos_ for token in doc]

for index, pos in enumerate(pos_tags):
    # Verifica se o token atual é um substantivo próprio.
    if pos == "PROPN":
        # Verifica se o próximo token é um verbo
        if pos_tags[index + 1] == "VERB":
            result = token_texts[index]
            print("Found proper noun before a verb:", result)

# Este código é eficiente
import spacy

nlp = spacy.load("pt_core_news_sm")
doc = nlp("Berlin parece ser uma cidade bonita.")

# Iterar nos tokens
for token in doc:
    # Verifica se o token atual é um substantivo próprio.
    if token.pos_ == "PROPN":
        # Verifica se o próximo token é um verbo
        if doc[token.i + 1].pos_ == "VERB":
            print(f"Encontrado nome próprio antes de um verbo: {token.text}")
