import asyncio
import ipaddress


async def check_port(ip, port):
    conn = asyncio.open_connection(str(ip), port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        writer.close()
        return True
    except:
        return False


async def scan_ip(ip, ports):
    open_ports = []
    for port in ports:
        if await check_port(ip, port):
            open_ports.append(port)
    return (str(ip), open_ports)


async def scan_network(network, ports):
    loop = asyncio.get_event_loop()
    network = ipaddress.IPv4Network(network)
    tasks = [loop.create_task(scan_ip(ip, ports)) for ip in network]
    completed, pending = await asyncio.wait(tasks, timeout=5, return_when=asyncio.ALL_COMPLETED)

    for task in completed:
        ip, open_ports = task.result()
        if open_ports:
            print(f'{ip}: {open_ports}')
        else:
            print(f'{ip} has no open ports or is not responding.')


if __name__ == '__main__':
    network_range = '192.168.1.0/24'  # Network range to scan
    ports_to_scan = range(1, 1025)  # Ports range to scan
    asyncio.run(scan_network(network_range, ports_to_scan))