import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with a given path and arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments for the file to be executed.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: Failed getting absolute path to working directory. {e}"

    try:
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    except Exception as e:
        return f"Error: Failed normalizing path. {e}"

    valid_target_file = (
        os.path.commonpath([absolute_path, target_file]) == absolute_path
    )
    if valid_target_file is False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if os.path.isfile(target_file) is False:
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if target_file.endswith(".py") is False:
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args is not None:
        command.extend(args)

    try:
        completed_process = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return_string = ""
    if completed_process.returncode != 0:
        return_string += f"Process exited with code {completed_process.returncode}."
    if completed_process.stdout is None and completed_process.stderr is None:
        return_string += " No output produced."

    return_string += (
        f" STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}"
    )

    return return_string
