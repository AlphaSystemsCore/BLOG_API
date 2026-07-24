class CommentException(Exception):
    """Base Exception for all comment related errors"""
    pass

class CommentOperationalError(CommentException):
    """Raised when a database operation fails(CRUD)"""
    pass