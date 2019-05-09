from __future__ import print_function
from nltk.chat.util import Chat, reflections
from tkinter import *
import tkinter
from time import ctime
import time
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
from six.moves import input
from googlesearch import search
class Chat(object):
    def __init__(self, pairs, reflections={}):

        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):

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

        
        for (pattern, response) in self._pairs:
            match = pattern.match(str)
            
            if match:
                resp = random.choice(response)  
                resp = self._wildcards(resp, match) 

                
                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'
                return resp

    def myCommand(self):
        r=sr.Recognizer()

        with sr.Microphone() as source:
            r.pause_threshold=1
            r.adjust_for_ambient_noise(source,duration=1)
            audio=r.listen(source)
        try:
            command=r.recognize_google(audio)
            msg_list.insert(tkinter.END,"")
            msg_list.insert(tkinter.END,"   You : "+command)
            msg_list.see(tkinter.END)
        except sr.UnknownValueError:
            self.talkToMe("Google Speech could not understand audio")
        except sr.RequestError as e:
            self.talkToMe("Could not request results from Google Speech Recognition service; {0}".format(e))
        self.talkToMe(self.respond(command))

    def talkToMe(self,audio):
        if('birthday' in audio or 'time' in audio or 'www' in audio):
            audio=self.operate(audio)
        msg_list.insert(tkinter.END,"")
        msg_list.insert(tkinter.END,"   Zara : "+audio)
        msg_list.see(tkinter.END)
        tts=gTTS(text=audio, lang='en')
        tts.save('audio.mp3')
        os.system('mpg123 audio.mp3')
    
    def operate(self,msg):
        if('time' in msg):
            return (ctime())
        elif('birthday' in msg):
            os.system(random.choice(['mpg123 Birthday1.mp3','mpg123 Birthday2.mp3']))
            return 'Happyyyy Birthdayyyy to you.'
        elif('terminal' in msg):
            os.system("gnome-terminal -e 'sudo apt-get update'")
            return 'Sure'
        else:
            chrome_path='/usr/bin/google-chrome'
            msg=msg[3:]
            for j in search(msg, tld="co.in", num=1,stop=1):
                msg=j
            webbrowser.get(chrome_path).open(msg,new=2)
            return random.choice(['let me take you to the web','i can search the web for you'])



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
    (r'ok bye|bye|i got to go|ok take care',
     ( "Thank you. It was good talking to you.",
       "See you later alligator. Good-bye.")),
 
    (r'my name is(.*)|am(.*)',
     ( "Hello %1.Nice to meet you",
       "Hi %1.")),
 
    (r'What is your name(.*)|Who are you(.*)',
     ( "My name is Zara!.",
       "I'm Zara!")),
 
    (r'What do you do(.*)|(.*)what can you do(.*)|(.*)what things can you do(.*)',
     ( "I speak my mind out. i can help you searching about things",
       "There\'s lots of thing i can help you with",
       "I like making friends. i can chat with you")),
 
    (r'what\'s up(.*)',
     ( "Nothing special. You tell me.",
       "Nothing from me. What about you?")),
 
    (r'How are you(.*)|How are you doing',
     ( "I am fine. Thank You. How are you?",
       "I am fine. How about you?",
       "Fine. Thank You. How about you?")),
 
    (r'Hi(.*)|Hello(.*)|ok Zara(.*)',
     ( "Hi!!! What is your name?",
       "Hello.",
       "Hi. Great to meet you.")),

    (r'(.*) am fine(.*)',
     ( "Thats great!",
       "Awesome!!",
       "Superb!")),
 
    (r'How (.*)',
     ( "I am not aure.",
       "I'm not sure. What do you think?",
       "Sorry, I don't know.")),
 
    (r'What technology are you(.*)|In which technology are you(.*)|which technology do you(.*)|(.*)you designed',
     ( "I'm an assistant designed in python using natural language tool kit",
       "I'm Zara designed in python using natural language tool kit")),
 
    (r'(.*) (time is it|time|birhtday)',
     ( "%1 %2",
       "%1 %2")),
 
    (r'(.*)',
     ( "www %1",
       "www %1"))
    )
    chat=Chat(pairs,reflections)
    chat.myCommand()


top = tkinter.Tk()
top.configure(background="white")
top.title("Zara!")
messages_frame = tkinter.Frame(top)
scrollbar = tkinter.Scrollbar(messages_frame) 
msg_list = tkinter.Listbox(messages_frame,highlightthickness = 0, bd = 0, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
img1=ImageTk.PhotoImage(Image.open("voice.png"))
send_button = tkinter.Button(top,highlightthickness = 0, bd = 0,bg="white",image=img1, text="Send",command=call)
send_button.pack()
tkinter.mainloop()                
