import speech_recognition as sr
import ssl
import config
import soundfile as sf
import sounddevice as sd
from playsounds import playsound
from openai import OpenAI
from .logging import Logger
ssl._create_default_https_context = ssl._create_unverified_context

logger = Logger(code = 'CHARLES')

class WernickesArea:
    def __init__(self, input_device_index=0, output_device_index=0):
        self.recognizer = sr.Recognizer()
        #self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = False
        #self.source = sr.Microphone(input_device_index)
        self.input_device_index = input_device_index
        self.output_device_index = output_device_index
        self.client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])

    def get_recognized_text(self):
        text = ''
        with sr.Microphone(self.input_device_index) as source:
            playsound('./sounds/Charles_Alert.wav', self.output_device_index)
            
            #self.recognizer.adjust_for_ambient_noise(source=source)
            audio = self.recognizer.listen(source)

            playsound('./sounds/Charles_end.wav', self.output_device_index)

            try:
                text = self.recognizer.recognize_whisper_api(audio, api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])
                logger.log('Recognized text: ' + text)
            except:
                raise Exception("Could not recognize audio")
            
        return text
    
    def __del__(self):
        self.client.__exit__(None, None, None)
        del self.recognizer