from openai import OpenAI
import config
import soundfile as sf
import io
import sounddevice as sd

class BrocasArea:
    def __init__(self):
        self.client = OpenAI(api_key=config.PROJECT_CONFIG['OPENAI_API_KEY'])

    def speak(self, text):
        with self.client.audio.speech.with_streaming_response.create(
            model='tts-1',
            voice='onyx',
            response_format='mp3',
            input=text
        ) as audio:
            audio.stream_to_file('speech.mp3')
            data, fs = sf.read('speech.mp3')
            sd.play(data, fs)
            sd.wait()