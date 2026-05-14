import aiohttp


class HttpClient:
    session: aiohttp.ClientSession | None = None

async def init_http_session():
    if not HttpClient.session or HttpClient.session.closed:
        HttpClient.session = aiohttp.ClientSession()

async def close_http_session():
    if HttpClient.session and not HttpClient.session.closed:
        await HttpClient.session.close()
