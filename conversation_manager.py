from openai import OpenAI
import logging
from config import model, idea_prompt, code_prompt, idea_system, code_system, feedback_system, feedback_user, ft3, gpt3
import re
from code_executer import CodeExecutor
from gemini_chat import GeminiChat

# Initialize GeminiChat for conversation with Gemini+OpenAI integration
chat = GeminiChat()
chat.start_chat()

class ConversationManager:
    '''
    This class manages the conversation and development process, integrating OpenAI and Gemini for idea generation,
    code development, and iterative refinement. The flow includes:
    1. Idea generation with Gemini
    2. Development of the project with code suggestions from OpenAI
    3. Iterative refinement and feedback integration
    4. Code execution and testing
    5. Finalization of the project code
    6. Logging the development process
    '''
    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI()
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content

    def iterate_development(self):
        # Use Gemini for idea generation
        chat.send_message("I want to create a profitable project, give me a clear directive.")
        self.project_idea = chat.get_last_response()
        

        # Develop project code with OpenAI based on the idea from Gemini
        self.project_code = self.generate_response(ft3, code_prompt + f"{self.project_idea}", code_system)

        completion = "no"
        iteration = 0
        while completion == "no":
            clean_project_code = CodeExecutor.remove_comments_and_extract_code(self.project_code)
            CodeExecutor.save_code(clean_project_code, f"project_{iteration}.py")
            execution_result = CodeExecutor.execute_python_code(clean_project_code)

            # Get feedback on the code execution
            feedback = self.generate_response(gpt3, feedback_user + execution_result + clean_project_code, feedback_system)
            
            if "yes" in feedback.lower():
                completion = "yes"
                logging.info("Project deemed complete and potentially profitable.")
            else:
                # Refine the project code based on feedback, using both Gemini and OpenAI
                self.project_code = self.generate_response(model, f"Refine the Python code to ensure profitability and completion. {feedback} {self.project_code}", "Refining project code...")
                iteration += 1

    def conversation_thread(self):
        self.iterate_development()
        if self.project_code:
            logging.info("Final Project Code:\n" + self.project_code)
        else:
            logging.warning("Failed to develop a profitable project.")
        logging.info("Conversation and development process complete.")
