import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from app.commons.common_services import create_bulk_query,add_object,filter_objects_exist
from app.models import DXVLLogs,DXVLLogNames,DXVLUsers
from datetime import datetime
from django.utils import timezone
from dxvl.settings import BATCH_SIZE, PATTERN

def check_filename(filename):
    return filter_objects_exist(DXVLLogNames.objects, file_name=filename)

def time_parser(time_str):
    naive_datetime = datetime.strptime(time_str, '%d-%b-%Y %H:%M:%S')
    aware_datetime = timezone.make_aware(naive_datetime, timezone.get_default_timezone())
    return aware_datetime

def process_line(line, pattern, user):
    match = pattern.match(line)
    if match:
        time, artist, advertisement = match.groups()
        return DXVLLogs(
            date_aired = time_parser(time),
            artist = artist,
            advertisement = advertisement,
            added_by = DXVLUsers.objects.get(username=user)
        )
    
    return None

def process_file(filename, pattern, user):
    processed = 0
    batch = []
    try:

        if check_filename(filename):
            return 'file_exists'
        else:
            for line in filename.read().decode('latin-1').split('\n'):
                result = process_line(line, pattern, user)
                if result:
                    batch.append(result)
                    if len(batch) >= BATCH_SIZE:
                        create_bulk_query(DXVLLogs.objects,batch)
                        processed += len(batch)
                        add_object(DXVLLogNames.objects, file_name=filename,file_state=True,file_lines=processed)
                        batch = []
                        return 'success'

            if batch:
                create_bulk_query(DXVLLogs.objects,batch)
                processed += len(batch)
                add_object(DXVLLogNames.objects, file_name=filename,file_state=True,file_lines=processed)
                return 'success'
            
    except Exception as e:
        return 'file_error'

def parse_dxvl_logs(user,log_files):
    log_pattern = PATTERN

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(process_file, file, log_pattern,user) for key, file in log_files]
        for future in futures:
            result = future.result()
            return result

