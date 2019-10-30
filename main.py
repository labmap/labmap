import time
from multiprocessing.pool import Pool
from typing import List

import click
from click import Context
from tqdm import tqdm

from src.database import initialize_database, Computer
from src.ping import ping_hosts


@click.group()
def cli():
    pass


@cli.command()
@click.option('--interval', 'interval', type=int, default=60, help='Sleep interval length.')
@click.option('--threads', 'thread_count', type=int, default=1, help='Number of threads.')
@click.pass_context
def schedule(ctx: Context, interval: int, thread_count: int):
    while True:
        ctx.invoke(run, thread_count=thread_count)
        sleep_with_tqdm(interval)


def sleep_with_tqdm(seconds: int):
    for _ in tqdm(range(seconds), desc='Sleeping'):
        time.sleep(1)

@cli.command()
@click.option('--threads', 'thread_count', type=int, default=1, help='Number of threads')
def run(thread_count):
    database_path = 'database.db'
    session = initialize_database(database_path)
    computers = session.query(Computer)
    host_names = [computer.id for computer in computers]
    with Pool(thread_count) as pool:
        for host_name, state in ping_hosts_with_tqdm(pool, host_names):
            computers.get(host_name).state = state
    session.commit()


def ping_hosts_with_tqdm(pool: Pool, host_names: List[str]) -> tqdm:
    return tqdm(
        ping_hosts(pool, host_names),
        desc='Pinging hosts',
        unit='host',
        total=len(host_names)
    )


if __name__ == '__main__':
    cli()
