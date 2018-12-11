# triviaBot
A bot designed to answer live trivia game questions. (**~2600/3000** answered correctly)

### What it does
The script is triggered by a screenshot of the question and possible answers (multiple choice). The bot then uses **Tesseract OCR** to convert the images into machine-encoded text. Finally, it uses different search techniques in parallel to find out the most popular/relevant answer available and returns it in less than 5 seconds, currently with an **85% average success rate**.

### How I built it
The frontend is a basic **Automator** script, while the backend is written in **Python 3**. Initially, I considered using **Google's Vision API** to OCR the screenshots of the question, however I realized that, with low internet speeds, I just couldn’t afford the RTT _(round trip time)_. Therefore, I went for Tesseract OCR, which was much faster as it was installed locally on my machine.

I run two techniques in parallel to quickly figure out the correct answer:
* Simply google the question and search for all the answers. This trick works most of the time, but can be thrown off by simple "Which of these..." questions.
* Count the overall search results. Every time you search something on google you see something like: _About 1,330,000,000 results (0.65 seconds)_. I google the question with all three answer choices appended to find the most popular answer.

Finally, I take all of the calculations and return a confidence score for each answer.

### Challenges faced
There were a plethora of challenges I experienced over the course of this project.
* Most importantly, accuracy. It took forever to find the right way to scrape Google to accurately calculate the correct answer.
* Also, speed. I had to run each query in parallel, to get the answer in just under 5 seconds.
* Finally, adjusting to different types of questions. Questions like "Which of these..." or "What is NOT..." were tough questions to solve. "Which of these" questions were more easily solved through my second technique of counting search hits. I found it easiest to solve, "NOT" questions, by actually removing the word "NOT" from the query and then picking the "worst" answer choice. It worked pretty well!



##### _Please note:_ it is against terms and conditions to use this bot during a live game show.
