from openai import OpenAI
import config
import soundfile as sf
import io
import time
import os
import sounddevice as sd
from RealtimeTTS import TextToAudioStream, OpenAIEngine, SystemEngine

class BrocasArea:
    def __init__(self):
        os.environ['OPENAI_API_KEY'] = config.PROJECT_CONFIG['OPENAI_API_KEY']
        self.client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])
        self.engine = OpenAIEngine(voice='fable')
        self.tts = TextToAudioStream(self.engine)

    def speak(self, text_stream):
        print('Text Stream:', text_stream)

        text = ''

        self.tts.feed(text_stream)
        self.tts.play()

        print('Done Playing audio')