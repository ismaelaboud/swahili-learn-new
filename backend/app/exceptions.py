class SearchException(Exception):
    """
    Exception raised for errors in the search service
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseException(Exception):
    """
    Exception raised for database-related errors
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ValidationException(Exception):
    """
    Exception raised for validation errors
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
