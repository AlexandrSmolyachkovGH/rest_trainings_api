class RepositoryError(Exception):
    ...


class CreateRecordError(RepositoryError):
    def __init__(self):
        message = f"Client creation failed. Please try again later."
        super().__init__(message)


class ConvertRecordError(RepositoryError):
    def __init__(self, record: dict, error_detail: str):
        self.record = record
        self.error_detail = error_detail
        message = f"Failed to convert record: {error_detail}"
        super().__init__(self.record, self.error_detail, message)


class RecordNotFoundError(RepositoryError):
    def __init__(self):
        self.detail = {
            "error": "RecordNotFoundError",
            "message": f"Record not found Error."
        }
        super().__init__(self.detail)


class AttrError(ValueError):
    pass


class TokenError(ValueError):
    pass


class AccessError(Exception):
    """Error with access to the source."""

    def __init__(self, message="Access Denied"):
        self.message = message
        super().__init__(self.message)


class UninitializedDatabasePoolError(Exception):
    def __init__(self, message="The database connection pool has not been properly initialized."):
        self.message = message
        super().__init__(self.message)
