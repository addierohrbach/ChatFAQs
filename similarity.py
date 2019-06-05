
import scraping
import spacy
import numpy as np
from bs4 import BeautifulSoup
import copy


nlp = spacy.load('en_core_web_md')

qs = scraping.questions

referenceterms = ['they', 'it', 'them', 'this', 'that', 'these', 'those', 'the former', 'the latter', 'who', 'which', 'that', 'one', 'ones', 'such']

def fixqs(questions):
    return "".join([str(x) for x in questions.contents])

def calculate(question):
    formatted_qs = [fixqs(q) for q in qs]
    input_question = nlp(question)
    similar_qs = []
    for i in range(len(formatted_qs)):
        q = nlp(formatted_qs[i])
        similarity = input_question.similarity(q)
        similar_qs.append([similarity, qs[i], scraping.answers[i], i])  
    return similar_qs

def returnquestion(index):
    return qs[index]

def predict(question):
    similar_qs = calculate(question)
    similar_qs.sort(reverse=True)
    #new_similar_qs = selectbestmatches(similar_qs)
    return similar_qs

def selectbestmatches(similar_qs):
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
        if quest[0] <= last_sim or quest[0] < .5:
            break
        new_similar_qs.append(quest)
    
    if len(new_similar_qs) == 0:
        new_similar_qs.append([0, "<h2>Results not Found.</h2>", ['\n', "<p>Try rewording your question.</p>", '\n']])
    return new_similar_qs


def predictusinganswer(index, nquestion): 
    global referenceterms
    question = nlp(nquestion)
    for x in question:
        if x.lemma_.lower() in referenceterms:
            ans = scraping.answers[index]
            ansstr = ''
            for ele in ans:
                if ele != '\n':
                    contents = ele.contents
                    for content in contents:
                        if content.string is not None: 
                            ansstr += content.string
            predict1 = calculate(ansstr)
            predict2 = calculate(nquestion)
            
            newprob = calculate(ansstr)

            for i in range(len(predict1)):
                newprob[i][0] = .2 *predict1[i][0] + (.8 * predict2[i][0])
            newprob.pop(index)
            newprob.sort(reverse=True)
            #newprob = selectbestmatches(newprob)
            return newprob
    return predict(nquestion)




