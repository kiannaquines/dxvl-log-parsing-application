import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from app.commons.common_services import create_bulk_query
from app.models import DXVLLogs
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone

def time_parser(time_str):
    naive_datetime = datetime.strptime(time_str, '%d-%b-%Y %H:%M:%S')
    aware_datetime = timezone.make_aware(naive_datetime, timezone.get_default_timezone())
    return aware_datetime

def process_line(request, line, pattern):
    match = pattern.match(line)
    if match:
        time, artist, advertisement = match.groups()
        return DXVLLogs(
            date_aired = time_parser(time),
            artist = artist,
            advertisement = advertisement,
            added_by = request.user,
        )
    return None

def process_file(filename, pattern, request):
    processed = 0
    batch = []
    batch_size = 1000
    try:
        for line in filename.read().decode('latin-1').split('\n'):
            result = process_line(request, line, pattern)
            if result:
                batch.append(result)
                if len(batch) >= batch_size:
                    create_bulk_query(DXVLLogs.objects,batch)
                    processed += len(batch)
                    batch = []
        if batch:
            create_bulk_query(DXVLLogs.objects,batch)
            processed += len(batch)
    except Exception as e:
        print(f"Error processing {filename}: {e}")

def parse_dxvl_logs(request,log_files):
    log_pattern = re.compile(r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)")
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(process_file, file, log_pattern, request) for key, file in log_files]
        for future in futures:
            future.result()
    return HttpResponse("DXVL logs parsed successfully")
