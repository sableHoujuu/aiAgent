import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: Failed getting absolute path to working directory. {e}"

    try:
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
    except Exception as e:
        return f"Error: Failed normalizing path. {e}"

    if os.path.isdir(target_dir) is False:
        return f'Error: "{directory}" is not a directory'
    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    if valid_target_dir is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        files = os.listdir(target_dir)
    except Exception as e:
        return f"Error: Could not list files in {target_dir}. {e}"
    info_string = ""
    for file_name in files:
        file_path = os.path.join(target_dir, file_name)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        info_string += f"\n - {file_name}: file_size={file_size} bytes, is_dir={is_dir}"

    return info_string
