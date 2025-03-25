import sys
import re
from datetime import datetime
from collections import defaultdict

def read_log():
    """
    Reads HTTP logs from stdin and returns a list of tuples representing each entry.
    Each tuple contains: (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri)
    """
    log_entries = []
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        # Split the line into fields (assuming tab-separated values)
        fields = line.split('\t')
        
        try:
            # Extract relevant fields and convert to appropriate types
            ts = float(fields[0]) if fields[0] else None
            uid = fields[1] if len(fields) > 1 else None
            id_orig_h = fields[2] if len(fields) > 2 else None
            id_orig_p = int(fields[3]) if len(fields) > 3 and fields[3] else None
            id_resp_h = fields[4] if len(fields) > 4 else None
            id_resp_p = int(fields[5]) if len(fields) > 5 and fields[5] else None
            method = fields[7] if len(fields) > 7 else None
            host = fields[8] if len(fields) > 8 else None
            uri = fields[9] if len(fields) > 9 else None
            
            # Create a tuple for the entry and add to the list
            entry = (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri)
            log_entries.append(entry)
            
        except (IndexError, ValueError) as e:
            print(f"Error processing line: {line}\nError: {e}", file=sys.stderr)
            continue
            
    return log_entries

def sort_log(log, index):
    """
    Sorts the log entries based on the specified index in the tuple.
    Handles cases where index might be out of range.
    """
    try:
        return sorted(log, key=lambda x: x[index] if x[index] is not None else '')
    except IndexError:
        print(f"Index {index} is out of range for log entries", file=sys.stderr)
        return log

def validate_ip(ip):
    """Validates an IPv4 address"""
    if not ip:
        return False
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(part) <= 255 for part in ip.split('.'))

def validate_domain(domain):
    """Validates a domain name"""
    if not domain:
        return False
    pattern = r'^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None

def get_entries_by_addr(log, addr):
    """
    Returns entries from the log that match the given IP address or domain name.
    Validates the address before searching.
    """
    if not (validate_ip(addr) or validate_domain(addr)):
        print(f"Invalid address: {addr}", file=sys.stderr)
        return []
    
    return [entry for entry in log if entry[2] == addr or entry[7] == addr]

def validate_http_code(code):
    """Validates an HTTP status code"""
    try:
        code_int = int(code)
        return 100 <= code_int <= 599
    except (ValueError, TypeError):
        return False

def get_entries_by_code(log, code):
    """
    Returns entries from the log that have the specified HTTP status code.
    Validates the code before searching.
    """
    if not validate_http_code(code):
        print(f"Invalid HTTP status code: {code}", file=sys.stderr)
        return []
    
    return [entry for entry in log if len(entry) > 8 and str(entry[8]).startswith(str(code))]

def get_failed_reads(log, merge=False):
    """
    Returns entries with HTTP 4xx or 5xx status codes.
    If merge is True, returns a single combined list, otherwise returns separate lists.
    """
    client_errors = [entry for entry in log if len(entry) > 8 and str(entry[8]).startswith('4')]
    server_errors = [entry for entry in log if len(entry) > 8 and str(entry[8]).startswith('5')]
    
    if merge:
        return client_errors + server_errors
    else:
        return (client_errors, server_errors)

def get_entries_by_extension(log, extension):
    """
    Returns entries that request resources with the specified file extension.
    """
    if not extension:
        return []
    
    # Ensure extension doesn't start with a dot
    ext = extension.lower().lstrip('.')
    pattern = re.compile(r'\.' + re.escape(ext) + r'($|\?|#)', re.IGNORECASE)
    
    return [entry for entry in log if len(entry) > 8 and entry[8] and pattern.search(entry[8])]

