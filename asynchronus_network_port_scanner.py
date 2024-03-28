import asyncio
import ipaddress

async def check_port(ip, port, loop):
    conn = asyncio.open_connection(str(ip), port, loop=loop)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        print(f'Port {port} on {ip} is open')
        writer.close()
        return True
    except:
        return False

async def scan_ip(ip, ports, loop):
    open_ports = []
    for port in ports:
        if await check_port(ip, port, loop):
            open_ports.append(port)
    if open_ports:
        print(f'{ip}: {open_ports}')
    else:
        print(f'{ip} has no open ports or is not responding.')

async def scan_network(network, ports):
    loop = asyncio.get_event_loop()
    tasks = []
    for ip in ipaddress.IPv4Network(network):
        task = loop.create_task(scan_ip(ip, ports, loop))
        tasks.append(task)
    await asyncio.wait(tasks, timeout=5)

if __name__ == '__main__':
    network_range = '192.168.1.0/24'  # Network range to scan
    ports_to_scan = range(1, 1025)  # Ports range to scan
    asyncio.run(scan_network(network_range, ports_to_scan))