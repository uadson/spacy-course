"""
Personalizando os componentes de um fluxo (pipeline)

Componentes personalizados permitem que você adicione uma função feita por você ao fluxo de processamento (pipeline),
que é executado quando você chama nlp em um texto. Por exemplo: você pode modificar o documento e adicionar mais dados
a ele.

Após o texto ser toquenizado e o objeto ser criado, os componentes do fluxo de processamento (pipeline) são aplicados
sequencialmente.

A biblioteca spaCy suporta uma grande variedade de componentes pré-existentes, mas também permite que você crie seu
próprio componente.

Componentes personalizados são executados automaticamente quando você chamar o objeto Doc em um texto.
Eles são especialmente úteis para você adicionar metadados personalizados aos documentos e tokens.
Você também pode usá-los para atualizar os atributos já existentes, como as partições com entidades nomeadas.

Por que personalizar componentes ?

    Permite que uma função seja executada automaticamente quando você chamar nlp
    Adiciona metadados personalizados ao documentos e aos tokens
    Atualiza atributos padrão como por exemplo entidades doc.ents

Fundamentalmente, o componente de um fluxo de processamento é uma função ou um objeto que recebe um documento,
o modifica e em seguida retorna este objeto, que pode ser processado em seguida pelo próximo componente do fluxo de
processamento.

Para informar à biblioteca spaCy a localização do seu componente customizado e como ele deve ser utilizado,
você pode adicionar o decorador @Language.component.

Adicione o decorador na linha anterior à definição da função.
Uma vez que o componente estiver registrado, ele pode ser adicionado ao fluxo de processamento através do método
nlp.add_pipe.

O método recebe pelo menos um parâmetro: a string com o nome do componente.

Anatomia de um componente

    Função que recebe um doc, o modifica, e em seguida o retorna
    Registrado através do decorador Language.component
    Pode ser adicionado ao fluxo de processamento através do método nlp.add_pipe

                    import spacy
                    from spacy.language import Language

                    nlp = spacy.load("pt_core_news_sm")


                    @Language.component("custom_component")
                    def custom_component(doc):
                        # Faz alguma coisa com o documento
                        return doc

                    nlp.add_pipe("custom_component")


Para definir onde o componente será adicionado ao fluxo de processamento, você pode usar os seguintes argumentos:

Definir last como True irá adicionar o componente ao final do fluxo de processamento. Esse é o comportamento padrão.
Definir first como True irá adicionar o componente ao início do fluxo de processamento, logo após o toquenizador.
Os argumentos before e after permitem definir o nome de um componente existente de tal forma que o novo componente
seja adicionado antes ou depois dele.

    Por exemplo: before="ner" irá adicionar o novo componente antes do identificador de entidados nomeadas.

O componente existente ao qual o novo componente deve ser adicionado antes ou depois precisa existir,
senão a spaCy gerará um erro.

-----------------------------------------------------------------------------------------------------------------------
Parâmetro | Descrição                                                   | Exemplo
-----------------------------------------------------------------------------------------------------------------------
last      | Se True, adicionar no final                                 | nlp.add_pipe("component", last=True)
-----------------------------------------------------------------------------------------------------------------------
first     | Se True, adicionar no início                                | nlp.add_pipe("component", first=True)
-----------------------------------------------------------------------------------------------------------------------
before    | Adicionar antes do componente                               | nlp.add_pipe("component", before="ner")
-----------------------------------------------------------------------------------------------------------------------
after     | Adicionar depois do componente                              | nlp.add_pipe("component", after="tagger")
-----------------------------------------------------------------------------------------------------------------------
"""

print("\n1")
"""
Eis um exemplo de um componente simples do fluxo de processamento:

Começamos com o fluxo de processamento pequeno da língua portuguesa.
Em seguida definimos o componente: 
    uma função que recebe um objeto Doc e o retorna.

Vamos fazer algo simples e imprimir o tamanho do documento recebido.
Não se esqueça de retornar o documento para que ele seja processado pelo próximo componente no fluxo de processamento! 
O documento criado pelo toquenizador é passado para todos os componentes, portanto é essencial retornar o documento 
modificado.

Para poder utilizar o novo componente, nós o registramos utilizando o decorador Language.component e em seduida 
podemos chamá-lo com "custom_component".

Agora podemos adicionar o componente ao fluxo de processamento. 
Vamos adicioná-lo logo no início, antes do toquenizador, definindo o atributo first=True.

Quando imprimimos os nomes dos componentes do fluxo de processamento, o componente personalizado agora aparece no 
início. 
Isso significa que ele será aplicado logo no início do processamento do documento.

"""

