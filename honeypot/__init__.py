from __future__ import annotations

import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import Response

from .image import generate_honeypot_image

app = FastAPI(debug=True, title="Welcome!", version="0.0.1", openapi_url=None, redoc_url=None, docs_url=None)


# @app.get("/")
@app.route("/")  # type: ignore # starlette upstream bad types
async def index(request: Request) -> Response:
    assert request.client

    source_ip = request.headers.get("x-forwarded-for") or request.client.host
    headers = request.headers

    image = await asyncio.to_thread(
        generate_honeypot_image, source_ip, request.base_url.path, request.method.upper(), headers
    )

    return Response(content=image.read(), media_type="image/png")
