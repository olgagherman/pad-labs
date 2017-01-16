#!/usr/bin/env python3.5
import asyncio
import logging.config

from server import ServerNode
from core import settings


logging.config.dictConfig(settings.LOGGING_CONFIG)


if __name__ == "__main__":
    # To run all nodes from this script, you might need to remove `run_forever`
    # from the node's run method and return a task/future from it.
    # And execute `run_forever` from this script.
    node = dict()
    for n in range(1,7):
        node[n] = ServerNode(
            id=n,
            loop=asyncio.get_event_loop(),
            udp_group_address=settings.UDP_GROUP_ADDRESS,
            udp_group_port=settings.UDP_GROUP_PORT,
            **settings.SERVER_CONFIG[n],
        )
        t = node[n].run()
        task = node[n].loop.run_until_complete(t)
        node[n].loop.run_forever()
