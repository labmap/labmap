from multiprocessing.pool import Pool
from typing import List

import click
from tqdm import tqdm

from src.database import initialize_database, Computer
from src.ping import ping_hosts


@click.command()
@click.option('--threads', 'thread_count', type=int, default=1, help='Number of threads')
@click.option('--database', 'database_path', type=str, default='database.db', help='Database path')
def run(database_path, thread_count):
    session = initialize_database(database_path)
    computers = session.query(Computer)
    host_names = [computer.id for computer in computers]
    with Pool(thread_count) as pool:
        for host_name, state in ping_hosts_with_tqdm(pool, host_names):
            computers.get(host_name).state = state
    session.commit()


def ping_hosts_with_tqdm(pool: Pool, host_names: List[str]):
    return tqdm(
        ping_hosts(pool, host_names),
        desc='Pinging hosts',
        unit='host',
        total=len(host_names)
    )


if __name__ == '__main__':
    run()
