from __future__ import annotations

import asyncio
from typing import Any

from litestar import HttpMethod, Litestar, Request, route

from .image import generate_honeypot_image


@route(path=["/", "/{full_path:path}"], http_method=list(HttpMethod), media_type="image/png")
async def index(request: Request[Any, Any, Any], full_path: str = "/") -> bytes:
    assert request.client

    source_ip = request.headers.get("x-forwarded-for") or request.client.host
    headers = request.headers

    image = await asyncio.to_thread(generate_honeypot_image, source_ip, full_path, request.method.upper(), headers)

    return image.read()


app = Litestar(route_handlers=[index])
