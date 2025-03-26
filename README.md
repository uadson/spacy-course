# Explorando o Processamento de Linguagem Natural (NLP) com spaCy 🚀

O Processamento de Linguagem Natural (NLP) é uma das áreas mais fascinantes da Inteligência Artificial, permitindo que
máquinas compreendam, interpretem e gerem texto de maneira semelhante aos humanos. Uma das bibliotecas mais poderosas
para NLP em Python é o spaCy. Vamos dar uma olhada nos conceitos básicos para quem está começando! 👇

### 🔹 Criando um Pipeline de NLP

O spaCy trabalha com pipelines de processamento, que são sequências de operações para transformar texto bruto em
informação estruturada. O primeiro passo é criar um objeto nlp, que atua como o "cérebro" do processamento:

```python
import spacy
# Criando um pipeline vazio para português
nlp = spacy.blank("pt")
```

### 🔹 Trabalhando com Documentos (Doc)

Ao processar um texto com nlp, criamos um objeto Doc, que representa o texto de forma estruturada. Isso significa que
podemos acessar palavras (tokens), pontuações e outras informações de maneira organizada:

```python
doc = nlp("O conhecimento é a única riqueza que ninguém pode tirar de você.")
# Iterando sobre os tokens do documento
for token in doc:
	print(token.text)

```

✅ Saída:

```bash
O conhecimento é a única riqueza que ninguém pode tirar de você .
```

### 🔹 Tokens: As Unidades de Texto

Cada palavra (ou símbolo) em um texto é chamada de token. Podemos acessar tokens diretamente pelo índice:

```python
token_1 = doc[1]
print(token_1.text)  # Saída: conhecimento
```

### 🔹 Extraindo Partes do Texto (Span)

Se quisermos obter uma parte do texto, podemos usar um Span, que representa uma sequência contínua de tokens:

```python
span = doc[1:4]  # Pegando tokens da posição 1 até a 3
print(span.text)  # Saída: conhecimento é a
```

### 🔹 Identificando Tipos de Palavras

Com o spaCy, podemos analisar se um token é uma palavra, um número ou pontuação. Vamos testar com um exemplo:

```python
doc = nlp("Em 2024, o preço médio da gasolina foi de R$ 6,50.")

print(f"Tokens: {[token.text for token in doc]}")
print(f"É número? {[token.like_num for token in doc]}")
```

✅ Saída:

```bash
Tokens: ['Em', '2024', ',', 'o', 'preço', 'médio', 'da', 'gasolina', 'foi', 'de', 'R$', '6,50', '.']
É número? [False, True, False, False, False, False, False, False, False, False, False, True, False]
```

Perceba que 2024 e 6,50 foram reconhecidos como números! Isso pode ser útil para extrair datas, valores e percentuais
de um texto.

### 🔹 Encontrando Percentuais no Texto 📊

Que tal detectar automaticamente percentuais mencionados em um texto?

```python
doc = nlp("Em 1990, mais de 60% da população vivia na pobreza. Agora, menos de 4%.")

for token in doc:
	if token.like_num:  # Se for um número
    	next_token = doc[token.i + 1]  # Pegamos o próximo token
    	if next_token.text == "%":
        	print(f"Percentual encontrado: {token.text}%")
```

✅ Saída:

```bash
Percentual encontrado: 60%
Percentual encontrado: 4%
```
