from django.core.paginator import Paginator

def all_objects(object):
    return object.all()

def all_objects_only(object,*fields):
    return object.only(*fields)

def all_objects_only_with_order_limit(object,*fields,limit):
    return object.only(*fields).order_by('-date_aired')[:limit]

def all_objects_only_with_order(object,*fields):
    return object.only(*fields).order_by('-date_aired')

def filter_objects_exist(object, **kwargs):
    return object.filter(**kwargs).exists()

def filter_objects(object, **kwargs):
    return object.filter(**kwargs)

def filter_objects_count(object, **kwargs):
    return object.filter(**kwargs).count()

def order_objects(object, **kwargs):
    return object.order_by(**kwargs)

def get_object_by_id(object, id):
    return object.get(pk=id)

def add_object(object, **kwargs):
    return object.create(**kwargs)

def create_bulk_query(object, batch):
    return object.bulk_create(batch)

def count_objects(object):
    return object.count()

def pagination(queryset, page_number, per_page):
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj