import datetime
from typing import List, Tuple, Optional
import sys

def read_log(file_path: Optional[str] = None) -> List[Tuple]:
    """Reads HTTP logs from file or stdin"""
    log_entries = []
    source = open(file_path, 'r', encoding='utf-8') if file_path else sys.stdin
    
    for line in source:
        if not line.strip():
            continue
            
        fields = line.strip().split('\t')
        
        try:
            # Convert and validate required fields
            ts = datetime.datetime.fromtimestamp(float(fields[0]))
            uid = fields[1]
            id_orig_h = fields[2]
            id_orig_p = int(fields[3])
            id_resp_h = fields[4]
            id_resp_p = int(fields[5])
            trans_depth = int(fields[6])
            
            # Handle optional/missing fields
            method = fields[7] if len(fields) > 7 and fields[7] != '-' else None
            host = fields[8] if len(fields) > 8 and fields[8] != '-' else None
            uri = fields[9] if len(fields) > 9 and fields[9] != '-' else None
            referrer = fields[10] if len(fields) > 10 and fields[10] != '-' else None
            user_agent = fields[11] if len(fields) > 11 and fields[11] != '-' else None
            
            # Numeric fields
            request_body_len = int(fields[12]) if len(fields) > 12 else 0
            response_body_len = int(fields[13]) if len(fields) > 13 else 0
            
            # Status fields
            status_code = int(float(fields[14])) if len(fields) > 14 and fields[14] != '-' else None
            status_msg = fields[15] if len(fields) > 15 and fields[15] != '-' else None
            
            # Info fields
            info_code = int(float(fields[16])) if len(fields) > 16 and fields[16] != '-' else None
            info_msg = fields[17] if len(fields) > 17 and fields[17] != '-' else None
            
            # Tags and auth
            tags = fields[19] if len(fields) > 19 and fields[19] != '-' else None
            username = fields[20] if len(fields) > 20 and fields[20] != '-' else None
            
            # File and MIME types
            orig_fuids = fields[23] if len(fields) > 23 and fields[23] not in ['-', '(empty)'] else None
            orig_mime_types = fields[24] if len(fields) > 24 and fields[24] not in ['-', '(empty)'] else None
            resp_fuids = fields[25] if len(fields) > 25 and fields[25] not in ['-', '(empty)'] else None
            resp_mime_types = fields[26] if len(fields) > 26 and fields[26] not in ['-', '(empty)'] else None
            
            entry = (
                ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, trans_depth,
                method, host, uri, referrer, user_agent, request_body_len,
                response_body_len, status_code, status_msg, info_code, info_msg,
                tags, username, orig_fuids, orig_mime_types, resp_fuids, resp_mime_types
            )
            log_entries.append(entry)
            
        except (IndexError, ValueError) as e:
            print(f"Skipping malformed line: {line.strip()} (Error: {str(e)})", file=sys.stderr)
            continue
    
    if file_path:
        source.close()
    return log_entries