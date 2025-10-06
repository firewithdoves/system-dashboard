# system_dashboard.py
# Live system dashboard: press Q to quit

import time
import datetime as dt
import psutil
from rich.table import Table
from rich.live import Live
from rich.console import Console

console = Console()

def bytes_to_gb(n):
    return f"{n / (1024**3):.1f} GB"

def make_table() -> Table:
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=None)
    disk = psutil.disk_usage("C:\\")
    boot = dt.datetime.fromtimestamp(psutil.boot_time())
    uptime = dt.datetime.now() - boot

    tb = Table(title="💻 System Dashboard", expand=True, show_lines=True)
    tb.add_column("Metric", style="cyan", no_wrap=True)
    tb.add_column("Usage", justify="center", style="magenta")
    tb.add_column("Details", justify="right", style="green")

    # CPU
    tb.add_row(
        "🧠 CPU",
        f"{cpu:.0f}%",
        f"Cores: {psutil.cpu_count(logical=True)} | Uptime: {str(uptime).split('.')[0]}"
    )

    # Memory
    tb.add_row(
        "🧵 Memory",
        f"{mem.percent:.0f}%",
        f"Used {bytes_to_gb(mem.used)} / {bytes_to_gb(mem.total)}"
    )

    # Disk C:
    tb.add_row(
        "💾 Disk (C:)",
        f"{disk.percent:.0f}%",
        f"Used {bytes_to_gb(disk.used)} / {bytes_to_gb(disk.total)}"
    )

    # Processes
    tb.add_row(
        "🗂️ Processes",
        f"{len(psutil.pids())}",
        "Top process info requires admin to query safely"
    )

    return tb

def main():
    console.print("[bold]Press Q to quit[/bold]")
    with Live(make_table(), refresh_per_second=4, console=console) as live:
        while True:
            # Update table
            live.update(make_table())
            # Small sleep to limit CPU usage
            time.sleep(0.25)
            # Non-blocking key check (Windows only)
            try:
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch.lower() == "q":
                        break
            except ImportError:
                pass

if __name__ == "__main__":
    main()
