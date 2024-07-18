import asyncio
import socket
import time

# Dictionary to keep track of connection states
connection_states = {
    'successful': 0,
    'failed': 0,
    'dropped': 0,
}

async def create_tcp_connection(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port, family=socket.AF_INET6)
        connection_states['successful'] += 1
        print(f'Connection established with {host}:{port}')
        
        writer.write(b'Hello Server')
        await writer.drain()
        
        data = await reader.read(100)
        print(f'Received: {data.decode()} from {host}:{port}')
        
        writer.close()
        await writer.wait_closed()
    except ConnectionRefusedError:
        connection_states['failed'] += 1
        print(f'Connection failed to {host}:{port}')
    except (ConnectionResetError, asyncio.IncompleteReadError):
        connection_states['dropped'] += 1
        print(f'Connection dropped with {host}:{port}')
    except Exception as e:
        connection_states['failed'] += 1
        print(f'Error: {e} for {host}:{port}')

async def main(host, port, num_connections):
    tasks = []
    for _ in range(num_connections):
        tasks.append(create_tcp_connection(host, port))
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    ipv6_host = 'your_ipv6_server_address_here'  # Replace with your server's IPv6 address
    port = 80  # Replace with the desired port
    num_connections = 100  # Number of concurrent connections

    start_time = time.time()
    asyncio.run(main(ipv6_host, port, num_connections))
    end_time = time.time()

    print(f'Total time taken: {end_time - start_time} seconds')
    print('Connection states:')
    print(f"Successful connections: {connection_states['successful']}")
    print(f"Failed connections: {connection_states['failed']}")
    print(f"Dropped connections: {connection_states['dropped']}")

