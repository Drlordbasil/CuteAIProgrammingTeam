#conversation_manager.py
from openai import OpenAI
import logging
from config import model, idea_prompt, code_prompt, idea_system,code_system,feedback_system,feedback_user
import re
from code_executer import CodeExecutor


class ConversationManager:
    '''
    this class is used to manage the conversation and development process.
    It uses the OpenAI API to generate responses and execute the code.
    The conversation is managed in a loop, with the initial idea generation, code development, and iterative refinement.
    steps in process are:
    1. Initial idea generation
    2. Development of the project
    3. Iterative refinement and completion check
    4. Execute and test the generated code
    5. Further refine the code based on feedback
    6. Finalize the project
    7. Output the final project code
    8. Log the conversation and development process

    '''
    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI()
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": "meet all requirements and use your knowledge to do this"+prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        print(f"Response: {content}")
        return content



    def iterate_development(self):
        self.project_idea = self.generate_response(model, idea_prompt, idea_system)
        self.project_code = self.generate_response(model, code_prompt+f"{self.project_idea}", code_system)
        
        completion = "no"
        iteration = 0
        while completion == "no":
            clean_project_code = CodeExecutor.remove_comments_and_extract_code(self.project_code)
            CodeExecutor.save_code(clean_project_code, f"project_{iteration}.py")
            execution_result = CodeExecutor.execute_python_code(clean_project_code)
            feedback = self.generate_response(model, feedback_user+execution_result+clean_project_code, feedback_system)
        
            if "yes" in feedback.lower():
                clean_project_code = CodeExecutor.remove_comments_and_extract_code(self.project_code)
                CodeExecutor.save_code(clean_project_code, f"project_{iteration}.py")
                completion = "yes"
                logging.info("Project deemed complete and potentially profitable.")
            else:
                CodeExecutor.save_code(self.project_code, f"project_{iteration}_before_refinement.py")
                self.project_code = self.generate_response(model, f"Refine the Python code to ensure profitability and completion. {self.project_code} as it was rejected by another AI", "Refining project code to meet academic standards and beyond...")
                iteration += 1
    def conversation_thread(self):
        self.iterate_development()
        if self.project_code:
            logging.info("Final Project Code:\n" + self.project_code)
        else:
            logging.warning("Failed to develop a profitable project.")
        logging.info("Conversation and development process complete.")
        
