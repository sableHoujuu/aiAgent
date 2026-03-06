import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key found. Did you remember to set it?")

    parser = argparse.ArgumentParser(description="Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    if args.verbose is True:
        output = f"User prompt: {args.user_prompt}\n"
        print(output)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for iteration in range(20):
        if iteration >= 20:
            print("Reached max iterations without a conclusive response from model.")
            sys.exit(1)

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("No response recieved, is the API down?")
        if args.verbose is True:
            output = (
                f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
                f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
            )
            print(output)

        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls is not None:
            function_call_responses = []
            for function_call in response.function_calls:
                function_call_response = call_function(function_call, args.verbose)
                if (
                    function_call_response.parts is None
                    or function_call_response.parts == []
                ):
                    raise Exception("Parts list is empty!")
                parts = function_call_response.parts
                if parts[0].function_response.response is None:
                    raise Exception("No response from function")
                function_call_responses.append(parts[0])
                if args.verbose is True:
                    print(
                        f"-> {function_call_response.parts[0].function_response.response}"
                    )
            if function_call_responses != []:
                messages.append(
                    types.Content(role="user", parts=function_call_responses)
                )

        else:
            print(f"Response: {response.text}")
            break
    return


if __name__ == "__main__":
    main()