# Exemplo: um componente simples
import spacy
from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

# Criar um objeto nlp
nlp = spacy.load("pt_core_news_sm")


# Definir um componente personalizado
@Language.component("custom_component")
def custom_component(doc):
    # Imprimir o tamanho do documento
    print(f"Doc length: {len(doc)}")
    # Retorna o objeto doc
    return doc


# Adicionar o componente como primeiro no fluxo de processamento
nlp.add_pipe("custom_component", first=True)

# Imprimir o nome dos componentes do fluxo de processamento
print(f"Pipeline: {nlp.pipe_names}\n")

"""
Saída:
Pipeline: ['custom_component', 'tok2vec', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler', 'ner']
"""

"""
Agora quando processarmos um texto usando o objeto nlp, o componente customizado será aplicado ao documento e o 
tamanho do documento será impresso.
"""
# Processar o texto
doc = nlp("E tenho dito: o Palmeiras não tem mundial. :)")
print(f"{doc}\n")
"""
Saída:
Doc length: 11
E tenho dito: o Palmeiras não tem mundial. :)


##### Importante !
Componentes personalizados são ótimos para adicionar informações customizadas aos documentos, 
tokens e partições e também para customizar as entidades doc.ents.
Ex.: 
    Calcular alguns valores utilizando os tokens e seus atributos.
    Adicionar entidades nomeadas baseado em um dicionário, por exemplo.
Componentes personalizados são adicionados ao fluxo de processamento após o idioma ser carregado e 
depois da toquenização, portanto não são adequados para adicionar novos idiomas.
"""

# Este exemplo mostra um componente personalizado que imprime o número de tokens em um documento.


@Language.component("length_component")
def length_component_function(doc):
    # Calcule o tamanho do doc
    doc_length = len(doc)
    print(f"Este documento tem {doc_length} tokens.")
    # Retorne o doc
    return doc


nlp = spacy.load("pt_core_news_sm")
nlp.add_pipe("length_component", first=True)
print(f"{nlp.pipe_names}\n")
"""
Saída:
['length_component', 'custom_component', 'tok2vec', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler', 'ner']
"""

# Processa um texto
doc = nlp("Sábio é aquele que conhece os limites da própria ignorância. - Sócrates")

print(f"{doc}\n")
"""
Saída:
Este documento tem 13 tokens.
Doc length: 13
Sábio é aquele que conhece os limites da própria ignorância. - Sócrates
"""

print("\n2")
"""
Exemplo de um componente personalizado que usará o PhraseMatcher para identificar nomes de animais no documento e 
adicionar as partições reconhecidas ao doc.ents.
"""
nlp = spacy.load("pt_core_news_sm")
animals = ["Golden Retriever", "gato", "tartaruga", "Rattus norvegicus"]
animals_patterns = list(nlp.pipe(animals))
print(f"animal_patterns: {animals_patterns}")
"""
Saída:
animal_patterns: [Golden Retriever, gato, tartaruga, Rattus norvegicus]
"""
matcher = PhraseMatcher(nlp.vocab)
matcher.add("ANIMAL", animals_patterns)


# Definir o componente customizado
@Language.component("animal_component")
def animal_component_function(doc):
    # Aplicar o matcher ao doc
    matches = matcher(doc)
    # Criar uma partição para cada correspondência e atribuir o rótulo "ANIMAL"
    spans = [Span(doc, start, end, label="ANIMAL") for match_id, start, end in matches]
    # Sobrescrever doc.ents com as correspondências
    doc.ents = spans
    return doc


# Adicionar o componente ao fluxo de processamento após o componente "ner"
nlp.add_pipe("animal_component", after="ner")
print(f"Pipe names: {nlp.pipe_names}")
"""
Saída:
Pipe names: ['tok2vec', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler', 'ner', 'animal_component']
"""

# Processar o texto e imprimir o texto e rótulo de doc.ents
doc = nlp("Eu tenho um gato e um Golden Retriever")
print(f"Correspondências: {[(ent.text, ent.label_) for ent in doc.ents]}")
"""
Saída:
Correspondências: [('gato', 'ANIMAL'), ('Golden Retriever', 'ANIMAL')]
"""
