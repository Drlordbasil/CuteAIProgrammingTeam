#config.py
gpt4 = "gpt-4-0125-preview"
gpt3 = "gpt-3.5-turbo-0125"
ft3 = "ft:gpt-3.5-turbo-1106:personal::8uLu2E19"
model = gpt3
smartmodel = gpt4
idea_prompt = """
Generate a profitable Python program idea with zero startup and upkeep costs that can be developed in 1 file. 
The program should be able to run on any computer with Python installed and should make profit in a reasonable amount of time. 
use openai calls to create complex outputs that are not easily understood by humans but provide valuable profitable outputs.
we need to make an autonomous agent specefic to a certain niche that can output profitable content.
We need to use this to describe the new openai api calls:
from openai import OpenAI

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
"""
code_prompt = """
Develop Python code for the following idea. Please note, do not include placeholders such as 'pass' in the Python code. The code should follow this structure:

```python
# Import necessary libraries
import os
import sys
import threading
from openai import OpenAI
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
