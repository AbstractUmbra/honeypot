import os

import uvicorn

if __name__ == "__main__":
    host = "127.0.0.1" if os.getenv("HONEYPOT") else "0.0.0.0"  # noqa: S104 # acceptable
    port = int(os.getenv("WEB_PORT", "8080"))
    conf = uvicorn.Config(
        "honeypot:app",
        host=host,
        port=port,
        workers=5,
        proxy_headers=True,
        server_header=True,
        date_header=True,
        forwarded_allow_ips="*",
        loop="uvloop",
    )
    server = uvicorn.Server(conf)

    server.run()
