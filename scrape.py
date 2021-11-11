from bs4 import BeautifulSoup

# ? _________________________________
# * LOCAL HTML FILE PARSING
# ? _________________________________

# ? Opening the test.html file. "r" is passed as we want to read this file. 
# ? The result is stored in 'file'.

with open('test.html', "r") as file:

# ? Using BeautifulSoup to read the result, and parse it using a build in parser, and storing the results in 'doc'''
    doc = BeautifulSoup(file, "html.parser")

# ? Can use the doc class with dot notation to access any tag from the html document.
tag = doc.title

# ?To access the string that's contained within the tag. Which in this example would result in 'Document', the text between the title tag.'''

# print(tag.string)

# ? You can modify the string value within tags as well:
# tag.string = 'something else'
# print(tag)

# ? Using another method from doc class, you can also find tags, along with indexing to select a specific one. Looking for the first div tag

foundTags = doc.find_all('div')[0]

# ? Then you can find ANY nested tags, in this case, main is contained within the fist div.

print(foundTags('main'))

# print(doc.prettify())

# ? _________________________________
# * REMOTE HTML FILE PARSING
# ? _________________________________