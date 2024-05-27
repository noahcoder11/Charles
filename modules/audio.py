import pyaudio
from pvrecorder import PvRecorder
import struct

class Audio:
    def __init__(self, sample_rate, frame_length):
        self.frame_length = frame_length
        self.py_audio = pyaudio.PyAudio()
        self.device = self._find_available_device()
        self.recorder = PvRecorder(frame_length=frame_length, device_index=self.device)

    def create_stream(self):
        self.recorder.start()
    
    def get_next_frame(self):
        if self.recorder.is_recording:
            return self.recorder.read()
        raise Exception('Recorder is not recording')
    
    def _find_available_device(self):
        devices = PvRecorder.get_available_devices()
        for i in range(0, len(devices)):
            if devices[i].find('Scarlett'):
                return i
        
        raise Exception('No available audio device found')
    
    def cleanup(self):
        self.recorder.stop()
        self.recorder.delete()