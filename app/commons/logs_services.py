import re
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from app.commons.common_services import create_bulk_query
from app.models import DXVLLogs

def time_parser(time_str):
    return datetime.strptime(time_str, '%d-%b-%Y %H:%M:%S')

def process_line(line, pattern):
    match = pattern.match(line)
    if match:
        time, artist, advertisement = match.groups()
        return (time_parser(time), artist, advertisement)
    return None

def process_file(filename, pattern):
    processed = 0
    batch = []
    batch_size = 1000
    try:
        with open(filename,'r') as file:
            for line in file:
                result = process_line(line, pattern)
                if result:
                    batch.append(result)
                    if len(batch) >= batch_size:
                        create_bulk_query(DXVLLogs,batch)
                        processed += len(batch)
                        batch = []
        if batch:
            create_bulk_query(DXVLLogs,batch)
            processed += len(batch)
        
        print(f"Completed: {filename}, Processed: {processed} entries")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

def parse_dxvl_logs(log_files):
    log_pattern = re.compile(r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)")

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(process_file, file, log_pattern) for file in log_files]
        for future in futures:
            future.result()

    pass
