import asyncio
import aiohttp
import time
from itertools import cycle

# Dictionary to keep track of connection states
connection_states = {
    'successful': 0,
    'failed': 0,
    'dropped': 0,
}

async def create_http_connection(src_ip, dst_ip, port):
    connector = aiohttp.TCPConnector(local_addr=(src_ip, 0), family=socket.AF_INET6)
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(f'https://[{dst_ip}]:{port}') as response:
                if response.status == 200:
                    connection_states['successful'] += 1
                    print(f'HTTP connection established from {src_ip} to [{dst_ip}]:{port}')
                else:
                    connection_states['failed'] += 1
                    print(f'HTTP connection failed from {src_ip} to [{dst_ip}]:{port} with status {response.status}')
    except Exception as e:
        connection_states['failed'] += 1
        print(f'Error: {e} from {src_ip} to [{dst_ip}]:{port}')

async def main(src_ips, dst_ips, port, num_connections):
    tasks = []
    for src_ip, dst_ip in zip(cycle(src_ips), dst_ips * (num_connections // len(dst_ips))):
        tasks.append(create_http_connection(src_ip, dst_ip, port))
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    dst_ips = [
        '2001:4860:4860::8888',  # Replace with dst server's IPv6 addresses
        '2001:4860:4860::8844',  # Add more addresses as needed
    ]
    src_ips = [
        '2001:db8::1',  # Replace with EC2 (enX0) source IPv6 addresses
        '2001:db8::2',  # Add second (enX1) EC2 IPv6 addresses as needed
    ]
    port = 443  # Replace with the desired port
    num_connections = 350  # Number of concurrent connections

    start_time = time.time()
    asyncio.run(main(src_ips, dst_ips, port, num_connections))
    end_time = time.time()

    print(f'Total time taken: {end_time - start_time} seconds')
    print('Connection states:')
    print(f"Successful connections: {connection_states['successful']}")
    print(f"Failed connections: {connection_states['failed']}")
    print(f"Connections dropped: {connection_states['dropped']}")

