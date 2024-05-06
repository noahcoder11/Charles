import speech_recognition as sr
import ssl
import config
import soundfile as sf
import sounddevice as sd
from openai import OpenAI
ssl._create_default_https_context = ssl._create_unverified_context

class WernickesArea:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])

    def get_recognized_text(self):
        text = ''

        with sr.Microphone() as source:
            print("Listening...")
            
            audio = self.recognizer.listen(source)
            try:

                with open('audio.wav', 'wb') as f:
                    f.write(audio.get_wav_data())
                
                with open('audio.wav', 'rb') as f:
                    transcription = self.client.audio.transcriptions.create(
                        model='whisper-1',
                        file=f
                    )
                    text = transcription.text
            except:
                raise Exception("Could not recognize audio")
            
        return text