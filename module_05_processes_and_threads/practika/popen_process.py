import subprocess
import time

def main():
    process = []

    for _ in range(10):
        p = subprocess.Popen('sleep 15 && echo "My mission is done here!"',
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.append(p)

        start_time = time.time()

        outputs = []
        for p in process:
            out, err = p.communicate()
            outputs.append(out.decode().strip())

        end_time = time.time()
        duration = end_time - start_time

        for i, output in enumerate(outputs, 1):
            print(f"Process {i}: {output}")
        print(f"Total execution time: {duration:.2f} seconds")

if __name__ == '__main__':
    main()
