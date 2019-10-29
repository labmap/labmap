import re
import subprocess
from multiprocessing.pool import Pool, IMapIterator
from typing import List


def ping_hosts(process_pool: Pool, host_names: List[str]) -> IMapIterator:
    return process_pool.imap_unordered(ping_host, host_names)


def ping_host(host_name: str) -> (str, str):
    command = f'ping -c 1 {host_name}'
    result = subprocess.run(command.split(), stdout=subprocess.PIPE)
    if result.returncode == 0:
        output_string = result.stdout.decode('utf-8')
        state = parse_output(output_string)
    else:
        state = 'off'
    return host_name, state


def parse_output(output: str) -> str:
    ttl_line = output.splitlines()[1]
    match = re.search(r'ttl=(\d+)', ttl_line)
    ttl = int(match.group(1))
    return get_state_from_ttl(ttl)


def get_state_from_ttl(ttl: int) -> str:
    if ttl == 64:
        return 'linux'
    elif ttl == 128:
        return 'windows'
    else:
        return 'off'

