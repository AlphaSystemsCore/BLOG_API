class TagExceptions(Exception):
   """parent tags exception"""
   pass

class TagOperationalError(TagExceptions):
    """any CRUD related error"""
    pass