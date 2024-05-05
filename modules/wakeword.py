import pvporcupine
import config

class Wakeword:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=config.PROJECT_CONFIG.PORCUPINE_ACCESS_KEY,
            keyword_paths=['~/Documents/Charles/Charles_en_raspberry-pi_v3_0_0.ppn']
        )
    
    def process(self, audio_frame):
        keyword_index = self.porcupine.process(audio_frame)

        return keyword_index >= 0
    
    def cleanup(self):
        self.porcupine.delete()
