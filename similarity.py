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
        similar_qs.append([similarity, qs[i], scraping.answers[i]])
    similar_qs.sort(reverse=True)
    if similar_qs[0][0] >= 0.9:
        high_similar_qs = []
        for que in similar_qs:
            if que[0] <= 0.9:
                break
            high_similar_qs.append(que)
        return high_similar_qs
    first_sim = similar_qs[0][0]
    last_sim = first_sim - 0.15
    new_similar_qs = []
    for quest in similar_qs:
        if quest[0] <= last_sim:
            break
        new_similar_qs.append(quest)
    return new_similar_qs

