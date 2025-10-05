import asyncio


def run_sync(coro):
    return asyncio.run(coro)

