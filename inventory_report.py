import argparse
import sys
import requests
from registry_client import RegistryClient

def fetch_all(client, status=None):
    collected, offset, limit = [], 0, 10
    while True:
        page = client.get_services(limit=limit, offset=offset, status=status)
        collected.extend(page["results"])
        offset += limit
        if offset >= page["count"]:
            break
    return collected

def main():
    parser = argparse.ArgumentParser(description="AeroPay Service Registry Inventory Report")
    parser.add_argument("--status", default=None, help="Filter by status (healthy | unhealthy | maintenance)")
    args = parser.parse_args()

    client = RegistryClient()
    try:
        services = fetch_all(client, status=args.status)
    except requests.exceptions.RequestException as exc:
        print(f"Error: Unable to reach AeroPay Registry API ({exc})")
        sys.exit(0)

    header = f"{'ID':<4} | {'NAME':<20} | {'VERSION':<8} | {'STATUS':<12} | {'ENVIRONMENT':<12}"
    print(header)
    print("-" * len(header))
    for s in services:
        sid = str(s.get("id", ""))
        name = str(s.get("name", ""))
        version = str(s.get("version", ""))
        status = str(s.get("status", ""))
        env = str(s.get("environment", ""))
        print(f"{sid:<4} | {name:<20} | {version:<8} | {status:<12} | {env:<12}")

if __name__ == "__main__":
    main()