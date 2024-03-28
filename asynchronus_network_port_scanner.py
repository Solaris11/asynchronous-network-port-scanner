import asyncio
import ipaddress
from concurrent.futures import FIRST_COMPLETED

async def check_port(ip, port):
    try:
        conn = asyncio.open_connection(str(ip), port)
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        writer.close()
        return port
    except:
        return None

async def scan_ip(ip, ports):
    open_ports = []
    for port in ports:
        result = await check_port(ip, port)
        if result:
            open_ports.append(result)
    return ip, open_ports

async def scan_network(network, ports):
    network = ipaddress.IPv4Network(network)
    tasks = {asyncio.create_task(scan_ip(ip, ports)): ip for ip in network}
    while tasks:
        done, _ = await asyncio.wait(tasks, timeout=5, return_when=FIRST_COMPLETED)
        for task in done:
            ip, open_ports = task.result()
            if open_ports:
                print(f'{ip} open ports: {open_ports}')
            else:
                print(f'{ip} has no open ports or is not responding.')
            # Remove the task from the dictionary
            del tasks[task]

if __name__ == '__main__':
    network_range = '192.168.1.0/24'  # Network range to scan
    ports_to_scan = range(1, 1025)  # Ports range to scan
    asyncio.run(scan_network(network_range, ports_to_scan))