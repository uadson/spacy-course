"""
Extensões de atributos

Atributos personalizados permitem que você adicione metadados aos documentos, partições ou tokens.
Os dados podem ser adicionados uma vez ou calculados dinamicamente.

Atributos personalizados ficam disponíveis através da propriedade ._ (ponto sublinhado).
Isso deixa claro que foram adicionados pelo usuário e não são padrão da spaCy, como por exemplo token.text.

Esses atributos devem ser registrados nas classes globais Doc, Token e Span, que podem ser importadas de spacy.tokens.
Você já trabalhou com essas classes nos capítulos anteriores.
Para registrar um atributo personalizado no Doc, Token e Span você deve usar o método set_extension.

O primeiro parâmetro é o nome do atributo.
Parâmetros nomeados permitem que você defina como o valores serão computados.
Neste caso, ele tem um valor padrão que pode ser posteriormente alterado.

Definindo atributos personalizados
    Adicionam metadados personalizados a documentos, partições e tokens
    Accessíveis através da propriedade ._

doc._.title = "My document"
token._.is_color = True
span._.has_color = False

São registrados na classe global Doc, Token ou Span através do método set_extension

# Importar classes globais
from spacy.tokens import Doc, Token, Span

# Definir extensões para os objetos Doc, Token e Span
Doc.set_extension("title", default=None)
Token.set_extension("is_color", default=False)
Span.set_extension("has_color", default=False)

Existem três tipos de extensões:
    extensões de atributos, extensões de propriedades, extensões de métodos.


Extensões de atributos:

Extensões de atributos definem um valor que pode ser alterado posteriormente.
Por exemplo, a extensão de atributo is_color que tem o valor padrão como False.
Em tokens individuais, o valor pode ser alterado sobrescrevendo o valor.
Neste caso será "True" para o token "blue".

from spacy.tokens import Token

# define a extensão do token com valor padrão
Token.set_extension("is_color", default=False)

doc = nlp("The sky is blue.")

# Sobrescreve o valor do atributo extendido
doc[3]._.is_color = True


Extensões de propriedades:

Extensões de propriedades são similares às propriedades em Python:
    elas definem uma função getter e uma função setter opcional.

A função getter só é utilizada quando você recupera os valores de um atributo.
Isso permite calcular o valor dinamicamente e até levar em conta valores de outros atributos.

Funções getter recebem apenas um parâmetro:
    o objeto, neste caso, o token. Neste exemplo, a função retorna se o texto do token está na lista de cores.

Quando registramos uma extensão, definimos a função getter através do parâmetro nomeado getter.

O token "blue" agora retorna True para a propriedade extendida ._.is_color.

    Definem funções opcionais "getter" e "setter"
    A função "getter" só pode ser usada quando você for recuperar o valor do atributo

from spacy.tokens import Token

# Definir uma função getter
def get_is_color(token):
    colors = ["red", "yellow", "blue"]
    return token.text in colors

# Define uma extensão ao token com a função getter
Token.set_extension("is_color", getter=get_is_color)

doc = nlp("The sky is blue.")
print(doc[3]._.is_color, "-", doc[3].text)

Saída:
True - blue

Extensões de propriedades:

Se você quiser definir uma extensão de uma partição, você sempre deve usar a extensão de propriedade com uma
função getter. Se não fizer assim, você terá que atualizar toda e qualquer partição manualmente para definir todos
seus valores.

Neste exemplo, a função get_has_color recebe a partição e retorna se o texto ou algum token do texto está na lista
de cores.

Após processarmos o documento, podemos checar diferentes partições do texto e inspecionar a propriedade ._.has_color,
que indicará se a partição contém um token das cores selecionadas ou não.


from spacy.tokens import Span

# Definir a função getter
def get_has_color(span):
    colors = ["red", "yellow", "blue"]
    return any(token.text in colors for token in span)

# Definir a extensão com o parametro getter sendo a função definida
Span.set_extension("has_color", getter=get_has_color)

doc = nlp("The sky is blue.")
print(doc[1:4]._.has_color, "-", doc[1:4].text)
print(doc[0:2]._.has_color, "-", doc[0:2].text)

Saída:
True - sky is blue
False - The sky


Extensões de métodos:

Extensões de métodos permitem que um atributo se torne um método que pode ser invocado.
Você pode passar um ou mais parâmetros para o método extendido, e calcular valores de atributos dinamicamente.
Por exemplo, baseado em algum argumento ou configuração.
Neste exemplo, a função verifica se o documento contém um token com um dado texto.
O primeiro parâmetro do método é sempre o objeto em si, neste caso, o documento.
Ele é passado automaticamente quando o método é chamado.
Todos os outros parâmetros serão passados à função extendida, neste caso, token_text.
Aqui o método extendido ._.has_token retornará True para a palavra "blue" e False para a palavra "cloud".

from spacy.tokens import Doc

# Definir método com seus parâmetros
def has_token(doc, token_text):
    in_doc = token_text in [token.text for token in doc]
    return in_doc

# Definir a extensão do documento com o parâmetro nomeado method
Doc.set_extension("has_token", method=has_token)

doc = nlp("The sky is blue.")
print(doc._.has_token("blue"), "- blue")
print(doc._.has_token("cloud"), "- cloud")

True - blue
False - cloud
"""

# Exemplos
print("\n1")
# Definindo extensões de propriedades
import spacy
import json
import os
from spacy.tokens import Token, Doc, Span
from spacy.language import Language
from spacy.matcher import PhraseMatcher


nlp = spacy.load("pt_core_news_sm")

# Definir o atributo "is_country" com o valor padrão como falso (False)
Token.set_extension("is_country", default=False)

