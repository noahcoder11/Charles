import pyaudio
import struct

class Audio:
    def __init__(self, sample_rate, frame_length):
        self.py_audio = pyaudio.PyAudio()
        self.sample_rate = sample_rate
        self.frame_length = frame_length

    def create_stream(self):
        self.audio_stream = self.py_audio.open(rate=self.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=self.frame_length)
    
    def get_next_frame(self):
        pcm = self.audio_stream.read(self.frame_length)
        pcm = struct.unpack_from("h" * self.frame_length, pcm)

        return pcm