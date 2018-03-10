#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import io
import os

# OCR using Tesseract
from PIL import Image
import pytesseract

# Custom Search
from googleapiclient.discovery import build

# Parallel requests
from joblib import Parallel, delayed 

my_cse_id = "017243323922835907384:7bywfbe83ve"
dev_key = "AIzaSyDpTXV69ahVIKhUUWtQ9p4gyO1TY_omTl8"

file_name = os.path.join(
    os.path.dirname(__file__),
    'question.png')

im = Image.open(file_name)

text = pytesseract.image_to_string(im, lang = 'eng')

text = text.replace("ﬁ", "fi")
textArr = text.split("\n")
arr = []

for s in textArr:
    if s != "":
        arr.append(s)
        
arrLen = len(arr)
question = ""
for index in range(arrLen - 3):
    question += arr[index] + " "

answers = [arr[arrLen - 3],arr[arrLen - 2],arr[arrLen - 1]]

print("Question: " + question + "\na) " + answers[0] + "\nb) " + answers[1] + "\nc) " + answers[2] + "\n")

# Google custom search function
def google_search(question, answer):
    service = build("customsearch", "v1", developerKey=dev_key)
    res = service.cse().list(q=question, cx=my_cse_id, exactTerms=answer, fields='searchInformation').execute()
    return res['searchInformation']

# Queries are run in parallel using joblib
results = Parallel(n_jobs=6)(delayed(google_search)(question.lower(),answer.lower()) for answer in answers)

total = 1 + int(results[0]['totalResults']) + int(results[1]['totalResults']) + int(results[2]['totalResults'])
max = max(int(results[0]['totalResults']),int(results[1]['totalResults']),int(results[2]['totalResults']))

if max == int(results[0]['totalResults']):
    print("Answer is " + answers[0] + "  (confidence: " + str(round((int(results[0]['totalResults'])/total)*100)) + "%)")
elif max == int(results[1]['totalResults']):
    print("Answer is " + answers[1] + "  (confidence: " + str(round((int(results[1]['totalResults'])/total)*100)) + "%)")
else:
    print("Answer is " + answers[2] + "  (confidence: " + str(round((int(results[2]['totalResults'])/total)*100)) + "%)")

print();
