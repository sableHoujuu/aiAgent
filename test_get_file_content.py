from functions.get_file_content import get_file_content


def main():
    result = get_file_content("calculator", "lorem.txt")
    print(f"Length of output is {len(result)}, last 100 chars: {result[-100::]}")
    result = get_file_content("calculator", "main.py")
    print(f"Contents from calculator/main.py: {result}")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"Contents from calculator/pkg/calculator.py: {result}")
    result = get_file_content("calculator", "/bin/cat")
    print(f"This should be an error: {result}")
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"This should be an error: {result}")


main()
