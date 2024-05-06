import speech_recognition as sr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()


    def get_recognized_text(self):
        text = ''

        with sr.Microphone() as source:
            print("Listening...")
            print(source.list_microphone_names())
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
            try:
                text = self.recognizer.recognize_whisper(audio)
            except:
                raise Exception("Could not recognize audio")
            
        return text