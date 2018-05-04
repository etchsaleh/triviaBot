#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

# triviaBot - Answers live trivia game questions with a 80% avg success rate.

# Created by Hesham Saleh on 07/03/18.
# Copyright © 2018 Hesham Saleh. All rights reserved.

import io
import os

#Take screenshots
#os.system("screencapture -R910,215,350,90 question.png")
#os.system("screencapture -R930,370,235,35 ansA.png")
#os.system("screencapture -R930,445,235,35 ansB.png")
#os.system("screencapture -R930,520,235,35 ansC.png")

# OCR (text extraction)
from PIL import Image
import pytesseract

# Parallel requests
from joblib import Parallel, delayed

# Regex
import re

# Google Scraper (Beautiful Soup 4)
import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser

# Google Custom Search
from googleapiclient.discovery import build

# Credentials
my_cse_id = "017243323922835907384:7bywfbe83ve"
dev_key = "AIzaSyDpTXV69ahVIKhUUWtQ9p4gyO1TY_omTl8"

# Image directory
question_file = os.path.join(
    os.path.dirname(__file__),
    'question.png')
ans1_file = os.path.join(
    os.path.dirname(__file__),
    'ansA.png')
ans2_file = os.path.join(
    os.path.dirname(__file__),
    'ansB.png')
ans3_file = os.path.join(
    os.path.dirname(__file__),
    'ansC.png')

q  = Image.open(question_file)
a1 = Image.open(ans1_file)
a2 = Image.open(ans2_file)
a3 = Image.open(ans3_file)

# Q&A parsing
q_text  = pytesseract.image_to_string(q)
a1_text = pytesseract.image_to_string(a1)
a2_text = pytesseract.image_to_string(a2)
a3_text = pytesseract.image_to_string(a3)

# Single characters (Change Page Segmentation Mode)
if a1_text == "" or a2_text == "" or a3_text == "":
    a1_text = pytesseract.image_to_string(a1,config='-psm 10000')
    a2_text = pytesseract.image_to_string(a2,config='-psm 10000')
    a3_text = pytesseract.image_to_string(a3,config='-psm 10000')

"""
q_text  = q_text.lower().replace("spfing", "spring")
a1_text = a1_text.lower().replace("spfing", "spring")
a2_text = a2_text.lower().replace("spfing", "spring")
a3_text = a3_text.lower().replace("spfing", "spring")
"""
a1_text = a1_text.replace("ﬂ", "fi")
a1_text = a1_text.replace("ﬁ", "fi")
a2_text = a2_text.replace("ﬂ", "fi")
a2_text = a2_text.replace("ﬁ", "fi")
a3_text = a3_text.replace("ﬂ", "fi")
a3_text = a3_text.replace("ﬁ", "fi")

answers = [a1_text,a2_text,a3_text]

q_text = q_text.replace("ﬂ", "fi")
q_text = q_text.replace("ﬁ", "fi")
q_text_arr = q_text.split("\n")

q_arr = []
for s in q_text_arr:
    if not (s == "" or re.match(' +',s)):
        q_arr.append(s)
question = ' '.join(q_arr)

print("Question: " + question + "\na) " + answers[0] + "\nb) " + answers[1] + "\nc) " + answers[2] + "\n")

question = question.lower()

notFlag = False
if " not " in question or "never" in question:
    question = question.replace("not","")
    question = question.replace("never","")
    notFlag = True

# Calculates percentage of correctness compared to alternative options
def confidence(res):
    if notFlag:
        return("  (confidence: " + str(100 - round((res/total)*100)) + "%)")
    return("  (confidence: " + str(round((res/total)*100)) + "%)")

# Google first page results
text = urllib.parse.quote_plus(question)

url = 'https://google.com/search?q=' + text

response = requests.get(url)
output = ""
soup = BeautifulSoup(response.text, 'lxml')
for g in soup.find_all(class_='g'):
    output += g.text

def count(answer):
    counter = 0
    counter = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(answer.lower()), output.lower()))
    return str(counter)

# Queries are run in parallel using joblib
results = Parallel(n_jobs=4)(delayed(count)(answer) for answer in answers)

a = int(results[0])
b = int(results[1])
c = int(results[2])

maxVal = max(a,b,c)
total = a + b + c
if total == 0: total = 1 # Division by Zero

print("Google Search results")

if a == b and b == c:
    print("----NO RESULT----")
    
elif notFlag:
    
    minVal = min(a,b,c)
    
    if minVal == a:
        print("Answer is " + answers[0] + confidence(a))
    elif minVal == b:
        print("Answer is " + answers[1] + confidence(b))
    else:
        print("Answer is " + answers[2] + confidence(c))
else:
    
    if maxVal == a:
        print("Answer is " + answers[0] + confidence(a))
    elif maxVal == b:
        print("Answer is " + answers[1] + confidence(b))
    else:
        print("Answer is " + answers[2] + confidence(c))
        
print();

# Google custom search function
def google_search(question, answer):
    service = build("customsearch", "v1", developerKey=dev_key)
    res = service.cse().list(q=question, cx=my_cse_id, exactTerms=answer.lower(), fields='searchInformation').execute()
    return res['searchInformation']

# Queries are run in parallel using joblib
results = Parallel(n_jobs=4)(delayed(google_search)(question,answer) for answer in answers)

a = int(results[0]['totalResults'])
b = int(results[1]['totalResults'])
c = int(results[2]['totalResults'])

maxVal = max(a,b,c)

total = a + b + c
if total == 0: total = 1

print("Number of Results:");

if a == b and b == c:
    print("----NO RESULT----")
    
elif notFlag:

    minVal = min(a,b,c)
    
    if minVal == a:
        print("Answer is " + answers[0] + confidence(a))
    elif minVal == b:
        print("Answer is " + answers[1] + confidence(b))
    else:
        print("Answer is " + answers[2] + confidence(c))
else:
    
    if maxVal == a:
        print("Answer is " + answers[0] + confidence(a))
    elif maxVal == b:
        print("Answer is " + answers[1] + confidence(b))
    else:
        print("Answer is " + answers[2] + confidence(c))

print();

# r = "dogs are cool goggy thing dog my doggo"
# count = r.count("dog")
# print(str(count))

#TO DO: use inflect lib for punctuation.

# Identify Enitities using Google NLP, then search for entities in Wikipedia
# Classify question and use solvers (Wiki, IMDb, Google, Number of results, Bing)
# Remember to extract entities with High salience and search for them in wiki pages.

# If question contains NOT or NEVER, pick LEAST matching result.
# Least/most, smallest/largest

# If there is a tie in confidence, go with Google Search (provide an overall confidence later)
# exact terms search and count occurence (match words in any order using regex)
# Autocorrect misspelled words. (Hunspell)
