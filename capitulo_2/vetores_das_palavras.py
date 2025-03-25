"""
Comparando similiraridades semânticas

    A biblioteca spaCy pode comparar dois objetos e prever a sua similaridade.
    Doc.similarity(), Span.similarity() e Token.similarity()
    Recebem outro objeto e retornam um score de similaridade ( entre 0 e 1 )
    Importante: é necessário incluir um fluxo (pipeline) de processamento que tenha vetores de palavras incluso,
    como por exemplo:
        ✅ en_core_web_md ou pt_core_news_md ( tamanho médio )
        ✅ en_core_web_lg ou pt_core_news_lg ( tamanho grande )
        🚫 NÃO USE en_core_web_sm ou pt_core_news_sm ( tamanho pequeno )

A spaCy consegue comparar dois objetos e prever o quão similares eles são entre si. Os objetos podem ser documentos,
partições ou tokens.
Os objetos Doc, Token e Span possuem o método .similarity que recebe outro objeto e retorna um número de ponto flutuante
entre 0 e 1 indicando o quão similares estes objetos são entre si.

Um detalhe importante: para poder usar a similaridade, você necessita usar um fluxo (pipeline) de processamento maior
que inclua a representação das palavras em vetores (word vectors).
Você pode usar o fluxo (pipeline) de processamento médio ou grande da língua inglesa, mas não o modelo pequeno.
Se você desejar usar os vetores, sempre use um fluxo (pipeline) de processamento que termine com os caracteres
"md" ou "lg". Para mais detalhes, visite a documentação dos modelos.
"""

"""
Exemplos de similaridades

Aqui está um exemplo: vamos supor que você deseja saber se dois documentos são similares.
Inicialmente carregamos o modelo médio da língua portuguesa : "pt_core_news_md".
Em seguida podemos criar dois objetos o usar o método similarity do primeiro documento, comparando com o segundo.
Neste caso, encontramos uma similaridade razoavelmente alta entre "Eu gosto de comida rápida" e "Eu gosto de pizza".
O mesmo pode ser feito para tokens.
De acordo com os vetores de palavras, os tokens "pizza" e "torta" são relativamente similares e receberam um score de 
0.61.
"""

print("\n1")
import spacy

# Carregar o fluxo (pipeline) de processamento maior com os vetores
nlp = spacy.load("pt_core_news_md")

# Comparar dois documentos
doc1 = nlp("Eu gosto de comida rápida")
doc2 = nlp("Eu gosto de pizza")
print(f"Similaridade entre os dois documentos: {doc1.similarity(doc2):.2f}")

# Comparar dois tokens
doc = nlp("Eu gosto de pizza e torta.")
token1 = doc[3]  # pizza
token2 = doc[5]  # massa
print(f"\nSimilaridade entre os dois tokens: {token1.similarity(token2):.2f}")

print("\n2")
"""
Inspeção dos vetores das palavras
"""
# Processamento de um texto
doc = nlp("Python é uma linguagem de programação")

# Imprimindo o vetor para "linguagem"
linguagem_vector = doc[3].vector
print(f"Vetor para a palavra linguagem: {linguagem_vector}")
print(f"Tamanho do vetor para a palavra linguagem: {len(linguagem_vector)}")

print("\n3")
"""
Comparando similaridades
"""
## Entre dois documentos
doc1 = nlp("Eu quero comprar um livro novo")
doc2 = nlp("Preciso ler um livro")

# Obtendo a similaridade entre doc1 e doc2
similarity = doc1.similarity(doc2)
print(f"Similaridade entre dois documentos: {similarity:.2f}%")

print("\n4")
## Entre dois tokens
doc = nlp("Televisão e livro")
token1, token2 = doc[0], doc[2]

# Obtendo a similaridade entre "Televisão" e "livro"
similarity = token1.similarity(token2)
print(f"Obtendo a similaridade entre tokens: {similarity:.2f}%")

print("\n5")
# Obtendo similaridades entre partições (Span)
doc = nlp("Visitamos um excelente restaurante. Em seguida fomos a um ótimo bar.")

# Criando partições para "excelente restaurante" e "ótimo bar"
span1 = doc[2:4]
span2 = doc[10:12]
print(f"Span 1: {span1}")
print(f"Span 2: {span2}")

# Obtendo a similaridade entre as duas partições
similarity = span1.similarity(span2)
print(f"Similaridade entre as duas partições: {similarity:.2f}%")
