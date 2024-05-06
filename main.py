from modules import *

wakeword_detector = Wakeword()
audio = Audio(wakeword_detector.porcupine.sample_rate, wakeword_detector.porcupine.frame_length)
camera = Camera(0)
wernickes_area = WernickesArea()
generator = Generator()
brocas_area = BrocasArea()

audio.create_stream()

camera.start_capture()

while True:
    frame = audio.get_next_frame()

    if wakeword_detector.process(frame):
        print("Wakeword Detected")
        
        #Take a picture
        imageBase64 = camera.get_snapshot_base64()

        print('Picture taken')

        #Now do speech recognition
        recognized_text = wernickes_area.get_recognized_text()

        print('Recognized text:', recognized_text)

        #Now generate a response
        response = generator.generate(recognized_text, imageBase64)

        print('Response:', response)

        print('Speaking')

        #Now speak the response
        brocas_area.speak(response)



wakeword_detector.cleanup()
camera.cleanup()
