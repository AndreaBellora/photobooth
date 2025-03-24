import psutil
import matplotlib.pyplot as plt
import time
from collections import deque

def get_process_by_name(name):
    """Find the first process matching the given name."""
    while True:
        for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            cmdline = ' '.join(process.info.get('cmdline', [])).lower()
            if name.lower() in cmdline or name.lower() in process.info['name'].lower():
                return psutil.Process(process.info['pid'])
        time.sleep(1)

def monitor_memory_usage(process_name, duration=60, interval=0.1):
    """Monitors and plots memory usage of a process over time."""
    process = get_process_by_name(process_name)
    if not process:
        print(f"No process found with name: {process_name}")
        return

    times = deque(maxlen=duration)
    memory_usages = deque(maxlen=duration)

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Memory Usage (MB)")
    ax.set_title(f"Memory Usage of {process_name}")
    line, = ax.plot([], [], 'b-', label='Memory Usage')
    ax.legend()

    def on_close(event):
        print("Plot closed. Stopping monitoring.")
        plt.ioff()
        exit()
    
    fig.canvas.mpl_connect('close_event', on_close)

    start_time = time.time()
    
    try:
        while True:
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)
            try:
                memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            except psutil.NoSuchProcess:
                memory_usage = 0    
            memory_usages.append(memory_usage)
            
            line.set_xdata(times)
            line.set_ydata(memory_usages)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(interval)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    # process_name = input("Enter process name: ")
    process_name = 'test_picture_editor.py'
    monitor_memory_usage(process_name)
