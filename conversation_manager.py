from openai import OpenAI
import logging
from config import model, feedback_system, feedback_user
import re
from code_executer import CodeExecutor
from gemini_chat import GeminiChat

# Improved initialization of GeminiChat
chat = GeminiChat()
chat.start_chat()

class ConversationManager:
    '''
    Manages the conversation and development process with OpenAI and Gemini,
    focusing on testing valid code during iterative refinement.
    '''

    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI()
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        '''
        Generate a response using the specified model type and prompt, with an optional system message.
        '''
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        try:
            response = self.client.chat.completions.create(model=model_type, messages=messages)
            content = response.choices[0].message.content
            logging.info(f"Response: {content}")
            return content
        except Exception as e:
            logging.error(f"Failed to generate response: {e}")
            return ""

    def iterate_development(self):
        logging.info("Generating project idea...")
        self.project_idea = chat.get_idea()
        project_idea = self.project_idea
        logging.info(f"Project Idea: {self.project_idea}")

        initial_prompt = f"{project_idea}\n\nGenerate initial project code with robust implementations."
        logging.info("Generating initial project code...")
        self.project_code = self.generate_response(model, initial_prompt, "Create a robust python script.")

        iteration = 0
        while iteration < 10:  # Limit iterations to prevent infinite loops
            logging.info(f"Validating code - Iteration {iteration}...")
            if CodeExecutor.is_valid_code(self.project_code):
                execution_result = CodeExecutor.execute_python_code(self.project_code)
                logging.info(f"Execution Result: {execution_result}")

                feedback_prompt = f"Refine based on execution result:\n{execution_result}\n\n{initial_prompt}"
                logging.info("Generating feedback...")
                feedback = self.generate_response(model, feedback_prompt, feedback_system)

                if "satisfactory" in feedback.lower():
                    logging.info("Project complete and potentially profitable.")
                    break
                else:
                    self.project_code = self.generate_response(model, feedback, feedback_user)
            else:
                logging.info("Code is not valid. Refining...")
                self.project_code = self.generate_response(model, "Refine invalid code.", feedback_user)
            iteration += 1

    def conversation_thread(self):
        '''
        Starts the conversation thread and logs the final project code or failure.
        '''
        self.iterate_development()
        if self.project_code:
            logging.info("Final Project Code:\n" + self.project_code)
        else:
            logging.warning("Failed to develop a profitable project.")
        logging.info("Conversation and development process complete.")
