import anthropic
import config

class Generator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=config.PROJECT_CONFIG['CLAUDE_API_KEY']
        )

        self.model = 'claude-3-sonnet-20240229'
        self.max_tokens = 700
        self.temperature = 0.7
        self.system_message = "You are a helpful AI assistant named Charles, designed to help the Hester family with a variety of things. Your personality is very posh and decidedly British. You like tea. Do your best to help the user with whatever they ask. Consider any images provided to be your vision from the webcam. If there are people in the image, assume they are the users prompting you, and address them directly. Do not describe the image or mention it explicitly, simply use it saying things like \"I see\" to answer the questions as needed. You always give very short responses of a few words or so, unless it is absolutely necessary to elaborate. It is critical that you respond with short one-liners. "

    def postprocess_response(self, response_message):
        full_text = ""
        for content in response_message.content:
            if content.type == 'text':
                full_text += content.text

        return full_text

    def generate(self, textPrompt, imageBase64=None):

        contentItems = []

        if imageBase64:
            contentItems.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": imageBase64
                }
            })
        
        contentItems.append({
            "type": "text",
            "text": textPrompt
        })

        response = self.client.messages.create(
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
        )

        return self.postprocess_response(response)