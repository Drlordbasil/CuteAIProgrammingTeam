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
        logging.info(f"Project Idea: {project_idea}")

        # Improved prompting with detailed context for the AI
        initial_prompt = (
            f"Project Idea: {project_idea}\n\n"
            "Based on the above project idea, generate the initial Python code. "
            "The code should be robust, well-structured, and include error handling. "
            "Consider best practices for code efficiency and maintainability."
        )
        system_message = (
            "Your task is to translate the project idea into an initial Python script. "
            "Focus on creating a foundation that is scalable, maintainable, and efficient. "
            "Remember to include comments explaining your logic where necessary."
        )
        logging.info("Generating initial project code...")
        self.project_code = self.generate_response(model, initial_prompt, system_message)

        iteration = 0
        while iteration < 10:  # Limit iterations to prevent infinite loops
            logging.info(f"Validating code - Iteration {iteration}...")
            if CodeExecutor.is_valid_code(self.project_code):
                execution_result = CodeExecutor.execute_python_code(self.project_code)
                logging.info(f"Execution Result: {execution_result}")

                # Dynamically adapt the prompt based on execution results and iteration state
                feedback_prompt = (
                    f"Iteration {iteration}. Based on the execution results below, refine the project code to "
                    f"improve functionality, efficiency, or resolve any errors identified:\n\n"
                    f"Execution Result:\n{execution_result}\n\n"
                    f"Original Project Idea:\n{self.project_idea}\n\n"
                    "Please refine the code accordingly."
                )
                system_message = (
                    "Review the execution result and the original project idea. "
                    "Provide actionable feedback or modifications to the existing code to enhance its quality, "
                    "considering best practices and the aim of achieving a satisfactory project outcome."
                )
                logging.info("Generating feedback...")
                feedback = self.generate_response(model, feedback_prompt, system_message)

                if "satisfactory" in feedback.lower():
                    logging.info("Project complete and potentially profitable.")
                    break
                else:
                    self.project_code = self.generate_response(model, feedback, feedback_user)
            else:
                logging.info("Code is not valid. Refining...")
                system_message_for_refinement = (
                    "The submitted code has been evaluated and found to contain errors or inefficiencies. "
                    "Your task is to refine the code to address these issues, ensuring it aligns with best practices for Python programming. "
                    "Focus on improving code structure, error handling, and overall logic to meet the project requirements."
                )
                user_prompt_for_refinement = (
                    "Please refine the provided code, correcting any errors and improving its efficiency and maintainability. "
                    "Ensure the revised code adheres closely to the initial project idea and objectives."
                )
                self.project_code = self.generate_response(model, user_prompt_for_refinement, system_message_for_refinement)
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
