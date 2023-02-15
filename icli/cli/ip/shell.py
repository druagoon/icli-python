import netifaces

from .cli import cli_ip

EXCLUDE_IP = {'127.0.0.1', 'localhost'}


@cli_ip.command()
def shell():
    """Show local machine ip address."""
    ips = []
    for iface in netifaces.interfaces():
        info = netifaces.ifaddresses(iface)
        network = info.get(netifaces.AF_INET)
        if not network:
            continue
        addresses = {n['addr'] for n in network if n['addr'] not in EXCLUDE_IP}
        if addresses:
            ips.append((iface, ' '.join(addresses)))
    ips.sort(key=lambda x: x[1])
    shell_prompt = [f'{i}={v}' for i, v in ips]
    output = '  '.join(shell_prompt)
    print(output)
