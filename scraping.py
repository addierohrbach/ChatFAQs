# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup

# specify the url
website = 'https://myc.nm.org/MyChart/default.asp?mode=stdfile&option=faq#RE_enhancements'

# query the website and return the html
page = urlopen(website)

# parse the html using beautiful soup
soup = BeautifulSoup(page, 'html.parser')

heading_box = soup.find_all('h2')
# Deletes the last three elements in the array which are not relevant questions
heading_box.pop()
heading_box.pop()
heading_box.pop()

# print(heading_box)
# print(len(heading_box))
# print(heading_box[0])
multi_array = []

for i in range(len(heading_box)):
    print(f'----------{i}---------------')
    html_section = heading_box[i]

    id_name = heading_box[i].get('id')

    starting_point = soup.find('h2',id=id_name)
    print(f'starting point {starting_point}')
    
    if starting_point.next_sibling == None:
        break
    next_sib = starting_point.next_sibling.next_sibling
    next_sib_child = ""

    # print(f'------check {id_name}--------')
    if len(next_sib.contents) > 0:  
        next_sib_child = next_sib.contents[0]
    array = []

    
    while next_sib_child != soup.find('a', href = '#top'):
        array.append(next_sib)
        next_sib = next_sib.next_sibling.next_sibling
        if len(next_sib.contents) > 0:  
            
            next_sib_child = next_sib.contents[0]

    # print(array)
    multi_array.append(array)
# print(multi_array)