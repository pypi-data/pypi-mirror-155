"""
Main code file for the raise tool. Implements compliance checking and repo initialization.

FWIW, I too think it's ridiculous that we need two libraries for GitHub stuff--and we only
use one function from each; but one does not support the other, so here we fucking are.

Authors:
    Rahul Yedida <rahul@ryedida.me>
"""
import os
import argparse
import glob
from pathlib import Path
from colorama import Fore, init
from pycodestyle import StyleGuide
from typing import Union
from github import Github
from git import Repo
import configparser


CONFIG_FILENAME = '.raise.conf'


def test_file_exists(base_path: Path, filename: str):
    """
    Checks that a file exists. The return scheme is reversed: this allows us
    to count the ERRORS.

    TODO: Move this to a utils file

    :param {Path} base_path - The base path.
    :param {str} filename - The filename to check for.
    :param {bool} status - True if the file does NOT exist.
    """
    if not os.path.exists(base_path / filename):
        print(Fore.RED + 'File missing: ' + filename)
        return True
    return False


def test_string_exists(base_path: Path, filename: str, string: Union[str, list], beginning: bool):
    """
    Tests whether a file contains a specific string, optionally at the beginning of a line. As with
    test_file_exists, returns True if the string does NOT exist.

    TODO: Move this to a utils file.

    :param {Path} base_path - The base path
    :param {str} filename - The file to test
    :param {Union[str, list]} string - The string to test. If a list, checks if ANY of the strings exist
    :param {bool} beginning - Whether the string should be at the beginning of the file.
    :return {bool} status - True if the string does NOT exist.
    """
    with open(base_path / filename, 'r') as f:
        text = f.read()

    pattern = ''  # Pattern to test for
    if beginning:
        pattern += '\n'

    if isinstance(string, str):
        pattern += string
        if pattern not in text:
            print(Fore.RED + f'Missing text in {filename}: {string}')
            return True
    else:
        pattern_reset = pattern  # Keep a backup
        for item in string:
            pattern += item
            if pattern in text:
                return False  # We don't need to check anymore
            pattern = pattern_reset  # Reset `pattern`
        return True
    return False


def overwrite_args_with_config(args: dict, config: dict):
    """
    Overwrites args with preferences in the config file.

    :param {dict} args - the result of vars(ArgumentParser.parse)
    :config {dict} config - a dict with preferences
    """
    if 'init' in config:
        init_prefs = config['init']

        if 'template' in init_prefs:
            args['template'] = init_prefs['template']

        if 'fork' in init_prefs:
            try:
                args['no_fork'] = not init_prefs.getboolean('fork')
            except ValueError:
                print(
                    Fore.RED + '[ERR] invalid value for init.fork in config file')

    if 'check' in config:
        check_prefs = config['check']

        if 'max_line_length' in check_prefs:
            try:
                args['max_line_length'] = check_prefs.getint('max_line_length')
            except ValueError:
                print(
                    Fore.RED + '[ERR] invalid value for check.max_line_length in config file')


def _main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Checks compliance with the RAISE code template.')
    parser.add_argument('path', type=str, help='Root directory')
    parser.add_argument('init', action='store_true',
                        help='Initializes a new repo from a template')
    parser.add_argument('--template', type=str, default='dl4se',
                        help='Selects the template to use')
    parser.add_argument('--max_line_length', default=120)
    args = vars(parser.parse_args())

    # Does a config file exist?
    if os.path.exists(CONFIG_FILENAME):
        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILENAME)

        # Overwrite args with config file preferences
        overwrite_args_with_config(args, config)

    if args['init']:
        # Initialize a new repo: fork, and then clone
        template = args['template']

        if not args.no_fork:
            # Find the token
            if 'token' not in args:
                print('raise will now fork the template repo to your account. ' +
                      'Please provide a GitHub access token.')
                token = input(Fore.BLUE + 'access_token = ' + Fore.RESET)
            else:
                token = args['token']

            # Fork the repo
            gh = Github(token)
            repo = gh.get_repo(f'yrahul3910/raise-template-{template}')
            repo.create_fork()

            # Clone the repo
            Repo.clone_from(repo.html_url, os.getcwd())

        return

    # Extract root directory
    base_path = Path(args['path'])

    # Initialize colorama
    init()

    # Perform pycodestyle checks
    print(Fore.BLUE + '[Running code style checks]')
    print(Fore.RED)
    checker = StyleGuide(max_line_length=args['max_line_length'])
    report = checker.check_files(paths=glob.glob(
        f'{base_path}/**/*.py', recursive=True))
    report.print_statistics()

    if report.get_count() == 0:
        print(Fore.GREEN + 'No issues found.')
    print()

    # Perform file checks
    print(Fore.BLUE + '[Checking directory structure]\n')
    error_count = 0
    file_list = [
        'README.md',
        'src/',
        'data/',
        '.gitignore',
        'LICENSE',
        'requirements.txt',
        'main.py',
        'src/__init__.py'
    ]

    for file in file_list:
        error_count += test_file_exists(base_path, file)

    if error_count == 0:
        print(Fore.GREEN + 'No issues found.')
    print()

    print(Fore.BLUE + '[Checking README]\n')
    error_count = 0
    lines_list = [
        '## Data',
        '## Reference',
        ['## Instructions', '## Setup']
    ]

    for line in lines_list:
        error_count += test_string_exists(base_path, 'README.md', line, True)

    if error_count == 0:
        print(Fore.GREEN + 'No issues found.')


if __name__ == '__main__':
    _main()
