# import libraries
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import csv
import re


# MAKE SURE TO CHANGE THIS PATH
file = open("data/original_html.html", encoding="utf8")

# parse the html using beautiful soup
soup = BeautifulSoup(file.read(), 'html.parser')

questions = soup.find_all('h2')

# Delete the last element in the array which are not relevant questions
questions.pop()

answers = []

for i in range(len(questions)):

    html_section = questions[i]
    id_name = questions[i].get('id')

    starting_point = soup.find('h2', id=id_name)

    sib = starting_point.next_sibling
    answer = []

    while sib.name != 'h2' and sib.name != 'h1':
        answer.append(sib)
        sib = sib.next_sibling

    # delete the "Return to Top" button and html separator
    answer.pop()
    answer.pop()

    # update answer array
    answers.append(answer)



# write to csv, we never used this
with open('data/qa.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    for i in range(len(questions)):
        writer.writerow((questions[i], answers[i]))
    
csvfile.close()

# removing html tags, we never used this
with open('data/qa2.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    for i in range(len(questions)):
        # cleantext = BeautifulSoup(answers[i], "lxml").text

        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', f'{answers[i]}')
        writer.writerow((questions[i], cleantext))
    
csvfile.close()


