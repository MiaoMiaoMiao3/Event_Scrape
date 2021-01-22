#MODULES
from bs4 import BeautifulSoup
import requests

# WEBSCRAPE SETUP
html_target = 'https://www.greaterseattleonthecheap.com/free-and-cheap-things-to-do-in-seattle-this-weekend/'
source = requests.get(html_target).text
soup = BeautifulSoup(source, 'lxml')

#VARIABLES
all_events_txt = open('test.txt', 'w+')
event_set = set()
event_links = set()

new_month = soup.find("h3").text
all_events_txt.truncate(0)

#READ IN PREVIOUS EVENTS
for line in all_events_txt:
    if line.find("http") != -1:
        event_links.add(line.strip())
    elif line != "":
        event_set.add(line.strip())

# #INPUT IN EVENTS
for event in soup.find_all(class_ = "row event featured"):
    child = event.find("div").find("a")
    if not event.text in event_set:
        event_set.add(event.text)
        event_links.add(child["href"])
        all_events_txt.write (event.h3.text)
        all_events_txt.write('\n')
        all_events_txt.write (child["href"])
        all_events_txt.write('\n')
        all_events_txt.write('\n')

all_events_txt.close()
# print(event_set)
print('******WRITE COMPLETE******')
