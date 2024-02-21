import subprocess
import tempfile
import os
import logging
import re

class CodeExecutor:
    '''
    Class to execute Python code and return the output.
    This class is used to execute Python code and return the output. It uses the subprocess module to run the code in a separate process and capture the output. 
    The code is written to a temporary file and then executed using the Python interpreter. 
    The output is then returned to the caller. If there is an error, an exception is raised and the error message is returned.
    The temporary file is then deleted.
    the flow of the code is as follows:
    1. Write the code to a temporary file
    2. Execute the code using the Python interpreter
    3. Capture the output and return it to the caller
    4. If there is an error, raise an exception and return the error message
    5. Delete the temporary file
    
    '''
    @staticmethod
    def execute_python_code(code, input_simulation=""):
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode())
            tmp_name = tmp.name
        try:
            result = subprocess.run(['python', tmp_name], input=input_simulation.encode(), capture_output=True, text=True, timeout=30)
            output = result.stdout
            error = result.stderr
            if error:
                raise Exception(error)
            return output
        except Exception as e:
            return f"Error executing Python code: {e}"
        finally:
            os.remove(tmp_name)
    def save_code(self, code, filename):
        with open(filename, "w") as file:
            file.write(code)    
        print(f"Code saved to {filename}")
    def read_code(self, filename):
        with open(filename, "r") as file:
            code = file.read()
        print(f"Code read from {filename}")
        return code
    def execute_code(self, code, input_simulation=""):
        result = subprocess.run(['python', code], input=input_simulation.encode(), capture_output=True, text=True, timeout=30)
        output = result.stdout
        error = result.stderr
        if error:
            raise Exception(error)
        return output
    
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

    def extract_python_code(self, markdown_text):
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No Python code blocks found in the Markdown text.")
            return ""
        python_code_blocks = [match.strip() for match in matches]
        if len(python_code_blocks) > 1:
            logging.info("Multiple Python code blocks found. Returning the first block.")
        clean_code = self.remove_comments(python_code_blocks[0])
        return clean_code