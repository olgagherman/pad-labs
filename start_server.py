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
    node = ServerNode(
        asyncio.get_event_loop(),
        udp_group_address=settings.UDP_GROUP_ADDRESS,
        udp_group_port=settings.UDP_GROUP_PORT,
        **settings.SERVER_CONFIG[1],
    )
    node.run()
