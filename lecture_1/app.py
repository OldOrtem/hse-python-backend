
import json
import math
from urllib.parse import parse_qs


async def app(scope, receive, send) -> None:
    path = scope["path"]
    method = scope["method"]
    query_params = parse_qs(scope["query_string"].decode("utf-8"))
    
    content, status_code = {"error": "Not Found"}, 404
    
    if method == "GET":
        if path == "/factorial":
            content, status_code = await factorial(query_params)
        elif path.startswith("/fibonacci"):
            content, status_code = await fibonacci(path)
        elif path == "/mean":
            content, status_code = await mean(receive)

    await send_response(send, content, status_code)


async def factorial(query_params):
    n_str = query_params.get("n", [None])[0]

    if n_str is None:
        return {"error": "Parameter n is required"}, 422

    try:
        n = int(n_str)
    except ValueError:
        return {"error": "Parameter n must be an integer"}, 422

    if n < 0:
        return {"error": "Invalid value for n, must be non-negative"}, 400

    result = math.factorial(n)
    return {"result": result}, 200


async def fibonacci(path):
    n_str = path.split("/")[-1]

    if n_str is None:
        return {"error": "Parameter n is required"}, 422

    try:
        n = int(n_str)
    except ValueError:
        return {"error": "Parameter n must be an integer"}, 422

    if n < 0:
        return {"error": "Invalid value for n, must be non-negative"}, 400

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    result = b
    return {"result": result}, 200


async def mean(receive):
    body = await receive()

    if body["type"] == "http.request":
        try:
            data = json.loads(body["body"])
        except json.JSONDecodeError:
            return {"error": "Request body must be valid JSON"}, 422

        if not isinstance(data, list):
            return {"error": "Request body must be an array"}, 422

        if len(data) == 0:
            return {"error": "Array cannot be empty"}, 400

        try:
            float_data = [float(x) for x in data]
        except ValueError:
            return {"error": "All elements must be numbers"}, 422

        result = sum(float_data) / len(float_data)
        return {"result": result}, 200


async def send_response(send, content, status_code = 200):
    response = json.dumps(content).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status_code,
            "headers": [(b"content-type", b"application/json")],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": response,
        }
    )