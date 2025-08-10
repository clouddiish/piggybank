from app.schemas import ErrorResponse

common_responses_dict = {
    # 422 is automatically documented by FastAPI for validation errors
    401: {
        "description": "unauthorized",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "unauthorized"}}},
    },
    500: {
        "description": "internal server error",
        "model": ErrorResponse,
        "content": {"application/json": {"example": {"detail": "internal server error"}}},
    },
}
