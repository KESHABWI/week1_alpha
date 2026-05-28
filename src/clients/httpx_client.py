import httpx
from src.config.settings import settings


def create_http_client() -> httpx.AsyncClient:

    limits = httpx.Limits(
        max_connections=settings.HTTP_MAX_CONNECTIONS,
        max_keepalive_connections=settings.HTTP_KEEPALIVE_CONNECTIONS,
    )

    timeout = httpx.Timeout(
        connect=10.0,
        read=30.0,
        write=30.0,
        pool=5.0,
    )

    return httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
        http2=True,  # modern production APIs support this
    )


# singleton instance (used across app)
httpx_client = create_http_client()
