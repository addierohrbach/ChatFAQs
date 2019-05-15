import scraping
import spacy
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()

# loads the spacy model
# need to run 'python -m spacy download en_core_web_sm' in command line first
nlp = spacy.load("en_core_web_md")

# add new line character to stop words
nlp.vocab["\n    "].is_stop = True


""" Does:
        tokenizes the input
        separates stop words from stems
    Returns:
        doc: the tokenized and initially filtered questions
"""
def tok_stem(user_question):       
    # create tokens and filter
    doc = nlp(user_question)    
    doc = [ token.lemma_ for token in doc if (token.is_stop == False) and (not token.is_punct) and (token.lemma_ != "-PRON-")]
    return doc 

#creates the cleaner for the pipeline classifer
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [text for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

""" Does:
        for each question take the question out of the html
    Returns:
        the html-free questions
"""        
def fixqs(questions):
    return "".join([str(x) for x in questions.contents])


#create a list of clean, html-free questions
qs=scraping.questions
qs=[fixqs(q) for q in qs]

#class names corresponding to index of question
classes =  list(range(0, len(scraping.questions)))

count_vector = CountVectorizer(tokenizer = tok_stem, ngram_range=(1,1))
tfidf_vector = TfidfVectorizer(tokenizer = tok_stem)
pipe = Pipeline([("cleaner", predictors()),
                 ('vectorizer', count_vector),
                 ('classifier', classifier)])
pipe.fit(qs,classes)

def predict(question):
    predicted = pipe.predict([question])
    return qs[(int(predicted))],scraping.answers[int(predicted)]

#unused functions
'''
""" Does:
        applies tok_stem to each question
    Returns:
        q_tok_stems: multi-dim array of the appropriate stems for each question
"""
def tok_stem_qs(questions):
    
    q_tok_stems = []
    for q in range(len(questions)):
        q_input = "".join([str(x) for x in questions[q].contents])
        stems = tok_stem(q_input)
        q_tok_stems.append(stems)

    return q_tok_stems
'''
