# Processamento de Linguagem Natural com spaCy

## O que é Processamento de Linguagem Natural (PLN)?

O Processamento de Linguagem Natural (PLN) é uma área da Inteligência Artificial que permite que máquinas compreendam e processem textos escritos ou falados. Aplicações comuns incluem chatbots, tradução automática e análise de sentimentos.

O spaCy é uma das bibliotecas mais populares para PLN em Python. Ele oferece ferramentas eficientes para análise sintática, extração de entidades e outras tarefas relacionadas ao processamento de texto.

### Primeiros passos com spaCy

Para começar a usar o spaCy, instale-o e baixe um modelo de linguagem em português:

```python
    pip install spacy
    python -m spacy download pt_core_news_sm
```

Em seguida, podemos criar um objeto nlp, que representa o pipeline de processamento do spaCy:

```python
    import spacy

    nlp = spacy.load("pt_core_news_sm")
    doc = nlp("O céu está azul e bonito hoje.")
```

### Estruturas fundamentais: Doc, Token e Span

O spaCy transforma o texto em três principais componentes:

- Doc: Representa o texto inteiro processado.
- Token: Cada palavra ou pontuação do texto.
- Span: Um trecho do texto composto por múltiplos tokens.

Exemplo:

```python
    for token in doc:
        print(token.text)
```

Saída:

```bash
O

céu

está

azul

e

bonito

hoje
```

### Criando uma parte do texto (Span):

```python
    span = doc[1:3]
    print(span.text)
```

Saída:

```bash
céu está
```

### Atributos dos Tokens

Cada token contém diversas informações, como:

- token.is_alpha: verifica se o token contém apenas letras.
- token.is_punct: verifica se o token é pontuação.
- token.like_num: identifica números escritos por extenso ou em algarismos.

Exemplo:

```python
doc = nlp("Em 2024, o preço médio do café foi de R$ 10,00.")

for token in doc:
    print(token.text, token.is_alpha, token.is_punct, token.like_num)
```

Saída:

```baseh
Em True False False

2024 False False True

, False True False

o True False False

preço True False False

médio True False False

do True False False

café True False False

foi True False False

de True False False

R$ False False False

10,00 False False True

. False True False
```
