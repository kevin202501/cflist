import sys
import ipaddress
import dns.resolver
import dns.rdatatype
from concurrent.futures import ThreadPoolExecutor, as_completed

DNS_FILE = "dns.txt"
V4_FILE = "ipv4result.txt"
V6_FILE = "ipv6result.txt"


def load_dns_servers():
    with open(DNS_FILE) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def resolve(domain, dns_ip):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_ip]
    resolver.timeout = 3
    resolver.lifetime = 5
    ips = set()
    for rtype in (dns.rdatatype.A, dns.rdatatype.AAAA):
        try:
            answers = resolver.resolve(domain, rtype)
            for rdata in answers:
                ips.add(rdata.address)
        except Exception:
            pass
    return dns_ip, ips


def main():
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Enter domain: ").strip()

    dns_servers = load_dns_servers()
    all_ips = set()

    with ThreadPoolExecutor(max_workers=50) as pool:
        futures = {pool.submit(resolve, domain, dns): dns for dns in dns_servers}
        for f in as_completed(futures):
            _, ips = f.result()
            all_ips.update(ips)

    v4 = sorted(ip for ip in all_ips if isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address))
    v6 = sorted(ip for ip in all_ips if isinstance(ipaddress.ip_address(ip), ipaddress.IPv6Address))

    def write_results(filepath, new_ips):
        old_ips = set()
        try:
            with open(filepath) as f:
                old_ips = {line.strip() for line in f if line.strip()}
        except FileNotFoundError:
            pass
        deduped = new_ips | (old_ips - new_ips)
        ordered = sorted(
            (ip for ip in deduped),
            key=lambda x: (0 if x in new_ips else 1, x),
        )
        with open(filepath, "w") as f:
            f.write("\n".join(ordered) + "\n")

    write_results(V4_FILE, set(v4))
    write_results(V6_FILE, set(v6))

    print(f"IPv4 ({len(v4)}) -> {V4_FILE}")
    print(f"IPv6 ({len(v6)}) -> {V6_FILE}")
    print(f"Total unique IPs for {domain}: {len(all_ips)}")


if __name__ == "__main__":
    main()
