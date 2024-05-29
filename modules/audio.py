import pyaudio
import struct

class Audio:
    def __init__(self, sample_rate, frame_length):
        self.py_audio = pyaudio.PyAudio()
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.device = self._find_available_device()

    def create_stream(self):
        self.audio_stream = self.py_audio.open(rate=self.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=self.frame_length, input_device_index=self.device)
    
    def get_next_frame(self):
        pcm = self.audio_stream.read(self.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * self.frame_length, pcm)

        return pcm
    
    def _find_available_device(self):
        for i in range(self.py_audio.get_device_count()):
            dev = self.py_audio.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                return i
        
        raise Exception('No available audio device found')