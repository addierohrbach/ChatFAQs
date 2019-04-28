import scraping
import spacy
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()

# input_variable = "I keep forgetting my password. Is there an easier way to sign in?"
input_variable = "".join([str(x) for x in scraping.questions[0].contents])


""" Does:
        tokenizes the input
        stems the tokens
        separates stop words from stems
    Returns:
        stems: array of appropriate stems
        stops: array of stop words
"""
def tok_stem(user_question):
    # loads the spacy model
    # need to run 'python -m -spacy download en_core_web_sm' in command line first
    nlp = spacy.load("en_core_web_sm")

    # add new line character to stop words
    nlp.vocab["\n    "].is_stop = True
    
    # create array of tokens
    doc = nlp(user_question)

    stems = []
    stops = []
    
    doc = [word if word.lemma_ != "-PRON-" else word for word in doc]
    doc = [ token.lemma_ for token in doc if (token.is_stop == False) and (not token.is_punct)]
        #word for word in doc if word.is_stop == False and word not in punctuations]
    return doc 
    '''
    # for each token, separate usable stems from stop words
    for token in doc:
        if (token.is_stop == False) and (not token.is_punct):
            stems.append(token.lemma_)
        else:
            stops.append(token.lemma_)
    
    return stems, stops
    '''
""" Does:
        applies tok_stem to each question
    Returns:
        q_tok_stems: multi-dim array of the appropriate stems for each question
        q_tok_stems_stops: multi-dim array of the stop words for each question
"""
def tok_stem_qs(questions):
    
    q_tok_stems = []
    q_tok_stops = []
    print('1',len(questions))
    print('2',len(questions[0]))
    print('3',len(questions[1]))
    for q in range(len(questions)):
        q_input = "".join([str(x) for x in questions[q].contents])
        # print(f'-----{q_input}----')
        stems = tok_stem(q_input)
        #stems = stems.append(q)
        # print(f'tokens: {stems}')
        q_tok_stems.append(stems)
        #q_tok_stops.append(stops)

    return q_tok_stems#, q_tok_stops

class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [text for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}
        
def fixqs(questions):
    return "".join([str(x) for x in questions.contents])

stems = tok_stem(input_variable)
print(f'input_variable: {input_variable}')
print(f'stems: {stems}')
#print(f'stops: {stops}')

#q_stems = tok_stem_qs(scraping.questions)
#print(f'stems: {q_stems}')

qs=scraping.questions
qs=[fixqs(q) for q in qs]
print('fixed', qs)

classes =  list(range(0, len(scraping.questions)))

bow_vector = CountVectorizer(tokenizer = tok_stem, ngram_range=(1,1))
tfidf_vector = TfidfVectorizer(tokenizer = tok_stem)
pipe = Pipeline([("cleaner", predictors()),
                 ('vectorizer', bow_vector),
                 ('classifier', classifier)])
pipe.fit(qs,classes)

print(scraping.questions[77])

predicted = pipe.predict(["forgetting my password. Is there an way to sign in?"])
print(predicted)
