import pvporcupine
import config

class Wakeword:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=config.PROJECT_CONFIG['PORCUPINE_ACCESS_KEY'],
            keyword_paths=[config.PROJECT_CONFIG['PORCUPINE_WAKEWORD_FILE_PATH']]
        )
    
    def process(self, audio_frame):
        keyword_index = self.porcupine.process(audio_frame)

        return keyword_index >= 0
    
    def cleanup(self):
        self.porcupine.delete()
