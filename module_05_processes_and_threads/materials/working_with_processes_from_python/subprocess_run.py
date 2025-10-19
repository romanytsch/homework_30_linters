import subprocess
import sys


def run_program():
    res = subprocess.run(['python', 'test_program.py'],
                         stdout=sys.stderr,
                         stderr=subprocess.STDOUT,
                         text=True)
    print(res, file=sys.stderr)

if __name__ == '__main__':
    run_program()
