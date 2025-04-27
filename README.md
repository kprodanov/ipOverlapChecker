# IP Overlap Checker

This Python script checks for overlaps between allowed and blocked IP addresses or networks. It supports two modes: expanded IP checks and direct network comparisons.

## Features
- Reads allowed and blocked IP ranges from separate files.
- Supports customizable file separators (comma, space, tab, or automatic whitespace).
- Allows selection of the specific column from input files containing IP addresses/networks.
- Two modes of operation:
  - **Expand Mode**: Expands networks into individual IP addresses and checks for overlaps.
  - **Direct Mode**: Directly compares network entries without expansion.
- Provides detailed logging and feedback on entries processed, skipped, or invalid.

## Requirements

- Python 3.x
- pandas

Install dependencies:
```sh
pip install pandas
```

## Usage

Run the script from the command line:

```sh
python ip_overlap_checker.py
```

You'll be prompted to enter:
- Paths to allowed and blocked IP files.
- File separators.
- Column indices.
- Mode of operation (Expand or Direct).

### Example

```
Enter path to allowed IPs file: allowed_ips.csv
Enter separator for allowed file (e.g., ',' or ' ' or leave empty for auto): ,
Enter the column index for allowed IP ranges (starting at 0): 0

Enter path to blocked IPs file: blocked_ips.txt
Enter separator for blocked file (e.g., ',' or ' ' or leave empty for auto):  
Enter the column index for blocked IP ranges (starting at 0): 1

Choose mode - 1 for Expand IPs (expand) or 2 for Direct match (direct): 1
```

## File Format

Input files should be structured clearly, containing IP ranges in standard CIDR notation (e.g., `192.168.1.0/24`) or individual IP addresses.

## Contributing

If you want to contribute to this project, please check the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
