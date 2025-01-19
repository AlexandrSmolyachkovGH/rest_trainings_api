from fastapi import HTTPException, status


class ConvertRecordError(Exception):
    def __init__(self, record: dict, model_name: str, error_detail: str):
        self.record = record
        self.model_name = model_name
        self.error_detail = error_detail
        message = f"Failed to convert record to {model_name}: {error_detail}"
        super.__init__(message)


class RecordNotFoundError(HTTPException):
    def __init__(self, record_id: str, model_name: str):
        detail = {
            "error": "RecordNotFoundError",
            "message": f"Record with ID '{record_id}' not found in {model_name}.",
            "record_id": record_id,
            "model_name": model_name,
        }
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AttrError(ValueError):
    pass
