from bs4 import BeautifulSoup
import requests

# with open('GCPLabs.html') as html_file:
#     soup = BeautifulSoup(html_file, 'lxml')

# for article in soup.find_all('h3', class_='hide-from-toc'):
#     print(article.text)

html_target = 'https://www.greaterseattleonthecheap.com/free-and-cheap-things-to-do-in-seattle-this-weekend/'
source = requests.get(html_target).text
soup = BeautifulSoup(source, 'lxml')

# All_Events = open('test.txt', 'w+')
# All_Events.write(soup.prettify())
for event in soup.find_all(class_ = "row event featured"):
    child = event.find("div").find("a")
    print(child["href"])
# for event in soup.find_all(class_ = "row event featured"):
    # All_Events.write(event.text)
    # All_Events.write('\n')
    # children = event.find('div')
    # print(children)

print('******WRITE COMPLETE******')