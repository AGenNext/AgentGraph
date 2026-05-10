import sys
import os

# Add path to AGenNext-Helper repo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../AGenNext-Helper')))

try:
    from helper import say_hello
except ImportError:
    def say_hello():
        print('AGenNext Helper not found.')


def invoke_helper():
    print('Invoking AGenNext Helper from Enterprise:')
    say_hello()


if __name__ == '__main__':
    invoke_helper()