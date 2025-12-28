import subprocess
import os


def process_count(username: str) -> int:
    """Количество процессов пользователя username."""
    result = subprocess.run(['pgrep', '-u', username],
                            capture_output=True, text=True)
    return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0


def total_memory_usage(root_pid: int) -> float:
    """Суммарное потребление памяти дерева процессов с корнем root_pid."""
    result = subprocess.run(['ps', '-eo', 'ppid,pid,%mem', '--no-headers'],
                            capture_output=True, text=True)

    lines = result.stdout.strip().split('\n')

    def get_children(ppid):
        children_pids = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[0] == str(ppid):
                children_pids.append(int(parts[1]))
        return children_pids

    def calc_mem(pid):
        mem = 0.0
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[1] == str(pid):
                mem += float(parts[2])
                break
        for child_pid in get_children(pid):
            mem += calc_mem(child_pid)
        return mem

    return calc_mem(root_pid)


if __name__ == "__main__":
    username = os.getlogin()
    my_pid = os.getpid()

    print(f'Процессов пользователя {username}:', process_count(username))
    print(f'Память текущего процесса (PID {my_pid}):', total_memory_usage(my_pid))
