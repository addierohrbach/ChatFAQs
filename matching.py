import scraping
import spacy
from bs4 import BeautifulSoup

# input_variable = "I keep forgetting my password. Is there an easier way to sign in?"
input_variable = "".join([str(x) for x in scraping.questions[0].contents])

def tok_stem(user_question):
    
    # loads the spacy model
    # need to run 'python -m -spacy download en_core_web_sm' in command line first
    nlp = spacy.load("en_core_web_sm")

    # add new line character to stop words
    nlp.vocab["\n    "].is_stop = True
    
    doc = nlp(user_question)

    tokens = []
    stop = []

    for token in doc:
        if (token.is_stop == False) and (not token.is_punct):
            tokens.append(token.lemma_)
        else:
            stop.append(token.lemma_)

    return tokens, stop

def tok_stem_qs(questions):
    
    q_tok_stems = []
    q_tok_stems_stops = []

    for q in questions:
        q_input = "".join([str(x) for x in q.contents])
        print(f'-----{q_input}----')
        tokens, stops = tok_stem(q_input)
        print(f'tokens: {tokens}')
        q_tok_stems.append(tokens)
        q_tok_stems_stops.append(stops)

    return q_tok_stems, q_tok_stems_stops

return_var1, return_var2 = tok_stem(input_variable)
print(f'input_variable: {input_variable}')
print(f'tokens: {return_var1}')
print(f'stops: {return_var2}')

stems, stops = tok_stem_qs(scraping.questions)
print(f'stems: {stems}')
