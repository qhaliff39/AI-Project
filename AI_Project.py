import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import json
import requests
import wolframalpha
from urllib.request import urlopen
import time 
import Trading212
from Trading212 import Invest
from selenium import webdriver
import random

wolfram_id ='your_own'
engine = pyttsx3.init()
engine.setProperty('rate',150)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def stock(name):
    trading = Invest('email',password='password',panel='Panel.Real')
    traderes = str(trading.position_info(stock=name,info='ppl positive'))
    speak(traderes)

def time_():
    Time = datetime.datetime.now().strftime('%H:%M:%S')
    speak('The current time is')
    speak(Time)

def date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    speak('The current date is')
    speak(day)
    speak(month)
    speak(year)

def wishme():
    speak('Welcome back Qhaliff')

    hour = datetime.datetime.now().hour

    if hour>=6 and hour<12:
        speak('Good Morning Sir!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon Sir!')
    elif hour>=18 and hour<24:
        speak('Good Evening Sir')
    else:
        speak('Good Night!')
    speak('I am at your service, how can I help you?')

def sendemail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()

    server.login('email','password')
    server.sendmail('email',to,content)
    server.close()

def cpu():
    usage = str(psutil.cpu_percent())
    speak('Current cpu usage is')
    speak(usage)

    battery = str(psutil.sensors_battery())
    speak('Battery is at')
    speak(battery)

def jokes():
    speak(pyjokes.get_jokes(language='en'))

def screenshot():
    speak('Taking screenshot')
    img = pyautogui.screenshot()
    speak('What do you want me to save this as?')
    name = TakeCommand()
    img.save('path'+name+'.png')


def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening..')
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)
        
    try:
        query = r.recognize_google(audio,language='en-US')

    except Exception as e:
        print(e)
        print('Say that again please..')
        return 'None'
    return query


WAKE = 'apple'
greetings = ['Hi, what can I do for you?','I am at your service','What"s up?','How can I help you']

if __name__ == '__main__':

    while True:
            query =TakeCommand()
            print(query)

            while query.count(WAKE)>0:
                speak(random.choices(greetings))
                query = TakeCommand()

                if 'time' in query:
                    time_()
        
                elif 'date' in query:
                    date()

                elif 'wikipedia' in query:
                    query = query.replace('wikipedia','')
                    speak('Searching')
                    result = wikipedia.summary(query,sentences=4)
                    speak('According to wikipedia')
                    speak(result)
                    print(result)

                elif 'send email' in query:
                    try:
                        speak('What should I say?')
                        content = TakeCommand()
                        speak('Who is the receiver')
                        receiver = input('Enter receiver email: ')
                        sendemail(receiver,content)
                        speak(content)
                        speak('Email has been delivered')
                    except Exception as e:
                        print(e)
                        print('Unable to send email')

                elif 'search in chrome' in query:
                    try:
                        speak('What should I search?')
                        chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
                        search = TakeCommand().lower()
                        wb.get(chromepath).open_new_tab(search+'.com')
                    except Exception as e:
                        print(e)
                        print('Unable to open website')
                elif 'search in youtube' in query:
                    try:
                        speak('What should I search?')
                        search_term = TakeCommand().lower()
                        speak('Here we go to youtube!')
                        wb.open('https://www.youtube.com/results?search_query='+search_term)
                    except Exception as e:
                        print(e)
                        print('Unable to open youtube')

                elif 'search in google' in query:
                    try:
                        speak('What should I search?')
                        search_term= TakeCommand().lower()
                        speak('Searching')
                        wb.open('https://www.google.com/search?q='+search_term)
                    except Exception as e:
                        print(e)
                        print('Unable to open google')
                elif 'cpu' in query:
                    cpu()

                elif 'jokes' in query:
                    jokes()

                elif 'goodbye' in query:
                    speak('Goodbye Sir!')
                    quit()

                elif 'word' in query:
                    speak('Opening MS Word')
                    ms_word = r'C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.exe'
                    os.startfile(ms_word)

                elif 'write a note' in query:
                    speak('What should I write sir?')
                    notes= TakeCommand()
                    file = open('notes.txt','w')
                    speak('Should I include the time and date?')
                    respond= TakeCommand()

                    if 'yes' in respond:
                        strtime = datetime.datetime.now().strftime('%H:%M:%S')
                        file.write(strtime)
                        file.write(':-')
                        file.write(notes)
                        speak('Done taking notes')
                    else:
                        file.write(notes)

                elif 'show notes' in query:
                    speak('showing notes')
                    file = open('notes.txt','r')
                    speak(file)
                    print(file)

                elif 'screenshot' in query:
                    screenshot()

                elif 'news' in query:
                    try:
                        jsonobj = urlopen('http://newsapi.org/v2/everything?domains=wsj.com&apiKey='+'your_api')
                        data = json.load(jsonobj)
                        i=1
                        speak('Here are some articles from the Wall Street Journal')
                        print('===Articles===\n')
                        for item in data['articles']:
                            print(str(i)+'.'+item['title']+'\n')
                            print(item['description']+'\n')
                            speak(item['title'])
                            i += 1

                            if i==10:
                                speak('10 news articles for today')
                                break
                    except Exception as e:
                        print(str(e))

                elif 'where is' in query:
                     query = query.replace('where is','')
                     speak('Locating '+query)
                     wb.open_new_tab('https://www.google.com/maps/place/'+query)

                elif 'calculate' in query:
                    client = wolframalpha.Client(wolfram_id)
                    indx = query.lower().split().index('calculate')
                    query = query.split()[indx + 1:]
                    res = client.query(''.join(query))
                    answer = next(res.results).text
                    print('The answer is '+answer)
                    speak('The answer is'+answer)

                elif 'what is' in query or 'who is' in query:

                    client = wolframalpha.Client(wolfram_id)
                    res = client.query(query)

                    try:
                        print(next(res.results).text)
                        speak(next(res.results).text)
                    except StopIteration:
                        print('No Results')
             
                elif 'stop listening' in query:
                    speak('How long do you want me to stop listening')
                    answer = int(TakeCommand())
                    time.sleep(answer)

                elif 'log out' in query:
                    os.system('shutdown -1')

                elif 'restart' in query:
                    os.system('shutdown /r /t -1')

                elif 'shutdown' in query:
                    os.system('shutdown /s /t 1')

                elif 'stocks' in query:
                    speak('Which stocks in your portfolio do you want me to search for?')
                    query = TakeCommand()
                    speak('Please wait a moment for me to retrieve your stocks details')
                    stock(query.capitalize())

                elif 'thank you' in query:
                    speak('You are welcome')
                    break








