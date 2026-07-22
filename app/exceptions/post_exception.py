class BlogException(Exception):
    """Base exception for all blog-related errors."""
    pass

class PostNotFoundError(BlogException):
    """Raised when a specific post cannot be found in the database."""
    def __init__(self, post_id: int):
        super().__init__(f"Post with ID {post_id} does not exist.")
        self.post_id = post_id

class PostOperationError(BlogException):
    """Raised when a DB mutation (create, update, delete) fails."""
    pass
