#conversation_manager.py
from openai import OpenAI
import logging
from config import model, idea_prompt, code_prompt
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
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        print(f"Response: {content}")
        return content

    @staticmethod
    def remove_comments(code):
        new_lines = []
        lines = code.split('\n')
        for line in lines:
            if not line.strip().startswith("#"):
                if '#' in line:
                    line = line.split('#', 1)[0]
                new_lines.append(line)
        return '\n'.join(new_lines)

    @staticmethod
    def extract_python_code(markdown_text):
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No Python code blocks found in the Markdown text.")
            return ""
        python_code_blocks = [match.strip() for match in matches]
        if len(python_code_blocks) > 1:
            logging.info("Multiple Python code blocks found. Returning the first block.")
        clean_code = ConversationManager.remove_comments(python_code_blocks[0])
        return clean_code

    def iterate_development(self):
        self.project_idea = self.generate_response(model, idea_prompt, "Generating extremely real profitable project idea that an LLM can create in one response...")
        self.project_code = self.generate_response(model, code_prompt+f"{self.project_idea}", "Developing project code(full robust verbose complex logic without placeholders)...I am a python programming superstar")
        
        completion = "no"
        iteration = 0
        while completion == "no":
            execution_result = CodeExecutor.execute_python_code(self.project_code)
            feedback = self.generate_response(model, f""""
                                              Execution result: {execution_result}\n
                                              Is the program complete and profitable either directly or indirectly using the original idea of {self.project_idea}?
                                              Make sure you are heavily reviewing it for  the following criteria all must be met as our requirements:(all answers must be no if one answer is no, dont include yes at all if no is an answer.) 
                                              1. Does it profit eventually?
                                              2. Is it complete?
                                              3. Does it have a niche?
                                              4. Is it robust?
                                              5. is it free of placeholders?
                                              6. Does it have a unique selling point?
                                              7. Is it a program that can be run on any computer with python installed(given libraries are installed as well)?
                                              8. does it have a main loop with GUI?

                                              Answer yes or no ONLY, if all criteria are met, answer yes.
                                              if all criteria are not met, answer no. Only answer 1 yes or no, dont respond to each criteria individually as I just need a yes/no answer to move on. Does it pass all?
                                              """, "Evaluating program completion...")
            
            if "yes" in feedback.lower():
                CodeExecutor.save_code(self.project_code, f"{self.project_code}", f"project_{iteration}.py")
                completion = "yes"
                logging.info("Project deemed complete and potentially profitable.")
            else:
                # Further refine the code based on feedback
                CodeExecutor.save_code(self.project_code, f"{self.project_code}", f"project_{iteration}.py")
                refined_code = self.generate_response(model, f"Refine the Python code to ensure profitability and completion.{self.project_code} as it was rejected by another AI", "Refining project code to meet acedemic standards and beyond...")
                valid_code = self.extract_python_code(refined_code)
                if valid_code:
                    self.project_code = valid_code
                    CodeExecutor.save_code(self.project_code,f"{self.project_code}", f"project_{iteration}.py")
                    print(f"Refined code saved to project_{iteration}.py")
                    iteration += 1
    def conversation_thread(self):
        self.iterate_development()
        if self.project_code:
            logging.info("Final Project Code:\n" + self.project_code)
        else:
            logging.warning("Failed to develop a profitable project.")
# Initialize ConversationManager
manager = ConversationManager()

# Run the development process
manager.conversation_thread()