def api_response(
    api_source: str, data=None, message="Success", status_code=200, error_code="0"
):
    return {
        "status_code": status_code,
        "message": message,
        "success": 1 if status_code < 400 else 0,
        "data": data if data is not None else [],
        "error_code": error_code,
        "source": api_source,
    }
