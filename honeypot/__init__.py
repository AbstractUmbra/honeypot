from __future__ import annotations

import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import Response

from .image import generate_honeypot_image

app = FastAPI(debug=False, title="Welcome!", version="0.0.1", openapi_url=None, redoc_url=None, docs_url=None)


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"])  # type: ignore # starlette upstream bad types
async def index(request: Request, full_path: str) -> Response:
    assert request.client

    source_ip = request.headers.get("x-forwarded-for") or request.client.host
    headers = request.headers

    image = await asyncio.to_thread(generate_honeypot_image, source_ip, request.url.path, request.method.upper(), headers)

    return Response(content=image.read(), media_type="image/png")
