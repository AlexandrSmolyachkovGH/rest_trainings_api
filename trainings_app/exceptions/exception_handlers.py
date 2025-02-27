import json

from fastapi import Request, status, Response
from fastapi.responses import JSONResponse

from trainings_app.exceptions.exceptions import RecordNotFoundError, ConvertRecordError, AccessError
from trainings_app.custom_loggers.main import main_logger


def record_not_found_handler(request: Request, exc: RecordNotFoundError) -> Response:
    """Handler for the RecordNotFoundError"""
    detail = exc.detail
    main_logger.error(f"{str(exc)}")
    if isinstance(detail, str):
        try:
            json.loads(detail)
        except json.JSONDecodeError as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Invalid JSON",
                    "message": f"Invalid JSON format error: {str(e)}",
                },
            )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": detail.get("error", "Unknown error"),
            "message": detail.get("message", "No message provided"),
        },
    )


def convert_record_handler(request: Request, exc: ConvertRecordError) -> Response:
    """Handler for the ConvertRecordError"""
    main_logger.error(f"{str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "ConvertRecordError",
            "message": str(exc),
            "record": exc.record,
            "error_detail": exc.error_detail,
        }
    )


def access_denied_handler(request: Request, exc: AccessError) -> Response:
    """Handler for the AccessError"""
    main_logger.error(f"{str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            'error': 'AccessError',
            'message': str(exc.message) + ': No access to the specified user',
        }
    )
