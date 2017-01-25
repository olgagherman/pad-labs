#!/usr/bin/env python3.5
import asyncio
import logging
import logging.config

from server import ServerNode
from core import settings
from core.models import Student


logging.config.dictConfig(settings.LOGGING_CONFIG)
LOGGER = logging.getLogger(__name__)


async def run_tasks(nodes):
    tasks = []
    for node in nodes:
        _, pending = await node.run()
        LOGGER.debug('Node %s is running', node.id)
        tasks.extend(pending)
    return tasks

def create_objects():
    result = dict()
    for i in range(1,7):
        tmp = dict()
        for x in range(0,3):
            obj = Student("Viorel", "FI-131", 9.5)
            tmp[x] = obj.__dict__
        result[i] = tmp
    return result

def main():
    loop = asyncio.get_event_loop()
    nodes_data = create_objects()
    nodes = [
        ServerNode(
            node_id=x,
            loop=loop,
            udp_group_address=settings.UDP_GROUP_ADDRESS,
            udp_group_port=settings.UDP_GROUP_PORT,
            **settings.SERVER_CONFIG[x],
            data = nodes_data[x]
        )
        for x in range(1,7)
    ]
    loop.run_until_complete(run_tasks(nodes))
    loop.run_forever()


if __name__ == "__main__":
    # To run all nodes from this script, you might need to remove `run_forever`
    # from the node's run method and return a task/future from it.
    # And execute `run_forever` from this script.
    main()
