import os
import re
import argparse

import requests
from bs4 import BeautifulSoup
from colorama import Fore

from browser_classes import BrowserHistory

browser_history = BrowserHistory()


def show_parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']):
        if tag.name == 'a':
            print(Fore.BLUE + tag.get_text(), Fore.RESET)
        else:
            print(tag.get_text())


def show_new_content(dir_name, user_input):
    url = user_input if user_input.startswith('https://') else f'https://{user_input}'
    domain_name = url[url.find('/') + 2: url.find('.')]
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Invalid URL')
    else:
        if re.match('2..', str(r.status_code)):
            show_parse_content(r.content)
            with open(os.path.join(dir_name, domain_name), 'wb') as file:
                file.write(r.content)
            browser_history.extend_queue(domain_name)


def show_last_content(dirname):
    if len(browser_history.history) > 0:
        last_page = browser_history.history.pop()
        if last_page == '':
            return
        else:
            with open(os.path.join(dirname, last_page), 'rb') as file:
                show_parse_content(file.read())
            print()


def show_existing_content(dirname, user_input):
    with open(os.path.join(dirname, user_input), 'rb') as file:
        show_parse_content(file.read())
    print()
    browser_history.extend_queue(user_input)


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory_name', help='Name of directory to save files in')
    args = parser.parse_args()
    return args.directory_name


def main():
    directory_name = get_command_line_arguments()
    if not os.access(directory_name, os.F_OK):
        os.mkdir(directory_name)

    while (user_input := input().strip()) != 'exit':
        if user_input in os.listdir(directory_name):
            show_existing_content(directory_name, user_input)
        elif user_input == 'back':
            show_last_content(directory_name)
        else:
            show_new_content(directory_name, user_input)


if __name__ == '__main__':
    main()
