# pip install pyttsx3
import pyttsx3
# class ==> init

txt_sp=pyttsx3.init()
text=input("Enter Text: ")
rate=txt_sp.getProperty('rate')
txt_sp.setProperty('rate',100)
voices = txt_sp.getProperty('voices')
txt_sp.setProperty('voice', voices[0].id)
txt_sp.say(text) 
txt_sp.runAndWait()