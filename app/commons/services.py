from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def all_objects(object):
    return object.all()

def filter_objects(object, filter_criteria):
    return object.filter(*filter_criteria)

def order_objects(object, order_criteria):
    return object.order_by(*order_criteria)

def get_object_by_id(object, id):
    return object.get(pk=id)