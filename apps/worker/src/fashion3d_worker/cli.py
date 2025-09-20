from __future__ import annotations

import click
import rq
from redis import Redis

from .config import settings
from .logging import logger, setup_logging


@click.group()
def cli() -> None:
    """Fashion3D worker command line."""


@cli.command()
def worker() -> None:
    """Start an RQ worker that processes reconstruction jobs."""
    setup_logging()
    redis = Redis.from_url(settings.redis_url)
    queue = rq.Queue("fashion3d", connection=redis)
    worker = rq.Worker([queue], connection=redis)
    logger.info("worker.start", queue=queue.name, gpu=settings.gpu_enabled)
    worker.work()


if __name__ == "__main__":
    cli()
