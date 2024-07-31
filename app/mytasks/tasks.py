from celery import shared_task

@shared_task
def remove_pdf_files():
    print("Remove PDF Files")