# Processar o texto e atribuir o atributo is_country com valor verdadeiro (True) para o token "Espanha"

doc = nlp("Eu moro na Espanha")
doc[3]._.is_country = True

# Imprimir o texto e o atributo is_country para todos os tokens
print([(token.text, token._.is_country) for token in doc])
"""
Saída:
[('Eu', False), ('moro', False), ('na', False), ('Espanha', True)]
"""

print("\n2")


# Definir a função que recebe um token e retorna seu conteúdo invertido
def get_reversed(token):
    return token.text[::-1]


# Registrar o atributo extendido "reversed" com o argumento getter sendo a função get_reversed
Token.set_extension("reversed", getter=get_reversed)

# Processar o texto e imprimir o atributo "reversed" para cada token
doc = nlp("Todas as generalizações são falsas, incluindo esta.")
for token in doc:
    print("reversed: ", token._.reversed)
"""
Saída:
reversed:  sadoT
reversed:  sa
reversed:  seõçazilareneg
reversed:  oãs
reversed:  saslaf
reversed:  ,
reversed:  odniulcni
reversed:  atse
reversed:  .
"""

print("\n3")
# Definir propriedades mais complexas usando o argumento getter e a extensão de métodos.


# Definir a função para o atributo getter
def get_has_number(doc):
    # Retornar verdadeiro (True) se algum token do doc for número (token.like_num)
    return any(token.like_num for token in doc)


# Definir a propriedade extendida "has_number" com o getter sendo get_has_number
Doc.set_extension("has_number", getter=get_has_number)

# Processar o texto e verificar a propriedade has_number
doc = nlp("O museu esteve fechado por cinco anos em 2012.")
print("has_number:", doc._.has_number)
"""
Saída:
has_number: True
"""

print("\n4")


# Definir a função
def to_html(span, tag):
    # Envolva o texto com uma tag HTML e retorne como resultado
    return f"<{tag}>{span.text}</{tag}>"


# Definir o método extendido para a partição (Span) "to_html" com a função to_html
Span.set_extension("to_html", method=to_html)

# Processar o texto e chamar o método to_html para a partição span passando o argumento "strong"
doc = nlp("Olá mundo, essa é uma frase.")
span = doc[0:2]
print(span._.to_html("strong"))
"""
Saída:
<strong>Olá mundo</strong>
"""

print("\n5")
"""
Combinará propriedades personalizadas com as previsões estatísticas e criará um método extendido que retornará o 
endereço (URL) de busca na Wikipedia se a partição for uma pessoa, organização ou localidade.
"""


def get_wikipedia_url(span):
    # Gerar uma URL da Wikipedia se o texto tiver algum dos rótulos PERSON, ORG, GPE, LOCATION, PER
    if span.label_ in ("PERSON", "ORG", "GPE", "LOCATION", "PER"):
        entity_text = span.text.replace(" ", "_")
        return "https://en.wikipedia.org/w/index.php?search=" + entity_text


# Definir a propriedade extendida wikipedia_url usando o atributo getter com get_wikipedia_url
Span.set_extension("wikipedia_url", getter=get_wikipedia_url)

doc = nlp(
    "Ao longo de cinquenta anos, desde o lançamento de suas primeira músicas até o último album, "
    " David Bowie sempre esteve na vanguarda da cultura contemporânea."
)
for ent in doc.ents:
    # Imprimir a entidade e URL da Wikipedia URL para a entidade
    print(ent.text, ent._.wikipedia_url)

"""
Saída:
David Bowie https://en.wikipedia.org/w/index.php?search=David_Bowie
"""

print("\n6")
"""
Propriedades extendidas podem ser poderosas quando combinadas com componentes personalizados do fluxo (pipeline) de 
processamento.

Criação de um componente do fluxo de processamento para identificar nomes de países e definirá uma propriedade que 
retornará a capital do país, se houver.

Um Comparador com todos os países deverá ser disponibilizado na variável matcher. 
Um dicionário que mapeie os países e suas capitais deverá ser disponibilizado na variável CAPITALS.
"""

countries_file_path = os.path.join(os.getcwd(), "countries.json")
capitals_file_path = os.path.join(os.getcwd(), "capitals.json")

with open(countries_file_path, encoding="utf-8") as file:
    COUNTRIES = json.loads(file.read())

with open(capitals_file_path, encoding="utf-8") as file:
    CAPITALS = json.loads(file.read())

nlp = spacy.load("pt_core_news_md")
matcher = PhraseMatcher(nlp.vocab)
matcher.add("COUNTRY", list(nlp.pipe(COUNTRIES)))


@Language.component("countries_components")
def countries_components_function(doc):
    # Criar uma partição com o rótulo "GPE" para todas os correspondências
    matches = matcher(doc)
    doc.ents = [Span(doc, start, end, label="GPE") for match_id, start, end in matches]
    return doc


# Adicionar o componente ao fluxo de processamento (pipeline)
nlp.add_pipe("countries_components")
print(nlp.pipe_names)
"""
Saída:
['tok2vec', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler', 'ner', 'countries_components']
"""

# Criar uma função getter que compara o texto com um dicionário com países e suas capitais
get_capital = lambda span: CAPITALS.get(span.text)

# Definir a propriedade extendida "capital" com o atributo getter get_capital
Span.set_extension("capital", getter=get_capital)

# Processar o texto e imprimir o texto da entidade, rótulo (label) e a propriedade extendida capital
doc = nlp("A República Tcheca pode ajudar a Eslováquia a proteger seu espaço aéreo.")
print([(ent.text, ent.label_, ent._.capital) for ent in doc.ents])
"""
Saída:
[('República Tcheca', 'GPE', None), ('Eslováquia', 'GPE', None)]
"""
