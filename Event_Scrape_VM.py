#MODULES
from bs4 import BeautifulSoup
import requests

#CONSTANTS & VARIABLES
html_target = 'https://www.greaterseattleonthecheap.com/free-and-cheap-things-to-do-in-seattle-this-weekend/'
TXT_FILE = '/home/utp56479user/Event_Scraper/event.txt' #REPLACE WITH THE DIRECTORY YOU CREATED

SRC_FILE = TXT_FILE
event_set = set()
event_links = set()

# WEBSCRAPE SETUP
all_events_txt = open(TXT_FILE, 'w+')
source = requests.get(html_target).text
soup = BeautifulSoup(source, 'lxml')


#ADD DATE
new_weekend = soup.find("h3").text
all_events_txt.write('Weekend of '+ new_weekend + ','+'\n')

# #INPUT IN EVENTS
for event in soup.find_all(class_ = "row event featured"):
    child = event.find("div").find("a")
    if not event.text in event_set:
        event_set.add(event.text)
        event_links.add(child["href"])
        all_events_txt.write (event.h3.text + ',' + '\n')
        all_events_txt.write (child["href"] + '\n'*2)


all_events_txt.close()