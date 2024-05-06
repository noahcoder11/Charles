from modules.wakeword import Wakeword
from modules.audio import Audio

wakeword_detector = Wakeword()
audio = Audio(wakeword_detector.porcupine.sample_rate, wakeword_detector.porcupine.frame_length)
audio.create_stream()

while(True):
    frame = audio.get_next_frame()

    if(wakeword_detector.process(frame)):
       print("Wakeword Detected")
       break

wakeword_detector.cleanup()
