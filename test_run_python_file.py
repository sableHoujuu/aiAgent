from functions.run_python_file import run_python_file


def main():
    results = run_python_file("calculator", "main.py")
    print(results)
    results = run_python_file("calculator", "main.py", ["3 + 5"])
    print(results)
    results = run_python_file("calculator", "tests.py")
    print(results)
    results = run_python_file("calculator", "../main.py")  # should error
    print(results)
    results = run_python_file("calculator", "nonexistent.py")  # should error
    print(results)
    results = run_python_file("calculator", "lorem.txt")  # should error
    print(results)


main()
