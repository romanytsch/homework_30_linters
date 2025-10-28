from datetime import datetime

def parse_log_time(timestr: str):
    return datetime.strptime(timestr, '%H:%M:%S.%f')

def calculate_average_duration(log_path='app.log') -> float:
    enter_times = []
    leave_times = []
    durations = []

    with open(log_path) as f:
        for line in f:
            parts = line.strip().split(' ', 3)

            if len(parts) > 3:
                continue
            timestamp, level, msg = parts[0], parts[1], parts[2]

            if msg == "Enter_measure_me":
                enter_times.append(parse_log_time(timestamp))
            elif msg == "Leave_measure_me":
                leave_times.append(parse_log_time(timestamp))

    # Предполагается, что enter и leave идут по порядку
    for start, end in zip(enter_times, leave_times):
        durations.append((end - start).total_seconds())

    average_duration = sum(durations) / len(durations) if durations else 0
    return average_duration