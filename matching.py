import scraping
import spacy
from bs4 import BeautifulSoup

# for matching function
from spacy.pipeline import TextCategorizer

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

    # for each token, separate usable stems from stop words
    for token in doc:
        if (token.is_stop == False) and (not token.is_punct):
            stems.append(token.lemma_)
        else:
            stops.append(token.lemma_)

    return stems, stops, nlp

""" Does:
        applies tok_stem to each question
    Returns:
        q_tok_stems: multi-dim array of the appropriate stems for each question
        q_tok_stems_stops: multi-dim array of the stop words for each question
"""
def tok_stem_qs(questions):
    
    q_tok_stems = []
    q_tok_stops = []

    for q in questions:
        q_input = "".join([str(x) for x in q.contents])
        # print(f'-----{q_input}----')
        stems, stops, nlp = tok_stem(q_input)
        # print(f'tokens: {stems}')
        q_tok_stems.append(stems)
        q_tok_stops.append(stops)

    return q_tok_stems, q_tok_stops

def matching():
    stems, stops, nlp = tok_stem(input_variable)
    q_stems, q_stops = tok_stem_qs(scraping.questions)
    
    # initalize a TextCategorizer object
    textcat = TextCategorizer(nlp.vocab)
    
    # begin training the object
    nlp.pipeline.append(textcat)
    optimizer = textcat.begin_training(pipeline = nlp.pipeline)


    raise NotImplementedError()


# print(f'{scraping.questions[60]}')
# stems, stops, nlp = tok_stem(input_variable)
# print(f'input_variable: {input_variable}')
# print(f'stems: {stems}')
# print(f'stops: {stops}')
print(f'{scraping.questions[86]}')

# q_stems, q_stops = tok_stem_qs(scraping.questions)
# print(f'stems: {q_stems}')
