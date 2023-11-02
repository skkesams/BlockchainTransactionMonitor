from core.utils import log_exception

from core.unconfirmed_transations import get_transaction


async def handle_request(limit):
    try:
        data = await get_transaction(limit)
        return data
    except Exception as e:
        log_exception(e, "Error while handling request")
    return []
