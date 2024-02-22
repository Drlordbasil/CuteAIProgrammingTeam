import subprocess
import tempfile
import os
import logging
import re

class CodeExecutor:
    """
    Class to execute Python code securely and efficiently, with improved error handling and maintainability.
    Adapted to conditionally handle or simulate user inputs in executed code.
    """
    @staticmethod
    def is_valid_code(code):
        """
        Validates Python code for syntax without executing it.
        Returns True if the code is syntactically correct, False otherwise.
        """
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    @staticmethod
    def execute_python_code(code, input_simulation=None):
        """
        Executes Python code from a string, capturing stdout and stderr.
        Conditionally simulates user input if 'input_simulation' is provided.
        Returns the stdout output, or an error message in case of failure.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            # Prepare the code, possibly wrapping it to simulate input
            prepared_code = CodeExecutor._prepare_code_for_execution(code, input_simulation)
            tmp.write(prepared_code.encode())
            tmp.flush()
            tmp_name = tmp.name
        try:
            result = subprocess.run(['python', tmp_name], capture_output=True, text=True, check=True, timeout=30)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Execution error: {e.stderr}")
            return f"Error executing Python code: {e.stderr}"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return f"Unexpected error: {e}"
        except subprocess.TimeoutExpired as e:
            logging.error(f"Execution timeout: {e}")
            return f"Execution timeout: {e}"
        
        finally:
            os.remove(tmp_name)

    @staticmethod
    def _prepare_code_for_execution(code, input_simulation):
        """
        Prepares the Python code for execution, simulating 'input()' if necessary.
        """
        if input_simulation is not None:
            # Simulate input by replacing 'input()' calls with provided simulations
            simulated_input_code = f"input = lambda x=None: {repr(input_simulation)}\n" + code
            return simulated_input_code
        else:
            return code
    @staticmethod
    def save_code(code, filename):
        """
        Saves the given code to a file specified by filename.
        """
        try:
            file_path = os.path.join("projects", filename)  # Construct the correct file path
            with open(file_path, "w") as file:
                file.write(code)
            logging.info(f"Code saved to {file_path}")
        except IOError as e:
            logging.error(f"Failed to save code to {file_path}: {e}")

    @staticmethod
    def read_code(filename):
        """
        Reads and returns the code from a file specified by filename.
        """
        try:
            with open(filename, "r") as file:
                code = file.read()
            logging.info(f"Code read from {filename}")
            return code
        except IOError as e:
            logging.error(f"Failed to read code from {filename}: {e}")
            return ""

    @staticmethod
    def remove_comments_and_extract_code(markdown_text):
        """
        Extracts Python code blocks from markdown text, removes comments, and ensures no markdown syntax is included.
        """
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No Python code blocks found in the Markdown text.")
            return ""
        code_blocks = [re.sub(r'#.*', '', match.strip()) for match in matches]  # Remove comments
        clean_code = '\n'.join(code_blocks).replace('```python', '').replace('```', '')  # Remove markdown syntax
        return clean_code
