import json
import shlex

import subprocess


def run_and_get_ip():
    command_line = """curl -s -H "Accept: application/json" -X GET https://api.ipify.org?format=json"""
    args = shlex.split(command_line)
    res = subprocess.run(args, capture_output=True, text=True)
    output = res.stdout.strip()
    data = json.loads(output)
    return data.get('ip')

if __name__ == '__main__':
    ip = run_and_get_ip()
    print(ip)

