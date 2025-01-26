import json

from fastapi import Request, status
from fastapi.responses import JSONResponse
from trainings_app.exceptions.exceptions import RecordNotFoundError, ConvertRecordError


async def record_not_found_handler(request: Request, exc: RecordNotFoundError) -> JSONResponse:
    """Handler for the RecordNotFoundError"""
    detail = exc.detail
    if isinstance(detail, str):
        try:
            json.loads(detail)
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": "RecordNotFoundError",
                    "message": "Invalid JSON format in detail."
                },
            )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": detail.get("error", "Unknown error"),
            "message": detail.get("message", "No message provided"),
            "record_id": detail.get("record_id"),
            "model_name": detail.get("model_name"),
        },
    )


async def convert_record_handler(request: Request, exc: ConvertRecordError) -> JSONResponse:
    """Handler for the ConvertRecordError"""
    status_code = status.HTTP_400_BAD_REQUEST,
    return JSONResponse(
        content={
            "error": "ConvertRecordError",
            "message": str(exc),
            "record": exc.record,
            "model_name": exc.model_name,
            "error_detail": exc.error_detail
        }
    )
