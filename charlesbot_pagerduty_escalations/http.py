import asyncio
import aiohttp
import logging
log = logging.getLogger(__name__)


# TODO: Move this to the base library
@asyncio.coroutine
def http_post_request(url,
                      content_type="application/json",
                      payload={}):  # pragma: no cover
    headers = {
        'Content-type': content_type,
    }
    response = yield from aiohttp.post(url, data=payload, headers=headers)
    if not response.status == 200:
        text = yield from response.text()
        log.error("URL: %s" % url)
        log.error("Response status code was %s" % str(response.status))
        log.error(response.headers)
        log.error(text)
        response.close()
        return ""
    return (yield from response.text())
