import google.generativeai as genai
from config import gemini_api_key
import logging

class GeminiChat:
    def __init__(self, model_name="gemini-1.0-pro", generation_config=None, safety_settings=None):
        genai.configure(api_key=gemini_api_key)  # Use API key from config
        
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        } if generation_config is None else generation_config

        self.safety_settings = [
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
        ] if safety_settings is None else safety_settings

        self.model = genai.GenerativeModel(model_name=model_name,
                                           generation_config=self.generation_config,
                                           safety_settings=self.safety_settings)

    def start_chat(self):
        try:
            self.convo = self.model.start_chat(history=[])
        except Exception as e:
            logging.error(f"Failed to start chat: {e}")
            return "Chat start failure."

    def send_message(self, message):
        try:
            self.convo.send_message(message)
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            return "Message sending failure."

    def get_last_response(self):
        try:
            if hasattr(self.convo.last, 'parts'):
                return " ".join(part.text for part in self.convo.last.parts if part.text)
            else:
                return "Response parsing error: 'parts' attribute not found."
        except Exception as e:
            logging.error(f"Error retrieving last response: {e}")
            return "Error retrieving response."

    def get_idea(self):
        self.send_message("Generate a project idea involving AI and web development...")
        response = self.get_last_response()
        return response
