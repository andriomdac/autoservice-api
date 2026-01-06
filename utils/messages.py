from fastapi.responses import JSONResponse


def error_message(
    message: str = "Operação falhou", status_code: int = 400
) -> JSONResponse:
    return JSONResponse({"detail": message}, status_code=status_code)


def success_message(
    message: str = "Operação bem sucedida", status_code: int = 200
) -> JSONResponse:
    return JSONResponse({"success": message}, status_code=status_code)