def entry_to_dict(entry):
    """
    Converts a log entry tuple to a dictionary with descriptive keys.
    """
    if not entry or len(entry) < 9:
        return {}
    
    return {
        'timestamp': entry[0],
        'uid': entry[1],
        'source_ip': entry[2],
        'source_port': entry[3],
        'dest_ip': entry[4],
        'dest_port': entry[5],
        'method': entry[6],
        'host': entry[7],
        'uri': entry[8]
    }

def log_to_dict(log):
    """
    Converts the entire log to a dictionary where keys are UIDs and values are lists of entry dictionaries.
    """
    log_dict = defaultdict(list)
    
    for entry in log:
        if len(entry) > 1 and entry[1]:  # Check if UID exists
            log_dict[entry[1]].append(entry_to_dict(entry))
    
    return dict(log_dict)

def print_dict_entry_dates(log_dict):
    """
    Prints statistics about the log entries in a readable format.
    """
    for uid, entries in log_dict.items():
        if not entries:
            continue
            
        # Get all unique source IPs/hosts for this UID
        ips = set(entry.get('source_ip', '') for entry in entries)
        hosts = set(entry.get('host', '') for entry in entries)
        
        # Count requests
        request_count = len(entries)
        
        # Get timestamps and convert to datetime
        timestamps = [entry.get('timestamp') for entry in entries if entry.get('timestamp') is not None]
        if timestamps:
            first_request = datetime.fromtimestamp(min(timestamps))
            last_request = datetime.fromtimestamp(max(timestamps))
        else:
            first_request = last_request = "N/A"
        
        # Count methods
        method_counts = defaultdict(int)
        for entry in entries:
            method = entry.get('method', 'UNKNOWN')
            method_counts[method] += 1
        
        # Calculate method percentages
        method_percentages = []
        for method, count in method_counts.items():
            percentage = (count / request_count) * 100
            method_percentages.append(f"{method} - {percentage:.1f}%")
        
        # Count successful requests (2xx)
        success_count = sum(1 for entry in entries 
                          if str(entry.get('status_code', '')).startswith('2'))
        success_ratio = (success_count / request_count) * 100 if request_count > 0 else 0
        
        # Print the information
        print(f"\nSession UID: {uid}")
        print(f"Source IPs: {', '.join(ip for ip in ips if ip)}")
        print(f"Hosts: {', '.join(host for host in hosts if host)}")
        print(f"Number of requests: {request_count}")
        print(f"First request: {first_request}")
        print(f"Last request: {last_request}")
        print("Method distribution:")
        for method_pct in method_percentages:
            print(f"  {method_pct}")
        print(f"Success ratio (2xx): {success_ratio:.1f}%")

if __name__ == "__main__":
    # Example usage
    print("Reading log entries from stdin...")
    log_entries = read_log()
    
    if not log_entries:
        print("No log entries read.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Read {len(log_entries)} log entries.")
    
    # Example: Sort by timestamp (index 0)
    sorted_log = sort_log(log_entries, 0)
    print(f"First entry timestamp: {sorted_log[0][0]}")
    print(f"Last entry timestamp: {sorted_log[-1][0]}")
    
    # Example: Get entries by IP
    example_ip = "192.168.1.1"  # Replace with actual IP from your logs
    ip_entries = get_entries_by_addr(log_entries, example_ip)
    print(f"Found {len(ip_entries)} entries for IP {example_ip}")
    
    # Example: Get failed reads
    client_errors, server_errors = get_failed_reads(log_entries)
    print(f"Client errors (4xx): {len(client_errors)}")
    print(f"Server errors (5xx): {len(server_errors)}")
    
    # Example: Convert to dictionary format
    log_dict = log_to_dict(log_entries)
    print(f"Created dictionary with {len(log_dict)} sessions")
    
    # Print statistics for the first 5 sessions
    for i, (uid, entries) in enumerate(log_dict.items()):
        if i >= 5:
            break
        print(f"\nSession {i+1}: {uid}")
        print(f"  Number of requests: {len(entries)}")
        print(f"  First request timestamp: {entries[0]['timestamp']}")