from RealtimeTTS import TextToAudioStream, OpenAIEngine, SystemEngine
import sounddevice as sd
print(sd.query_devices())
tts = TextToAudioStream(SystemEngine())
tts.feed('Testing this')
tts.play()