#!/usr/bin/env python3
import psutil
import platform
import curses
import time

def draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)  # allow blocking for key input
    stdscr.keypad(True)

    scroll_offset = 0
    sort_mode = "cpu"  # default sort by CPU

    while True:
        stdscr.clear()
        uname = platform.uname()

        # System Info
        stdscr.addstr(0, 0, f"System: {uname.system} {uname.release} ({uname.machine})")
        stdscr.addstr(1, 0, f"Node: {uname.node} | Kernel: {uname.version}")

        # CPU Info
        cpu_usage = psutil.cpu_percent(interval=0.5, percpu=True)
        stdscr.addstr(3, 0, "=== CPU Usage ===")
        for i, usage in enumerate(cpu_usage):
            stdscr.addstr(4+i, 2, f"Core {i}: {usage}%")

        # Memory Info
        mem_line = 5+len(cpu_usage)+1
        mem = psutil.virtual_memory()
        stdscr.addstr(mem_line, 0, "=== Memory ===")
        stdscr.addstr(mem_line+1, 2, f"Total: {mem.total/(1024**3):.2f} GB")
        stdscr.addstr(mem_line+2, 2, f"Used: {mem.used/(1024**3):.2f} GB ({mem.percent}%)")

        # Disk Info
        disk_line = mem_line+4
        disk = psutil.disk_usage('/')
        stdscr.addstr(disk_line, 0, "=== Disk ===")
        stdscr.addstr(disk_line+1, 2, f"Total: {disk.total/(1024**3):.2f} GB")
        stdscr.addstr(disk_line+2, 2, f"Used: {disk.used/(1024**3):.2f} GB ({disk.percent}%)")

        # Network Info
        net_line = disk_line+4
        net = psutil.net_io_counters()
        stdscr.addstr(net_line, 0, "=== Network ===")
        stdscr.addstr(net_line+1, 2, f"Sent: {net.bytes_sent/(1024**2):.2f} MB")
        stdscr.addstr(net_line+2, 2, f"Recv: {net.bytes_recv/(1024**2):.2f} MB")

        # Process Info
        proc_line = net_line+4
        stdscr.addstr(proc_line, 0, f"=== Processes (↑/↓ scroll, q quit, c sort CPU, m sort MEM) ===")
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            processes.append(p.info)

        # Sort based on mode
        if sort_mode == "cpu":
            processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
        else:
            processes = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)

        # Show 10 processes at a time
        visible_procs = processes[scroll_offset:scroll_offset+10]
        for i, p in enumerate(visible_procs):
            stdscr.addstr(proc_line+1+i, 2,
                          f"PID {p['pid']} {p['name']} | CPU {p['cpu_percent']}% | MEM {p['memory_percent']:.1f}%")

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_DOWN and scroll_offset < len(processes)-10:
            scroll_offset += 1
        elif key == curses.KEY_UP and scroll_offset > 0:
            scroll_offset -= 1
        elif key == ord('c'):
            sort_mode = "cpu"
        elif key == ord('m'):
            sort_mode = "mem"

        time.sleep(0.5)

def main():
    curses.wrapper(draw_dashboard)

if __name__ == "__main__":
    main()
