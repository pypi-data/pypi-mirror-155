import os
import subprocess
import pathlib


if __name__ == '__main__':
    subprocess.Popen(['python3', f'{pathlib.Path(__file__).parent.resolve()}/base_core.py'])
