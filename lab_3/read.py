import sys
import datetime
from typing import List, Tuple

def read_log() -> List[Tuple]:
    """
    Reads HTTP logs from stdin and returns a list of tuples containing only the specified fields.
    
    Returns:
        List[Tuple]: A list of tuples, each containing:
            - ts (datetime): Timestamp of the request
            - uid (str): Unique session identifier
            - id_orig_h (str): Client IP address
            - id_orig_p (int): Client port
            - id_resp_h (str): Server IP address
            - id_resp_p (int): Server port
            - method (str): HTTP method
            - host (str): Server hostname
            - uri (str): Requested URI
    """
    log_entries = []
    
    for line in sys.stdin:
        # Skip empty lines
        if not line.strip():
            continue
            
        # Split the line into fields (tab-separated)
        fields = line.strip().split('\t')
        
        try:
            # Convert timestamp from UNIX float to datetime
            ts = datetime.datetime.fromtimestamp(float(fields[0]))
            
            # Extract only the specified fields
            uid = fields[1]
            id_orig_h = fields[2]
            id_orig_p = int(fields[3])
            id_resp_h = fields[4]
            id_resp_p = int(fields[5])
            
            # Handle potentially missing fields (method, host, uri)
            method = fields[7] if len(fields) > 7 and fields[7] != '-' else None
            host = fields[8] if len(fields) > 8 and fields[8] != '-' else None
            uri = fields[9] if len(fields) > 9 and fields[9] != '-' else None
            
            # Create a tuple with only the specified fields
            entry = (ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri)
            log_entries.append(entry)
            
        except (IndexError, ValueError) as e:
            # Skip lines that don't match the expected format
            print(f"Skipping malformed line: {line.strip()} (Error: {str(e)})", file=sys.stderr)
            continue
    
    return log_entries

if __name__ == "__main__":
    # Example usage
    logs = read_log()
    print(f"Read {len(logs)} log entries")
    if logs:
        print("\nFirst entry:")
        print(f"Timestamp: {logs[0][0]}")
        print(f"UID: {logs[0][1]}")
        print(f"Client IP: {logs[0][2]}")
        print(f"Client Port: {logs[0][3]}")
        print(f"Server IP: {logs[0][4]}")
        print(f"Server Port: {logs[0][5]}")
        print(f"Method: {logs[0][6]}")
        print(f"Host: {logs[0][7]}")
        print(f"URI: {logs[0][8]}")