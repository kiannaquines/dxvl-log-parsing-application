import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def parse_dxvl_logs(log,**kwargs):
    batch = []
    log_pattern = re.compile(r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)")
    pass
