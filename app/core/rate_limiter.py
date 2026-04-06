from fastapi import Request
import time

# simple in-memory store
request_log = {}

MAX_REQUESTS = 10
WINDOW_SECONDS = 60


def rate_limiter(request: Request):
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_log:
        request_log[client_ip] = []

    # remove old requests
    request_log[client_ip] = [
        t for t in request_log[client_ip]
        if t > current_time - WINDOW_SECONDS
    ]

    if len(request_log[client_ip]) >= MAX_REQUESTS:
        raise Exception("Too many requests. Slow down.")

    request_log[client_ip].append(current_time)