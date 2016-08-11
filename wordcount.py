#!/afs/crc.nd.edu/x86_64_linux/python/3.4.0/gcc-4.8.0/bin/python3

import string
import requests
import datetime
from bs4 import BeautifulSoup
from collections import Counter

# Request html doc from google
url = "https://news.google.com" 
request = requests.get(url)
html_raw = request.content


# Make soup and find all Titles
soup = BeautifulSoup(html_raw,'html.parser')
titletext_elements = soup.find_all('span', {'class': 'titletext'}, text=True)

def stripTagsandMakeList(title_elements): 
    temp_list = []
    for i in range(len(title_elements)):
        title_tag = title_elements[i]
        temp_list.append(title_tag.string)
    return temp_list 

titleList = stripTagsandMakeList(titletext_elements)        

def writeTitlestoFile(titleList):
     f = open('titles.txt', 'w')
     for i in range(len(titleList)):
         f.write(titleList[i])
         f.write('\n')
     f.close()

writeTitlestoFile(titleList) 
   
def stripPunctuation(titleList):
    puncList = ["|",":",".",";",":","!","?","/","\\",",","#","@","$","&",")",'"',"(","-","\""]
    for punc in puncList:
        for title in titleList:
            titleList = [title.replace(punc,'') for title in titleList]
    return titleList

titleList = stripPunctuation(titleList)

def splitStrings(titleList):
    wordList = []
    for title in range(len(titleList)):
        titleList[title] = titleList[title].rsplit(sep=None,maxsplit=-1)     
        wordList.append(titleList[title])
    return wordList

wordList = splitStrings(titleList)

def countWords(wordList):
    c = Counter()
    for inner_list in wordList:
        for item in inner_list:
            c[item] += 1 
    return c

counter = countWords(wordList)

def writeCountertoFile(counter):
    now = datetime.datetime.now()
    with open('countofwords-%s.txt' % now.strftime("%Y-%m-%d %H:%M"), 'w') as f:
        for word, count in counter.most_common():
            print("%s:%d" % (word, count), file=f)

writeCountertoFile(counter) 


