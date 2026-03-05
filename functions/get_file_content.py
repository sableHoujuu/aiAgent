import os

from google.genai import types

from config import CHARACTER_LIMIT

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file with a given path and returns it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to get contents from.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: Failed getting absolute path to working directory. {e}"

    try:
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    except Exception as e:
        return f"Error: Failed normalizing path. {e}"

    valid_target_dir = os.path.commonpath([absolute_path, target_file]) == absolute_path
    if valid_target_dir is False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    valid_file = os.path.isfile(target_file)
    if valid_file is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            contents = f.read(CHARACTER_LIMIT)
            if f.read(1):
                contents += (
                    f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
                )
    except Exception as e:
        return f"Error: Error reading or opening file, {e}"

    return contents
