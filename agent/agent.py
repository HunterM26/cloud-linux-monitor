import psutil
import os
import time

pipe_path = "/tmp/sysmetrics.pipe"

# Ensure the named pipe exists
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)

while True:
    try:
        # Gather metrics
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        net = psutil.net_io_counters()
        load = os.getloadavg()[0]

        # Format the data
        data = (
            f"CPU:{cpu:.2f}% | "
            f"MEM:{mem:.2f}% | "
            f"DISK:{disk:.2f}% | "
            f"NET:{(net.bytes_sent + net.bytes_recv) / 1_000_000:.2f}MB | "
            f"LOAD:{load:.2f}\n"
        )

        # Open pipe and write
        with open(pipe_path, "w") as pipe:
            pipe.write(data)

        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
