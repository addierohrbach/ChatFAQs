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

print(heading_box)

