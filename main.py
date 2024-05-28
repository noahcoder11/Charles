from modules import *
import sounddevice as sd
from playsounds import playsound

CHOSEN_INPUT_DEVICE = 0
CHOSEN_OUTPUT_DEVICE = 0

#First, we want to make sure we're selecting the right audio devices
print('Available audio devices:')
print(sd.query_devices())
print('\n')
print('Beginning output device selection:')
output_device_placeholder = 0
out_device_selected = False
while not out_device_selected:
    output_device_placeholder = int(input('Enter an output device index: '))
    while True:
        print('- Testing output device...', end='', flush=True)
        try:
            playsound('sounds/Charles_Startup.wav', output_device_placeholder)
            print('done')
        except Exception as e:
            print('\nError:', e)
            continue
        uinput = input('  -> Did you hear sound? [y/n, r=retry] ')
        if uinput.lower() == 'y':
            CHOSEN_OUTPUT_DEVICE = output_device_placeholder
            out_device_selected = True
            break
        elif uinput.lower() == 'r':
            continue
        else:
            print('- Canceling device selection')
            break

print('Beginning input device selection:')
CHOSEN_INPUT_DEVICE = int(input('Enter an input device index: '))
    


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

playsound('sounds/Charles_Startup.wav', CHOSEN_OUTPUT_DEVICE)
print('Finished Playing sound')
try:
    while True:
        frame = audio.get_next_frame()
        #start = input('Press any key to start')
        if wakeword_detector.process(frame):
        #if True:
            wakeword_detector.cleanup()
            session = create_session()
            while True:
                print('Prompting again')

                #imageBase64 = take_picture()
                text = recognize_text()
                add_messages_to_session(session, text, None)

                response_stream = start_response_stream(session)
                speak_response(response_stream)

                print("\n\n")

            wakeword_detector = Wakeword()
except KeyboardInterrupt:
    print('Closing program...')
    wakeword_detector.cleanup()
    camera.cleanup()
    
    performance_monitor.print_perf_analysis()
