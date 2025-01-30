import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "honeypot:app",
        host="0.0.0.0",  # noqa: S104 # containerised product
        port=8080,
        workers=2,
        loop="uvloop",
        proxy_headers=True,
        server_header=True,
        date_header=True,
    )
