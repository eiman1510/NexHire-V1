import time
from fastapi import Request

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    # Start timer
    start_time = time.time()

    # Execute the requested endpoint
    response = await call_next(request)

    # Stop timer
    end_time = time.time()

    print(
        f"{request.method} {request.url.path} "
        f"took {end_time - start_time:.4f} seconds"
    )

    return response