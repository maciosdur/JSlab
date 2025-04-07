from typing import Dict, Any, List, Tuple
from collections import defaultdict
def entry_to_dict(entry: tuple) -> Dict[str, Any]:
    """
    Konwertuje krotkę wpisu logu na słownik z opisowymi kluczami
    
    Args:
        entry: Krotka reprezentująca pojedynczy wpis z logu
        
    Returns:
        Słownik z mapowaniem nazw pól na wartości
    """
    return {
        'timestamp': entry[0],
        'uid': entry[1],
        'source_ip': entry[2],
        'source_port': entry[3],
        'dest_ip': entry[4],
        'dest_port': entry[5],
        'transaction_depth': entry[6],
        'http_method': entry[7],
        'host': entry[8],
        'uri': entry[9],
        'referer': entry[10],
        'user_agent': entry[11],
        'request_body_len': entry[12],
        'response_body_len': entry[13],
        'status_code': entry[14],
        'status_message': entry[15],
        'info_code': entry[16],
        'info_message': entry[17],
        'tags': entry[18],
        'username': entry[19],
        'orig_fuids': entry[20],
        'orig_mime_types': entry[21],
        'resp_fuids': entry[22],
        'resp_mime_types': entry[23]
    }
    
def log_to_dict(log_entries: List[tuple]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Konwertuje listę wpisów logu na słownik zorganizowany według UID sesji
    
    Args:
        log_entries: Lista krotek reprezentujących wpisy z logu
        
    Returns:
        Słownik gdzie:
        - klucz: uid sesji (str)
        - wartość: lista słowników reprezentujących wpisy danej sesji
    """
    log_dict = {}
    
    for entry in log_entries:
        uid = entry[1]  # UID jest na pozycji 1 w krotce
        entry_dict = entry_to_dict(entry)
        
        if uid not in log_dict:
            log_dict[uid] = []
        log_dict[uid].append(entry_dict)
    
    return log_dict   

def print_dict_entry_dates(log_dict: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Analizuje i wyświetla statystyki dla każdej sesji w słowniku logów
    
    Args:
        log_dict: Słownikowa reprezentacja logu (wynik log_to_dict)
    """
    for uid, entries in log_dict.items():
        if not entries:
            continue
            
        # 1. Adresy IP/nazwy domenowe
        source_ip = entries[0]['source_ip']
        dest_ips = {e['dest_ip'] for e in entries}
        
        # 2. Liczba żądań
        request_count = len(entries)
        
        # 3. Daty pierwszego i ostatniego żądania
        timestamps = [e['timestamp'] for e in entries]
        first_request = min(timestamps)
        last_request = max(timestamps)
        
        # 4. Procentowy udział metod HTTP
        method_counts = defaultdict(int)
        for e in entries:
            method = e['http_method'] or 'UNKNOWN'
            method_counts[method] += 1
        
        method_percentages = {
            method: (count / request_count) * 100
            for method, count in method_counts.items()
        }
        
        # 5. Stosunek żądań 2xx do wszystkich
        success_count = sum(
            1 for e in entries 
            if e['status_code'] and 200 <= e['status_code'] < 300
        )
        success_ratio = (success_count / request_count) * 100 if request_count > 0 else 0
        
        # Formatowanie wyjścia
        print(f"\n=== Analiza sesji UID: {uid} ===")
        print(f"Host źródłowy: {source_ip}")
        print(f"Hosty docelowe: {', '.join(dest_ips)}")
        print(f"Liczba żądań: {request_count}")
        print(f"Zakres czasowy: {first_request} - {last_request}")
        
        print("\nRozkład metod HTTP:")
        for method, percent in method_percentages.items():
            print(f"  • {method}: {percent:.1f}%")
        
        print(f"\nUdział żądań z kodem 2xx: {success_ratio:.1f}%")
        print("=" * 60)
        
def find_multi_request_sessions(log_dict: Dict[str, List[Dict[str, Any]]], min_requests: int = 2) -> Dict[str, List[Dict[str, Any]]]:
    """
    Filtruje słownik logów, zwracając tylko sesje z określoną minimalną liczbą żądań
    """
    return {uid: entries for uid, entries in log_dict.items() if len(entries) >= min_requests}