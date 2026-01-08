import subprocess


def process_count(username: str) -> int:
    """Количество процессов, запущенных из-под текущего пользователя username."""
    cmd = ["pgrep", "-u", username]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return len(result.stdout.strip().split('\n'))
    return 0


def total_memory_usage(root_pid: int) -> float:
    """Суммарное потребление памяти древа процессов с корнем root_pid в процентах."""
    # Получаем все процессы с PPID (включая сам root_pid где PPID=1 или корень)
    cmd_ps = [
        "ps", "-eo", "ppid,pid,%mem", "--ppid", str(root_pid), "-o", "ppid,pid,%mem"
    ]
    result = subprocess.run(cmd_ps, capture_output=True, text=True)

    if result.returncode != 0:
        return 0.0

    lines = result.stdout.strip().split('\n')[1:]  # Пропускаем заголовок

    total_mem = 0.0
    pids = set()
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            ppid = int(parts[0])
            pid = int(parts[1])
            mem = float(parts[2])
            pids.add(pid)
            total_mem += mem

    # Рекурсивно собираем потомков (дерево процессов)
    def collect_children(pid_set, new_pids):
        cmd_children = ["ps", "--ppid"] + [str(p) for p in new_pids] + ["-o", "ppid,pid,%mem"]
        result_child = subprocess.run(cmd_children, capture_output=True, text=True)
        if result_child.returncode != 0:
            return pid_set

        child_lines = result_child.stdout.strip().split('\n')[1:]
        child_pids = []
        add_mem = 0.0
        for line in child_lines:
            parts = line.split()
            if len(parts) >= 3:
                ppid = int(parts[0])
                pid = int(parts[1])
                mem = float(parts[2])
                if ppid in pid_set:
                    child_pids.append(pid)
                    add_mem += mem

        pid_set.update(child_pids)
        total_mem[0] += add_mem  # Мутируем total_mem через list для ссылки

        if child_pids:
            collect_children(pid_set, child_pids)
        return pid_set

    total_mem_ref = [total_mem]
    all_pids = collect_children(pids, list(pids))

    return total_mem_ref[0]
