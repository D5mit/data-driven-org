
import pyttsx3
engine = pyttsx3.init()

def test_spelling(inword):

    engine.say("Please type in the word,")
    engine.runAndWait()

    engine.say(inword)
    engine.runAndWait()

    input1 = input('Question 1: ')

    if input1 == inword:
        engine.say("this is correct")
        engine.runAndWait()
    else:
        engine.say("this is incorrect")
        engine.runAndWait()

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say("Hello, welcome to this spelling test.")
engine.runAndWait()

engine.say("Question 1.")
engine.runAndWait()

test_spelling('with')


