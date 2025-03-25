"""
No centro do spaCy está o objeto que contém o pipeline de processamento. Normalmente,
chamamos essa variável de “nlp”.
Por exemplo, para criar um objeto nlp em português, você pode importar o spacy e usar o método
spacy.blank para criar um pipeline em português em branco. Você pode usar o objeto nlp como
uma função para analisar o texto.
Ele contém todos os diferentes componentes do pipeline.
Ele também inclui regras específicas do idioma usadas para tokenizar o texto em palavras e
pontuação. O spaCy oferece suporte a uma variedade de idiomas.
"""

# Objeto nlp
import spacy

# python -m spacy download pt_core_news_sm
# para instalar o pacote com o idioma em português

nlp = spacy.load("pt_core_news_sm")

"""
Quando você processa um texto com o objeto nlp, o spaCy cria um objeto Doc - abreviação de 
“document” (documento). O Doc permite que você acesse informações sobre o texto de forma 
estruturada e nenhuma informação é perdida. A propósito, o Doc se comporta como uma sequência 
Python normal e permite que você itere sobre seus tokens ou obtenha um token pelo seu índice. 
"""

# Objeto Doc
doc = nlp(
    "Há livros escritos para evitar espaços vazios na estante. Carlos Drummond de Andrade"
)

print("\n1")
print(type(doc))
# Saída:
""" <class 'spacy.tokens.doc.Doc'> """

print("\n2")
for token in doc:
    print(token.text, end=" ")

# Saída:
"""
Há livros escritos para evitar espaços vazios na estante. Carlos Drummond de Andrade
"""

"""
---- TOKEN ----
Os objetos token representam os tokens em um documento, por exemplo, uma palavra ou um 
caractere de pontuação. Para obter um token em uma posição específica, você pode indexar o 
documento. Os objetos token também fornecem vários atributos que permitem acessar mais 
informações sobre os tokens. Por exemplo, o atributo .text retorna o texto literal do token.
"""

# Objeto Token

token_1 = doc[1]
print("\n3")
print(token_1.text)

# Saída:
""" livros """

"""
---- SPAN ----
Um objeto Span é uma fatia do documento que consiste em um ou mais tokens. 
Ele é apenas uma visualização do documento e não contém nenhum dado em si.
Para criar uma extensão, você pode usar a notação de fatia do Python. 
Por exemplo, 1:3 criará uma fatia a partir do token na posição 1, 
até - mas não incluindo! - o token na posição 3.
"""

# Objeto span
span = doc[1:3]
print("\n4")
print(span.text)

# Saída:
""" livros escritos """

"""
---- ATRIBUTOS (CARACTERÍSTICAS) LEXICAIS ----
Aqui você pode ver alguns dos atributos de token disponíveis:
-- i -- é o índice do token no documento pai.
-- text -- retorna o texto do token.
-- is_alpha --, -- is_punct -- e -- like_num -- retornam valores booleanos que indicam se o 
token consiste em caracteres alfabéticos, se é pontuação ou se é semelhante a um número. 
Por exemplo, um token “10” - um, zero - ou a palavra “dez” - D, E, Z.
Esses atributos também são chamados de atributos lexicais: eles se referem à entrada no 
vocabulário e não dependem do contexto do token.
"""

doc = nlp("O preço médio da picanha em 2024 foi de R$ 71,00")

print("\n5")
print(f"Índice: {[token.i for token in doc]}")
print(f"Text: {[token.text for token in doc]}")
print(f"is_alpha: {[token.is_alpha for token in doc]}")
print(f"is_punct: {[token.is_punct for token in doc]}")
print(f"like_num: {[token.like_num for token in doc]}")

# Saída:

"""
Índice: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Text: ['O', 'preço', 'médio', 'da', 'picanha', 'em', '2024', 'foi', 'de', 'R$', '71,00']
is_alpha: [True, True, True, True, True, True, False, True, True, False, False]
is_punct: [False, False, False, False, False, False, False, False, False, False, False]
like_num: [False, False, False, False, False, False, True, False, False, False, True
"""

# Processamento do texto
doc = nlp(
    "Em 1990, mais de 60% da população da Ásia Oriental estava em situação de extrema pobreza."
    "Agora, menos de 4% está nessa situação."
)

# Iterar os tokens de um documento doc
for token in doc:
    # Checar se o token é composto por algarismos numéricos
    if token.like_num:
        # Selecionar o próximo token do documento
        next_token = doc[token.i + 1]
        # Checar se o texto do próximo token é igual a "%"
        if next_token.text == "%":
            print(f"Percentuais encontrados: {token.text}")

# Saída:
"""
Percentuais encontrados: 60
Percentuais encontrados: 4
"""
