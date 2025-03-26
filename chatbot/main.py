# Base de dados
database = {
    "Oi": "Olá.",
    "Olá": "Olá. Tudo bem?",
    "Qual é o seu nome?": "Meu nome é Chatbot.",
    "Como você se chama?": "Meu nome é Chatbot.",
    "Como você está?": "Estou bem, obrigado por perguntar!",
    "Qual é a capital do Brasil?": "A capital do Brasil é Brasília.",
    "Qual a sua idade?": "Sou um programa de computador, não tenho idade.",
    "O que você pode fazer?": "Posso responder a perguntas e fornecer informações gerais.",
}

# Processar perguntas
from pprint import pprint as p
import spacy

nlp = spacy.load("pt_core_news_md")


def process_question(question):
    return nlp(question)


def find_answer(user_question):
    user_question_processed = process_question(user_question)
    better_similarity = 0.6
    better_answer = "Desculpe, não entendi a pergunta."

    for question, answer in database.items():
        question_processed = process_question(question)
        similarity = user_question_processed.similarity(question_processed)

        if similarity > better_similarity:
            better_similarity = similarity
            better_answer = answer
    return better_answer


while True:
    user_question = input("You: ")
    if user_question.lower() == "sair":
        p("Bot: bye, bye!")
        break
    answer = find_answer(user_question)
    p(str(f"Bot: {answer}"))
