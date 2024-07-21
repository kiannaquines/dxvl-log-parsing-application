def all_objects(object):
    return object.all()

def filter_objects(object, **kwargs):
    return object.filter(**kwargs)

def order_objects(object, **kwargs):
    return object.order_by(**kwargs)

def get_object_by_id(object, id):
    return object.get(pk=id)

def create_bulk_query(object, batch):
    return object.bulk_create(batch)