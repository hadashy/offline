import os
from typing import Optional


PATH = '../'


def get_relevant_directories() -> Optional[list[str]]:
    relevant_directories = []
    directories = os.listdir(PATH)
    for directory in directories:
        files = os.listdir(PATH + directory)
        python_files = [i for i in files if i.endswith('.py')]
        if python_files:
            relevant_directories.append(directory)
    return relevant_directories


def run_mypy_check(directories: Optional[list[str]]) -> None:
    if directories:
        for directory in directories:
            os.system(f'mypy --namespace-packages {PATH}{directory}')


def run_pylint_check(directories: Optional[list[str]]) -> None:
    if directories:
        for directory in directories:
            os.system(f'pylint --extension-pkg-whitelist=win32security {PATH}{directory} '
                      f'--disable=missing-docstring --disable=c-extension-no-member')


def main() -> None:
    directories = get_relevant_directories()
    print("Moving to mypy checks")
    run_mypy_check(directories)
    print("Moving to pylint checks")
    run_pylint_check(directories)


if __name__ == '__main__':
    main()
