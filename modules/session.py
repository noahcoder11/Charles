from .openai_init import oai_client
from .generator import AISessionEventHandler
import threading
import queue

class Session:
    def __init__(self):
        self.thread = oai_client.beta.threads.create()
        self.thread_id = self.thread.id
        self.assistant_id = 'asst_bKmXRGMkucFOGxnssZ95o1pG'

    def add_message(self, message_data):
        oai_client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role='user',
            content=message_data
        )

    def add_text(self, text):
        self.add_message([{
            'type': 'text',
            'text': text
        }])

    def run_thread(self, event_handler: AISessionEventHandler):
        with oai_client.beta.threads.runs.stream(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            event_handler=event_handler
        ) as stream:
            stream.until_done()
            """if 'delta' in event.data:
                print('STREAM_DATA: ', event.data.delta.content[0].text.value)
                yield event.data.delta.content[0].text.value"""
        event_handler.finished.wait()
        
            
    def get_text_stream(self):
        handler = AISessionEventHandler()

        threading.Thread(target=self.run_thread, args=(handler,)).start()

        while not handler.finished.is_set() or not handler.queue.empty():
            try:
                piece = handler.queue.get()
                if piece is None:
                    break
                yield piece
            except queue.Empty:
                continue