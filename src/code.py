from __future__ import print_function
from nltk.chat.util import Chat, reflections
from tkinter import *
import tkinter
import random
from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
import smtplib
from PIL import ImageTk, Image
import requests
from weather import Weather
import re
import random
from six.moves import input

class Chat(object):
    def __init__(self,pairs, reflections={}):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find('%')
        return response


    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'
                return resp


    # Hold a conversation with a chatbot

    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                print(self.respond(user_input))

    def myCommand(self):
        r=sr.Recognizer()

        with sr.Microphone() as source:
            r.pause_threshold=1
            r.adjust_for_ambient_noise(source,duration=1)
            audio=r.listen(source)
        try:
            command=r.recognize_google(audio)
            msg_list.insert(tkinter.END,"                                                       "+command)
            msg_list.see(tkinter.END)
        except sr.UnknownValueError:
            self.talkToMe('Sorry i did not get this')
        self.talkToMe(self.respond(command))

    def talkToMe(self,audio):
        msg_list.insert(tkinter.END,"   "+audio)
        msg_list.see(tkinter.END)
        tts=gTTS(text=audio, lang='en')
        tts.save('audio.mp3')
        os.system('mpg123 audio.mp3')

def call():
    reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i would": "you would",
    "i have": "you have",
    "i will": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you have": "I have",
    "you will": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
    }
    pairs = (
    (r'ok bye',
     ( "Thank you. It was good talking to you.",
       "Good-bye.")),
 
    (r'Who are you(.*)',
     ( "My name is Pyexa.",
       "I'm Pyexa.")),
 
    (r'What is your name(.*)',
     ( "My name is Alpha.",
       "I'm Alpha.")),
 
    (r'What do you do(.*)',
     ( "I speak my mind out.",
       "I chat.",
       "I like making friends.")),
 
    (r'Then(.*)',
     ( "Nothing special. You tell me.",
       "What else?",
       "Nothing from me. What about you?")),
 
    (r'How are you(.*)',
     ( "I am fine. Thank You. How are you?",
       "I am fine. How about you?",
       "Fine. Thank You. How about you?")),
 
    (r'Hi(.*)',
     ( "Hi!!! What is your name?",
       "Hello.",
       "Hi. Great to meet you.")),
 
    (r'My name is (.*)',
     ( "Hi %1!!!",
       "Hello %1.",
       "Hi %1. Great to meet you.")),
 
    (r'You tell me(.*)',
     ( "What?",
       "Tell me about yourself.",
       "WHat do you do?")),
 
    (r'What else(.*)',
     ( "Nothing special. You tell me.",
       "Nothing from me. What about you?")),
 
    (r'I need (.*)',
     ( "Why do you need %1?",
       "Why?",
       "Are you sure?")),
 
    (r'How (.*)',
     ( "I am not aure.",
       "I'm not sure. What do you think?",
       "Sorry, I don't know.")),
 
    (r'Hello(.*)',
     ( "Hi... How are you today?",
       "Hello, How are you?")),
 
    (r'Yes',
     ( "You seem certain.",
       "Alright")),
 
    (r'My (.*)',
     ( "I see, your %1.",
       "Oh ok.")),
 
    (r'(.*)\?',
     ( "Why do you ask that?",
       "I am not sure.",
       "I do not know the answer to your question")),
 
    (r'(.*) (happy|cheerful|glad|good)',
     ( "%1 %2",
       "%1 %2")),
 
    (r'(.*)',
     ( "Alright.",
       "I see.",
       "Very interesting."))
    )
    chat=Chat(pairs,reflections)
    chat.myCommand()


top = tkinter.Tk()
top.configure(background="white")
top.title("Lyra!")
messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
# this will contain the messages.
msg_list = tkinter.Listbox(messages_frame,highlightthickness = 0, bd = 0, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

img1=ImageTk.PhotoImage(Image.open("voice.png"))
send_button = tkinter.Button(top,highlightthickness = 0, bd = 0,bg="white",image=img1, text="Send",command=call)
send_button.pack()
tkinter.mainloop()                