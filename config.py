#config.py
gpt4 = "gpt-4-0125-preview"
gpt3 = "gpt-3.5-turbo-0125"
ft3 = "ft:gpt-3.5-turbo-1106:personal::8uLu2E19"
model = gpt3
smartmodel = gpt4

gemini_api_key = ""
idea_prompt = """
Generate a profitable Python program idea with zero startup and upkeep costs that can be developed in 1 file. 
The program should be able to run on any computer with Python installed and should make profit in a reasonable amount of time. 
use openai calls to create complex outputs that are not easily understood by humans but provide valuable profitable outputs.
we need to make an autonomous agent specefic to a certain niche that can output profitable content.
We need to use this to describe the new openai api calls:
from openai import OpenAI
#never use dotenv as we dont need it for api calls
    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI() # never add api_key here
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content
make sure your idea is robust and profitable. If I can sell the output content such as programs it creates or content like full chapterbooks to sell online or anything else like that.
                                              1. Does it profit eventually?
                                              2. Is it complete?
                                              3. Does it have a niche?
                                              4. Is it robust?
                                              5. is it free of placeholders?
                                              6. Does it have a unique selling point?
                                              7. Is it a program that can be run on any computer with python installed(given libraries are installed as well)?
                                              8. does it have a main loop with GUI?
                                              9. is it creatively unique?
"""
code_prompt = """
Develop Python code for the following idea. Please note, do not include placeholders such as 'pass' in the Python code. The code should follow this structure:

#never use dotenv as we dont need it for api calls
                                              1. Does it profit eventually?
                                              2. Is it complete?
                                              3. Does it have a niche?
                                              4. Is it robust?
                                              5. is it free of placeholders?
                                              6. Does it have a unique selling point?
                                              7. Is it a program that can be run on any computer with python installed(given libraries are installed as well)?
                                              8. does it have a main loop with GUI?
                                              9. is it creatively unique?
                                              10. is it a standalone program you can run without other scripts?
```python(must be a standalone program that can be run on any computer with python installed given libraries are installed as well.)
# Import necessary libraries
import os
import sys
import threading
from openai import OpenAI
#never use dotenv as we dont need it for api calls
# Define necessary classes
class MyClass:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def method1(self):
        # Implement method1
        return self.param1 + self.param2

    def method2(self):
        # Implement method2
        return self.param1 * self.param2
def GUI():
    # Implement GUI
    return "GUI"
# Define main function including GUI with threading for all classes used.
def main():
    # Create an instance of MyClass
    my_class = MyClass('param1', 'param2')

    # Call methods of MyClass
    my_class.method1()
    my_class.method2()

# Call the main function
if __name__ == "__main__":
    main()
```
proper openai calls that you cant change if using openai:
from openai import OpenAI
    gpt4 = "gpt-4-0125-preview"
    gpt3 = "gpt-3.5-turbo-0125" # good model for testing purposes.
    def __init__(self):
        self.conversation_memory = []
        self.client = OpenAI() # never add api_key here
        self.project_idea = ""
        self.project_code = ""

    def generate_response(self, model_type, prompt, system_message=""):
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model_type, messages=messages)
        content = response.choices[0].message.content
        logging.info(f"Response: {content}")
        return content
never change these openai core functions(they are even case-sensative, dont include models I didnt list) while improving the programs extended functionalities for automation of content creation. All outputs from your program must directly profit with content creation or other means of profit where the user can sell the output like program code, stories, images, ect.
"""
code_system = "Developing 1 script python programs with ease is your duty, you are Anthony that codes perfectly(full robust verbose complex logic without placeholders such as pass in python)...I am a python programming superstar"
idea_system = "You are an LLM based AI named Fred, you can create a profitable project idea in one response. You are a python programming superstar, you can develop a full robust verbose complex logic without placeholders in one response."
feedback_system = "I am strictly a program feedback loop agent named Jerry in a larger set of AI agent members."
feedback_user = """
                                            
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
                                            9. is it creatively unique?
                                                script:
                                                
                                            Answer yes or no ONLY, if all criteria are met, answer yes.
                                            if all criteria are not met, answer no. Only answer 1 yes or no, dont respond to each criteria individually as I just need a yes/no answer to move on. Does it pass all?
                                            """
