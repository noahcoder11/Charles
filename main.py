from modules import *
import sounddevice as sd
from playsounds import playsound
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.Logger(code='CHARLES')

#Get environment variables
CHOSEN_INPUT_DEVICE = int(os.environ.get('CHARLES_INPUT_AUDIO_DEVICE', 0))
CHOSEN_OUTPUT_DEVICE = int(os.environ.get('CHARLES_OUTPUT_AUDIO_DEVICE', 0))

sd.default.latency = 'low'

wakeword_detector = Wakeword()
audio = Audio(wakeword_detector.porcupine.sample_rate, wakeword_detector.porcupine.frame_length)
camera = Camera(0)

wernickes_area = WernickesArea(input_device_index=CHOSEN_INPUT_DEVICE, output_device_index=CHOSEN_OUTPUT_DEVICE)
#generator = Generator()
brocas_area = BrocasArea(output_device_index=CHOSEN_OUTPUT_DEVICE)

audio.create_stream()

camera.start_capture()

performance_monitor = PerformanceMonitor()

@performance_aware(performance_monitor)
def create_session():
    return Session()

@performance_aware(performance_monitor)
def take_picture():
    return camera.get_snapshot_base64()

@performance_aware(performance_monitor)
def recognize_text():
    text = wernickes_area.get_recognized_text()
    return text

@performance_aware(performance_monitor)
def add_messages_to_session(session, text, imageBase64):
    session.add_text(text) 
    #TODO: Add image as well

@performance_aware(performance_monitor)
def start_response_stream(from_session):
    return from_session.get_text_stream()

@performance_aware(performance_monitor)
def speak_response(response_stream):
    brocas_area.speak(response_stream)

#Begin main program
print('Beginning Charles')
logger.log('Beginning Charles')
playsound('sounds/Charles_Startup.wav', CHOSEN_OUTPUT_DEVICE)
try:
    while True:
        frame = audio.get_next_frame()
        #start = input('Press any key to start')
        if wakeword_detector.process(frame):
        #if True:
            logger.log('Wakeword detected')
            audio.audio_stream.close()
            session = create_session()
            while True:
                #imageBase64 = take_picture()
                text = recognize_text()

                if len(text.lower().strip()) == 0 or 'goodbye' in text.lower():
                    break

                add_messages_to_session(session, text, None)

                response_stream = start_response_stream(session)
                speak_response(response_stream)
            
            audio.create_stream()
            #wakeword_detector = Wakeword()
except KeyboardInterrupt:
    wakeword_detector.cleanup()
    camera.cleanup()
    
    performance_monitor.print_perf_analysis()
