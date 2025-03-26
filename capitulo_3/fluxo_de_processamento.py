"""
Componentes padrão do fluxo de processamento

O que acontece quando você usa nlp?

doc = nlp("Na era da informação, a invisibilidade é equivalente à morte." - Zygmunt Bauman )

Você já viu esse comando diversas vezes:
passar um texto como argumento para o objeto nlp e receber um objeto Doc.

Mas o que o objeto nlp de fato faz?

Inicialmente o toquenizador (tokenizer) é aplicado ao texto e ele é transformado em um objeto Doc.
Em seguida, uma série de componentes são aplicados sequencialmente no objeto Doc:
o tagueador (tagger), o analisador (parser) e o identificador de entidades.
Por fim, o documento processado é retornado, e você poderá trabalhar com ele.

A biblioteca spaCy possui uma variedade de componentes para o fluxo de processamento.
Esses são os mais comuns que você provavelmente utilizará em seus projetos:

- O tagueador (tagger) de classes gramaticais cria os atributos token.tag e token.pos.
- O analisador sintático cria os atributos token.dep e token.head e também é responsável por identificar sentenças e
frases nominais, também conhecidas como "pedaços de substantivos" (noun chunks).
- O identificador de entidades adiciona entidades ao atributo doc.ents.
Ele também atribui o tipo de entidade aos tokens, que indica se um token é parte de uma entidade ou não.
- E por último, o classificador de textos define os marcadores de categoria que se aplicam ao texto como um todo,
adicionando essa informação ao atributo doc.cats.

Uma vez que as categorias de texto são bastante específicas, o classificador de texto não está incluso em nenhum dos
fluxos de processamento (pipelines) treinados.
Mas você pode utilizá-lo em seu projeto.

-----------------------------------------------------------------------------------------------------------------------
Nome       | Descrição                                                 | O que cria
-----------------------------------------------------------------------------------------------------------------------
tagger     | Tagueador de classes gramaticais(part-of-speech tagger)   | Token.tag, Token.pos
-----------------------------------------------------------------------------------------------------------------------
parser     | Analisador sintático (dependency parser)                  | Token.dep, Token.head, Doc.sents,
           |                                                           | Doc.noun_chuncks
-----------------------------------------------------------------------------------------------------------------------
ner        | Identificador de entidades (named entity recognizer)      | Doc.ents, Token.ent_iob, Token.ent_type
-----------------------------------------------------------------------------------------------------------------------
textcat    | Classificador de texto (text classifier)                  | Doc.cats
-----------------------------------------------------------------------------------------------------------------------

Nos bastidores

pt_core_news_sm

config.cfg
[nlp]
lang = "pt"
pipeline = ["tok2vec", "tagger", "parser", "ner", ...]

    O fluxo de processamento (pipeline) ocorre sequencialmente conforme definido no arquivo config.cfg
    Os componentes padrão usam dados binários para fazer as previsões

Todos os pacotes de fluxo de processamento que você pode importar na biblioteca spaCy incluem vários arquivos,
dentre eles o config.cfg.
O arquivo config define o idioma e o fluxo de processamento.
Ele indica quais componentes precisam ser instanciados pela spaCy e como eles devem ser configurados.
Os componentes internos que fazem as previsões necessitam de dados binários.
Esses dados estão inclusos no pacote do fluxo de procesamento e são carregados nos componentes quando você carrega
o fluxo (pipeline).

Atributos do fluxo de processamento

nlp.pipe_names: lista dos nomes dos componentes
print(nlp.pipe_names)
# Saída: ['tok2vec','tagger', 'parser', 'ner','attribute_ruler', 'lemmatizer']

nlp.pipeline: lista de tuplas (name, component)
print(nlp.pipeline)
# Saída:
[('tok2vec', <spacy.pipeline.Tok2Vec>),
 ('tagger', <spacy.pipeline.Tagger>),
 ('parser', <spacy.pipeline.DependencyParser>),
 ('ner', <spacy.pipeline.EntityRecognizer>)
 ('attribute_ruler', <spacy.pipeline.AtributeRuler>),
 ('lemmatizer', <spacy.pipeline.Lemmatizer>),
 ]

Para verificar os nomes dos componentes do fluxo de processamento presentes no objeto atual,
você pode usar o atributo nlp.pipe_names.
Para obter uma lista de tuplas com o nome do componente e sua função, você pode usar o atributo nlp.pipeline.
A função de um componente é a função que é aplicada ao documento para processá-lo e definir alguns atributos,
como por exemplo, classe gramatical, termos sintáticos e de entidades.
"""

"""
Entendendo o que acontece nos bastidores quando se processa um texto.
Aprendendo a escrever os próprios componentes e adicioná-los ao fluxo de processamento, e também a usar atributos
personalizados para adicionar metadados aos documentos, partições e tokens.
"""
print("\n1")
import spacy

nlp = spacy.load("pt_core_news_sm")

# Imprime o nome dos componentes do fluxo
print(nlp.pipe_names)
"""
Saída:
['tok2vec', 'morphologizer', 'parser', 'lemmatizer', 'attribute_ruler', 'ner']
"""

# Imprime as informações das tuplas (name, component)
print(nlp.pipeline)
"""
Saída:
[
    ('tok2vec', <spacy.pipeline.tok2vec.Tok2Vec object at 0x7fe7af697dd0>), 
    ('morphologizer', <spacy.pipeline.morphologizer.Morphologizer object at 0x7fe7af697470>), 
    ('parser', <spacy.pipeline.dep_parser.DependencyParser object at 0x7fe7af768200>), 
    ('lemmatizer', <spacy.pipeline.edit_tree_lemmatizer.EditTreeLemmatizer object at 0x7fe7af696bd0>), 
    ('attribute_ruler', <spacy.pipeline.attributeruler.AttributeRuler object at 0x7fe7af615410>), 
    ('ner', <spacy.pipeline.ner.EntityRecognizer object at 0x7fe7af7683c0>)
]
"""
