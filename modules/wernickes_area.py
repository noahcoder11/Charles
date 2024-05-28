import speech_recognition as sr
import ssl
import config
import soundfile as sf
import sounddevice as sd
from playsounds import playsound
from openai import OpenAI
ssl._create_default_https_context = ssl._create_unverified_context

class WernickesArea:
    def __init__(self, input_device_index=0, output_device_index=0):
        self.recognizer = sr.Recognizer()
        #self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = False
        self.source = sr.Microphone(input_device_index)
        self.output_device_index = output_device_index
        self.source.__enter__()
        self.client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])

    def get_recognized_text(self):
        text = ''
        print("Listening...")
        playsound('./sounds/Charles_Alert.wav', self.output_device_index)
        
        #self.recognizer.adjust_for_ambient_noise(source=source)
        audio = self.recognizer.listen(self.source)

        print('Audio captured')
        playsound('./sounds/Charles_end.wav', self.output_device_index)

        try:
            text = self.recognizer.recognize_whisper_api(audio, api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])
            
            print("Transcribed")
        except:
            raise Exception("Could not recognize audio")
            
        return text
    
    def __del__(self):
        self.source.__exit__(None, None, None)
        self.client.__exit__(None, None, None)
        del self.recognizer