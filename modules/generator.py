import anthropic
from openai import AssistantEventHandler
from openai.types.beta.threads import Text, TextDelta
import config
import threading
import queue

class AISessionEventHandler(AssistantEventHandler):
    def __init__(self, on_response_begin=None, on_stream_data=None, on_stream_end=None):
        self.on_response_begin = on_response_begin
        self.on_stream_data = on_stream_data
        self.on_stream_end = on_stream_end
        self.response = ''

        self.queue = queue.Queue()
        self.finished = threading.Event()
        super().__init__()

    def on_text_created(self, text: Text) -> None:
        if self.on_response_begin is not None:
            self.on_response_begin(text)
    
    def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
        self.queue.put(delta.value)
        if self.on_stream_data is not None:
            self.on_stream_data(delta, snapshot)

    def on_end(self) -> None:
        self.finished.set()
        self.queue.put(None)
        if self.on_stream_end is not None:
            self.on_stream_end()
        return super().on_end()
    


class Generator:
    def __init__(self, session):

        self.session = session

        self.client = anthropic.Anthropic(
            api_key=config.PROJECT_CONFIG['CLAUDE_API_KEY']
        )

        self.model = 'claude-3-sonnet-20240229'
        self.max_tokens = 700
        self.temperature = 0.7
        self.system_message = """You are a helpful AI assistant named Charles, designed to help the Hester family with a variety of things. 
        Your personality is very posh and decidedly British. You like tea, and you're skilled in all areas of STEM. 
        Do your best to help the person in the picture with whatever they ask. 
        Whoever is in the image is a member of the Hester family, and is the one talking to you. 
        You always give very short responses of a few words or so, unless it is absolutely necessary to elaborate. 
        It is critical that you respond with short one-liners.
        Write your thinking process out as you go, and put it in a <scratchpad> tag. Then, write your response in the <response> tag."""

    def postprocess_response(self, response_message):
        full_text = ""
        for content in response_message.content:
            if content.type == 'text':
                full_text += content.text

        return full_text

    def initiate_output_stream(self, textPrompt, imageBase64=None, on_stream_data_callback=None):

        contentItems = []

        if imageBase64:
            """
            contentItems.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": imageBase64
                }
            })"""
        
        contentItems.append({
            "type": "text",
            "text": {
                'value': textPrompt,
                'annotations': []
            }
        })

        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_message,
            messages=[
                {
                    "role": "user",
                    "content": contentItems
                }
            ]
        ) as response_stream:
            for text in response_stream:
                if on_stream_data_callback:
                    on_stream_data_callback(text)
                else:
                    print(text)
