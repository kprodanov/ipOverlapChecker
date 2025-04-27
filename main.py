import ipaddress
import pandas as pd


def read_ip_ranges(file_path, separator, column_index, label):
    try:
        if separator == '':
            print(f"[{label}] Using automatic whitespace separator.")
            df = pd.read_csv(file_path, delim_whitespace=True, header=None, engine='python')
        else:
            print(f"[{label}] Using separator '{separator}'.")
            df = pd.read_csv(file_path, sep=separator, header=None, engine='python')

        if column_index >= len(df.columns):
            print(f"[{label}] Error: Selected column {column_index} doesn't exist in {file_path}.")
            return []

        ip_ranges = []
        for idx, entry in enumerate(df[column_index]):
            if pd.isna(entry):
                print(f"[{label}] Row {idx}: Empty entry skipped.")
                continue
            entry = str(entry).strip()
            if not entry:
                print(f"[{label}] Row {idx}: Blank entry skipped.")
                continue
            try:
                if '/' in entry:
                    network = ipaddress.ip_network(entry, strict=False)
                    ip_ranges.append(network)
                    print(f"[{label}] Row {idx}: Added network {network}")
                else:
                    ip = ipaddress.ip_address(entry)
                    network = ipaddress.ip_network(f"{ip}/{32 if ip.version == 4 else 128}", strict=False)
                    ip_ranges.append(network)
                    print(f"[{label}] Row {idx}: Added IP {ip}")
            except ValueError:
                print(f"[{label}] Row {idx}: Invalid IP/network skipped -> {entry}")
        return ip_ranges
    except Exception as e:
        print(f"Failed to read {label} file {file_path}: {e}")
        return []


def expand_networks(networks):
    expanded_ips = {}
    for net in networks:
        for ip in net.hosts():
            expanded_ips[str(ip)] = net
    return expanded_ips


def main():
    allowed_file = input("Enter path to allowed IPs file: ")
    allowed_separator = input("Enter separator for allowed file (e.g., ',' or ' ' or leave empty for auto): ").strip()
    allowed_column = int(input("Enter the column index for allowed IP ranges (starting at 0): "))

    blocked_file = input("Enter path to blocked IPs file: ")
    blocked_separator = input("Enter separator for blocked file (e.g., ',' or ' ' or leave empty for auto): ").strip()
    blocked_column = int(input("Enter the column index for blocked IP ranges (starting at 0): "))

    mode = input("Choose mode - 1 for Expand IPs (expand) or 2 for Direct match (direct): ").strip()

    if mode == '1':
        mode = 'expand'
    elif mode == '2':
        mode = 'direct'
    else:
        print("Invalid choice. Defaulting to expand.")
        mode = 'expand'

    print("\n--- Processing Allowed IPs ---\n")
    allowed_networks = read_ip_ranges(allowed_file, allowed_separator, allowed_column, label="Allowed")

    print("\n--- Processing Blocked IPs ---\n")
    blocked_networks = read_ip_ranges(blocked_file, blocked_separator, blocked_column, label="Blocked")

    if mode == 'expand':
        print("\nExpanding allowed IPs...")
        allowed_ips = expand_networks(allowed_networks)
        print(f"Total allowed IPs expanded: {len(allowed_ips)}")

        print("Expanding blocked IPs...")
        blocked_ips = expand_networks(blocked_networks)
        print(f"Total blocked IPs expanded: {len(blocked_ips)}")

        print("\nChecking for allowed IPs that are blocked...\n")
        blocked_allowed_ips = set(allowed_ips.keys()).intersection(set(blocked_ips.keys()))

        if blocked_allowed_ips:
            print("The following allowed IPs/networks are blocked:")
            for ip in blocked_allowed_ips:
                print(f"{ip} is part of allowed network {allowed_ips[ip]}")
        else:
            print("No allowed IPs are blocked.")

    elif mode == 'direct':
        print("\nChecking for direct network matches...\n")
        allowed_set = set(str(net) for net in allowed_networks)
        blocked_set = set(str(net) for net in blocked_networks)

        blocked_allowed = allowed_set.intersection(blocked_set)

        if blocked_allowed:
            print("The following allowed networks are blocked:")
            for net in blocked_allowed:
                print(net)
        else:
            print("No allowed networks are blocked.")


if __name__ == "__main__":
    main()
