import os

from dimtim.helpers.management.runner import CommandRunner


def main():
    CommandRunner(os.getcwd(), 'bin').run()


if __name__ == '__main__':
    main()
