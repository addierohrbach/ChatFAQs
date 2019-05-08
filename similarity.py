import scraping
import spacy

nlp = spacy.load('en_core_web_md')

qs = scraping.questions

def fixqs(questions):
    return "".join([str(x) for x in questions.contents])

def predict(question):
    formatted_qs = [fixqs(q) for q in qs]
    input_question = nlp(question)
    similar_qs = []
    for i in range(len(formatted_qs)):
        q = nlp(formatted_qs[i])
        similarity = input_question.similarity(q)
        if similarity >= 0.9:
            similar_qs.append([similarity, qs[i], scraping.answers[i]])
    similar_qs.sort(reverse=True)
    return similar_qs

