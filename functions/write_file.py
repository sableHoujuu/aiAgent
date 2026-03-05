import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file with a given path and contents, creating it if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "contents"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to.",
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: Failed getting absolute path to working directory. {e}"

    try:
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    except Exception as e:
        return f"Error: Failed normalizing path. {e}"

    if os.path.isdir(target_file) is True:
        f'Error: Cannot write to "{file_path}" as it is a directory'
    valid_target_file = (
        os.path.commonpath([absolute_path, target_file]) == absolute_path
    )
    if valid_target_file is False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.split(target_file)[1], exist_ok=True)
    except Exception as e:
        return f"Error: makedirs failed creating directories. {e}"

    try:
        with open(target_file, "w") as f:
            f.write(content)

    except Exception as e:
        return (
            f"Error: could not open or write to {file_path}, see for more details: {e}"
        )

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
