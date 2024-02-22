import google.generativeai as genai
from config import gemini_api_key

class GeminiChat:
    def __init__(self):
        genai.configure(api_key=gemini_api_key)  # Use API key from config

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

    def start_chat(self):
        self.convo = self.model.start_chat(history=[])

    def send_message(self, message):
        self.convo.send_message(message)

    def get_last_response(self):
        # Access the parts directly from the last response
        if hasattr(self.convo.last, 'parts'):
            return " ".join(part.text for part in self.convo.last.parts if part.text)
        else:
            return "Response parsing error: 'parts' attribute not found."

    def get_idea(self):
        '''Generate an idea using Gemini.'''
        self.send_message("Generate a project idea involving AI and web development. Make this idea direct another AI agent into starting a script coding session, give them step by step guidance. include text-based flowchart, how you want it structured in python and what libraries to use. Only send 1 idea with this structure.")
        response = self.get_last_response()
        return response
