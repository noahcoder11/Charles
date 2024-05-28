import pyaudio
import wave

pyaudio_instance = pyaudio.PyAudio()

def playsound(sound_file, output_device_index=0):
    f = wave.open(sound_file, 'rb')
    out_stream = pyaudio_instance.open(format=pyaudio_instance.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True, output_device_index=output_device_index)
    
    data = f.readframes(1024)
    while data:
        out_stream.write(data)
        data = f.readframes(1024)
    f.close()
    out_stream.close()

