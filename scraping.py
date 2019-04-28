# import libraries
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import json
import csv

# file = codecs.open("data/original_html.html", "r")
file = open("data/original_html.html", encoding="utf8")

# parse the html using beautiful soup
soup = BeautifulSoup(file.read(), 'html.parser')

questions = soup.find_all('h2')

# Delete the last element in the array which are not relevant questions
questions.pop()

answers = []

# def fixqs(faq_strings):
#     for i in range(0,len(faq_string):
#         "".join([str(x) for x in faq_string.contents])

for i in range(len(questions)):
    html_section = questions[i]
    id_name = questions[i].get('id')

    starting_point = soup.find('h2', id=id_name)

    sib = starting_point.next_sibling
    answer = []

    while sib.name != 'h2':
        answer.append(sib)
        sib = sib.next_sibling

    answers.append(answer)

# write answers and questions into csv file, to prevent running scraping every time we run
with open('data/questions.json', 'w') as f:
    json.dump(str(questions), f)

with open('data/answers.json', 'w') as f:
    json.dump(str(answers), f)

# with open('data/questions.csv', 'w') as write_file:
#     writer = csv.writer(write_file)
#     writer.writerow([questions])
wtr = csv.writer(open('data/questions.csv', 'w'), delimiter = '\f')
for x in questions: wtr.writerow([x])

# write_file.close()

with open('data/answers.csv', 'w') as write_file:
    writer = csv.writer(write_file)
    writer.writerow([answers])

write_file.close()

print(f'questions: {questions}')



# print(f'{questions}')

#----debugging-----
# print(f'answers: {answers}')
# print(f'answers len: {len(answers)}')
# print(f'questions len: {len(heading_box)}')

# # Open spreadsheet for reading
# wb = load_workbook(filename='data/faq_spreadsheet.xlsx')
# # Get the current active sheet
# ws = wb.get_active_sheet()
#
# # Load questions into the first column
# for i in range(len(heading_box)):
#     ws['A', i + 1] = heading_box[i]
#
# # Load answers into the second column
# for j in range(len(answers)):
#     ws['B', j + 1] = answers[j]
#
# # Save workbook
# wb.save('data/faq_spreadsheet.xlsx')
