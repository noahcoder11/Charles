from modules import *
import sounddevice as sd
from playsounds import playsound, perform_audio_output_setup


sd.default.latency = 'low'

#wakeword_detector = Wakeword()
#audio = Audio(wakeword_detector.porcupine.sample_rate, wakeword_detector.porcupine.frame_length)
camera = Camera(0)

wernickes_area = WernickesArea()
#generator = Generator()
brocas_area = BrocasArea()

#audio.create_stream()

camera.start_capture()

print(sd.query_devices())

performance_monitor = PerformanceMonitor()

class ProgramState:
    def __init__(self):
        self.session = None
        self.imageBase64 = None
        self.recognized_text = None
        self.response = None
        self.response_stream = None

    def reset(self):
        self.imageBase64 = None
        self.recognized_text = None
        self.response = None
        self.response_stream = None

@performance_aware(performance_monitor)
def create_session():
    return Session()

@performance_aware(performance_monitor)
def take_picture():
    return camera.get_snapshot_base64()

@performance_aware(performance_monitor)
def recognize_text():
    print('Recognizing')
    text = wernickes_area.get_recognized_text()
    print('Recognized:', text)
    return text

@performance_aware(performance_monitor)
def add_messages_to_session(session, text, imageBase64):
    print('Adding message')
    session.add_text(text) 
    #TODO: Add image as well

@performance_aware(performance_monitor)
def start_response_stream(from_session):
    print('Fetching response')
    return from_session.get_text_stream()

@performance_aware(performance_monitor)
def speak_response(response_stream):
    print('Speaking response')
    brocas_area.speak(response_stream)

#Begin main program
print("Beginning main loop")

perform_audio_output_setup()

playsound('sounds/Charles_Startup.wav')
print('Finished Playing sound')
try:
    while True:
        #frame = audio.get_next_frame()
        start = input('Press any key to start')
        #if wakeword_detector.process(frame):
        if True:
            #wakeword_detector.cleanup()
            session = create_session()
            while True:
                print('Prompting again')

                imageBase64 = take_picture()
                text = recognize_text()
                add_messages_to_session(session, text, imageBase64)

                response_stream = start_response_stream(session)
                speak_response(response_stream)

                print("\n\n")

            #wakeword_detector = Wakeword()
except KeyboardInterrupt:
    print('Closing program...')
    #wakeword_detector.cleanup()
    camera.cleanup()
    
    performance_monitor.print_perf_analysis()
