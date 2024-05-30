from openai import OpenAI
import config
import soundfile as sf
import io
import time
import os
import sounddevice as sd
import logging
from RealtimeTTS import TextToAudioStream, OpenAIEngine, SystemEngine

class BrocasArea:
    def __init__(self, output_device_index=0):
        os.environ['OPENAI_API_KEY'] = config.PROJECT_CONFIG['OPENAI_API_KEY']
        self.client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])
        self.engine = OpenAIEngine(voice='alloy', sample_rate=20500)
        self.tts = TextToAudioStream(self.engine, output_device_index=output_device_index, level=logging.DEBUG)

    def speak(self, text_stream):
        self.tts.feed(text_stream)
        self.tts.play()
