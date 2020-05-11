import psutil
from datetime import datetime
import pandas as pd
import time
import os

def get_process_info():
	#list contains all the process
	processes = []

	for process in psutil.process_iter():
		# get all the process info using loop
		with process.oneshot():
			#get the process id
			pid = process.pid
			if pid == 0:
				# System Idle Process for Windows
				continue

			# Get the name of the file executed
			name = process.name()

			# Get the time process was spawed
			try:
				create_time = datetime.fromtimestamp(process.create_time())
			except OSError:
				#System processes, using boot time instead
				create_time = datetime.fromtimestamp(psutil.boot_time())


			try:
				#Get the number of CPU Cores
				cores = len(process.cpu_affinity())
			except psutil.AccessDenied:
				cores = 0

			# Get the CPU uses percentage
			cpu_usage = process.cpu_percent()

			# Get the status of the process
			status = process.status()

			try:
				#get the process priority
				nice = int(process.nice())
			except psutil.AccessDenied:
				nice = 0

			#Memory Usage
			try:
				# get the memory usage
				memory_usage = process.memory_full_info().uss
			except psutil.AccessDenied:
				memory_usage = 0
				
			#total process read and written bytes
			io_counters = process.io_counters()
			read_bytes = io_counters.read_bytes
			write_bytes = io_counters.write_bytes


			# Total Threads spawned
			n_threads =  process.num_threads()

			# get the username spawned the process
			try:
				username = process.username()
			except psutil.AccessDenied:
				username = "N/A"

			# add all these info to our list

			processes.append({
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
            'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads, 'username': username,})
	return processes

#DataFrame of the processeses
def construct_dataframe(processes):
    # convert to pandas dataframe
    df = pd.DataFrame(processes)
    # set the process id as index of a process
    df.set_index('pid', inplace=True)
    # sort rows by the column passed as argument
    df.sort_values(sort_by, inplace=True, ascending=not descending)
    # pretty printing bytes
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    # reorder and define used columns
    df = df[columns.split(",")]
    return df    							
				
#size fun()
def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process Viewer & Monitor")
    parser.add_argument("-c", "--columns", help="""Columns to show,
                                                available are name,create_time,cores,cpu_usage,status,nice,memory_usage,read_bytes,write_bytes,n_threads,username.
                                                Default is name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores.""",
                        default="name,cpu_usage,memory_usage,read_bytes,write_bytes,status,create_time,nice,n_threads,cores")
    parser.add_argument("-s", "--sort-by", dest="sort_by", help="Column to sort by, default is memory_usage .", default="memory_usage")
    parser.add_argument("--descending", action="store_true", help="Whether to sort in descending order.")
    parser.add_argument("-n", help="Number of processes to show, will show all if 0 is specified, default is 25 .", default=25)
    parser.add_argument("-u", "--live-update", action="store_true", help="Whether to keep the program on and updating process information each second")

    # parse arguments
    args = parser.parse_args()
    columns = args.columns
    sort_by = args.sort_by
    descending = args.descending
    n = int(args.n)
    live_update = args.live_update



	# print the processes for the first time
    processes = get_process_info()
    df = construct_dataframe(processes)
    if n == 0:
        print(df.to_string())
    elif n > 0:
        print(df.head(n).to_string())
    # print continuously
    while live_update:
        # get all process info
        processes = get_processes_info()
        df = construct_dataframe(processes)
        # clear the screen depending on your OS
        os.system("cls") if "nt" in os.name else os.system("clear")
        if n == 0:
            print(df.to_string())
        elif n > 0:
            print(df.head(n).to_string())
        time.sleep(0.7)