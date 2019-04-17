# import libraries
from urllib.request import urlopen
import bs4
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import codecs

<<<<<<< HEAD
file = codecs.open("data/original_html.html", "r")

# parse the html using beautiful soup
soup = BeautifulSoup(file.read(), 'html.parser')
=======
# specify the url
# website = 'https://myc.nm.org/MyChart/default.asp?mode=stdfile&option=faq'

# query the website and return the html
# page = urlopen(website)

# parse the html using beautiful soup
fixed = codecs.open("fixed.html",'r')
soup = BeautifulSoup(fixed, 'html.parser')
# soup = BeautifulSoup(page, 'lxml')
print(soup.prettify())
>>>>>>> 845a3e0d46be7be4b07b48fed66f6910b76fb8d7

heading_box = soup.find_all('h2')
# Deletes the last three elements in the array which are not relevant questions
heading_box.pop()
heading_box.pop()
heading_box.pop()

# multidemensional array of answers
multi_array = []

# array of h2 id's where errors occured, thus potentially false data in multi_array
error_arr = []

for i in range(len(heading_box)):
    print(f'----------{i}---------------')
    html_section = heading_box[i]

    id_name = heading_box[i].get('id')

    starting_point = soup.find('h2',id=id_name)
    print(f'starting point {starting_point}')
    print(f'starting point.next_sib = {starting_point.next_sibling}')

    # if there is no next sibling for some reason, move on to the next question
    # if starting_point.next_sibling == None:
    #     error_arr.append(id_name)
    #     # print(f'-----error {id_name} ------ {error_arr}')
    #     continue

    next_sib = starting_point.next_sibling.next_sibling
    next_sib_child = ""

    # print(f'------check {id_name}--------')
    if len(next_sib.contents) > 0:
        next_sib_child = next_sib.contents[0]
    array = []

    while next_sib_child != soup.find('a', href = '#top'):
        array.append(next_sib)
        # if next_sib.next_sibling == None:
        #     error_arr.append(id_name)
        #     # print(f'-----error {id_name} ------ {error_arr}')
        #     break
        # if next_sib.next_sibling.next_sibling == None:
        #     error_arr.append(id_name)
        #     # print(f'-----error {id_name} ------ {error_arr}')
        #     break
        # if type(next_sib) is not bs4.element.NavigableString:
        #     error_arr.append(id_name)
        #     # print(f'-----error {id_name} ------ {error_arr}')
        #     break
        next_sib = next_sib.next_sibling.next_sibling
        if len(next_sib.contents) > 0:

            next_sib_child = next_sib.contents[0]
    print(array)
    multi_array.append(array)

print(f"full array: {multi_array}")
print(f"error_array: {error_arr}")

# Input all of the data into an excel spreadsheet
def update_xlsx(src):
    # Open spreadsheet for reading
    wb = load_workbook(filename=src)
    # Get the current active sheet
    ws = wb.get_active_sheet()

    # Load questions into the first column
    for x in range(len(heading_box)):
        ws['A' + x] = heading_box[x - 1]

    # Save workbook
    wb.save(src)


update_xlsx('data/faq_spreadsheet.xlsx')
