from openai import OpenAI
import logging
from config import model, idea_prompt, code_prompt, idea_system, code_system, feedback_system, feedback_user, ft3, gpt3
import re
from code_executer import CodeExecutor
from gemini_chat import GeminiChat


# Initialize Gemini Chat
chat = GeminiChat()
chat.start_chat()

class ConversationManager:
    '''
    Manages the conversation and development process with OpenAI and Gemini,
    aligning with the updated flow focusing on testing only valid code during
    iterative refinement and not during initial idea generations.
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
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content

    def iterate_development(self):
        logging.info("Generating project idea...")
        self.project_idea = chat.get_idea()
        logging.info(f"Project Idea: {self.project_idea}")
        print(f"Project Idea: {self.project_idea}")
        initial_prompt = f"{idea_prompt}\n\n{self.project_idea}"
        logging.info("Generating initial project code...")
        self.project_code = self.generate_response(model, initial_prompt, idea_system)
        logging.info(f"Initial Project Code: {self.project_code}")

        iteration = 0
        while True:
            logging.info(f"Validating code - Iteration {iteration}...")
            if CodeExecutor.is_valid_code(self.project_code):
                logging.info("Executing code...")
                print("Executing code...")
                execution_result = CodeExecutor.execute_python_code(self.project_code)
                logging.info(f"Execution Result: {execution_result}")
                print(execution_result)
                feedback_prompt = f"{feedback_user}\n\nCode:\n{self.project_code}\n\nExecution Result:\n{execution_result}{initial_prompt}"
                logging.info("Generating feedback...")
                print("Generating feedback...")
                feedback = self.generate_response(model, feedback_prompt, feedback_system)
                logging.info(f"Feedback: {feedback}")
                print(feedback)

                if "yes" in feedback.lower():
                    logging.info("Project complete and potentially profitable.")
                    print("Project complete and potentially profitable.")
                    break
                else:
                    refinement_prompt = f"Refine code based on feedback:\n\nFeedback:\n{feedback}\n\nCurrent Code:\n{self.project_code}"+self.project_code+self.project_idea
                    logging.info("Refining code based on feedback...")
                    print("Refining code based on feedback...")
                    self.project_code = self.generate_response(model, refinement_prompt, "Refining code...")
                    iteration += 1
            else:
                logging.info("Code is not valid for execution. Refinement needed.")
                print("Code is not valid for execution. Refinement needed.")
                break

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

