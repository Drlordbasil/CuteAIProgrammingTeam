import google.generativeai as genai

class GeminiChat:
    def __init__(self):
        genai.configure(api_key="AIzaSyCR-CmOHLN95nvl56M16Qm2T-DfNaNY05c")
        # Set up the model
        generation_config = {
            "temperature": 0.1,
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
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]

        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

    def start_chat(self):
        self.convo = self.model.start_chat(history=[])

    def send_message(self, message):
        self.convo.send_message(message)

    def get_last_response(self):
        print(self.convo.last.text)
        return self.convo.last.text
    

