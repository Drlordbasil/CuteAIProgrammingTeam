import subprocess
import tempfile
import os
import logging
import re

# Improved logging setup (example - to be adjusted based on requirements)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureTempFile:
    """
    Context manager for managing temporary files securely and efficiently.
    """
    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
        return self.temp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.temp_file.name)

class CodeExecutor:
    """
    Class to execute Python code securely and efficiently, with improved error handling and maintainability.
    Adapted to conditionally handle or simulate user inputs in executed code.
    """
    @staticmethod
    def is_valid_code(code):
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error in code: {e.msg} at line {e.lineno}")
            return False

    @staticmethod
    def execute_python_code(code, input_simulations=None):
        with SecureTempFile() as tmp:
            prepared_code = CodeExecutor._prepare_code_for_execution(code, input_simulations)
            tmp.write(prepared_code.encode())
            tmp.flush()
            tmp_name = tmp.name
        try:
            result = subprocess.run(['python', tmp_name], capture_output=True, text=True, check=True, timeout=30)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Execution error: {e.stderr}")
            return f"Error executing Python code: {e.stderr}"
        except subprocess.TimeoutExpired:
            logging.error("Execution timeout. The code did not complete within the allowed time.")
            return "Execution timeout: The code did not complete within the allowed time."

    @staticmethod
    def _prepare_code_for_execution(code, input_simulations):
        if input_simulations is not None:
            simulated_input_code = ''
            for input_value in input_simulations:
                simulated_input_code += f"input = lambda x=None, _values={input_simulations}: _values.pop(0)\n"
            return simulated_input_code + code
        else:
            return code

    @staticmethod
    def save_code(code, filename):
        try:
            file_path = os.path.join("projects", filename)
            with open(file_path, "w") as file:
                file.write(code)
            logging.info(f"Code saved to {file_path}")
        except IOError as e:
            logging.error(f"Failed to save code to {file_path}: {e}")

    @staticmethod
    def read_code(filename):
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
        pattern = r"```python\n(.*?)```"
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        if not matches:
            logging.warning("No Python code blocks found in the Markdown text.")
            return ""
        code_blocks = [re.sub(r'#.*', '', match.strip()) for match in matches]
        clean_code = '\n'.join(code_blocks).replace('```python', '').replace('```', '')
        return clean_code
