# pip install pyaudio
# pip install SpeechRecognition

import speech_recognition as sr

def speech_txt():
    r=sr.Recognizer() #class
    while True:
        with sr.Microphone() as source:    #Source=sr.Mircophone
            print("Speak.................")
            audio=r.listen(source)
        
        try:
            text=r.recognize_google(audio)
            print("You said",text)
        except:
            print("Did not hear anything. Please repeat")
                
speech_txt()