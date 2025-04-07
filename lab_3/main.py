from read import read_log
from sort import sort_log
from filters import get_entries_by_host, get_entries_by_code
from filters import get_failed_reads
from filters import get_entries_by_extension
from dicts import entry_to_dict, log_to_dict
from dicts import print_dict_entry_dates, find_multi_request_sessions



def display_entry(entry, index=None):
    """Pomocnicza funkcja do wyświetlania pojedynczego wpisu"""
    if index:
        print(f"{index}. ", end="")
    print(f"Timestamp: {entry[0]}")
    print(f"UID: {entry[1]}")
    print(f"Connection: {entry[2]}:{entry[3]} → {entry[4]}:{entry[5]}")
    print(f"Transaction: {entry[6]}")
    print(f"Method: {entry[7]}")
    print(f"Host: {entry[8]}")
    print(f"URI: {entry[9]}")
    if entry[14]:  # Jeśli istnieje kod statusu
        print(f"Status: {entry[14]} {entry[15]}")
    print()

def main():
    # Wczytaj logi
    print("Wczytywanie logów...")
    logs = read_log()
    print(f"Wczytano {len(logs)} wpisów\n")

    # a. Przykładowe wyświetlenie pierwszych 3 niesortowanych wpisów
    print("=== Przykładowe wpisy (niesortowane) ===")
    for i, entry in enumerate(logs[:3], 1):
        display_entry(entry, i)
    print("\n" + "="*80 + "\n")

    # b. sort_log - sortowanie po porcie docelowym (indeks 5)
    print("=== Sortowanie po porcie docelowym (id.resp_p) ===")
    sorted_by_port = sort_log(logs, 5)
    for i, entry in enumerate(sorted_by_port[:5], 1):
        display_entry(entry, i)
    print("\n" + "="*80 + "\n")

    # c. get_entries_by_host
    test_hosts = [
        "www.google.com",
        "192.168.201.2",
        "ww.exassmple.org"
    ]
    
    print("=== Filtrowanie po hoście ===")
    for host in test_hosts:
        try:
            entries = get_entries_by_host(logs, host)
            print(f"\nHost: {host} | Znaleziono wpisów: {len(entries)}")
            
            if entries:
                print("Przykładowe wpisy:")
                for i, entry in enumerate(entries[:3], 1):
                    display_entry(entry, i)
            print("-" * 60)
            
        except ValueError as e:
            print(f"Błąd dla hosta {host}: {str(e)}")
    print("\n" + "="*80 + "\n")

    # d. get_entries_by_code
    test_codes = [200, 404, 500, 302]
    
    print("=== Filtrowanie po kodzie statusu ===")
    for code in test_codes:
        try:
            entries = get_entries_by_code(logs, code)
            print(f"\nStatus: {code} | Znaleziono wpisów: {len(entries)}")
            
            if entries:
                print("Przykładowe wpisy:")
                for i, entry in enumerate(entries[:3], 1):
                    display_entry(entry, i)
            print("-" * 60)
            
        except ValueError as e:
            print(f"Błąd dla kodu {code}: {str(e)}")
    print("\n" + "="*80 + "\n")       

    # e. get_failed_reads - pokaż tylko 3 pierwsze wyniki
    print("\n=== Nieudane żądania (4xx i 5xx) ===")
    
    # Wersja z połączonymi listami
    all_failed = get_failed_reads(logs)
    print(f"\nWszystkie błędy (4xx+5xx) - pierwsze 3 z {len(all_failed)}:")
    for i, entry in enumerate(all_failed[:3], 1):
        display_entry(entry, i)
    
    # Wersja z rozdzielonymi listami
    client_errors, server_errors = get_failed_reads(logs, concatenate=False)
    print(f"\nBłędy klienta (4xx) - pierwsze 3 z {len(client_errors)}:")
    for i, entry in enumerate(client_errors[:3], 1):
        display_entry(entry, i)
    
    print(f"\nBłędy serwera (5xx) - pierwsze 3 z {len(server_errors)}:")
    for i, entry in enumerate(server_errors[:3], 1):
        display_entry(entry, i)
    
    print("\n" + "="*80 + "\n")       
            
            
    # f. get_entries_by_extension
    test_extensions = ["jpg", "pasdf", "js", "html"]
    
    print("\n=== Filtrowanie po rozszerzeniu pliku ===")
    for ext in test_extensions:
        entries = get_entries_by_extension(logs, ext)
        print(f"\nRozszerzenie: .{ext} | Znaleziono wpisów: {len(entries)}")
        
        if entries:
            print("Przykładowe wpisy:")
            for i, entry in enumerate(entries[:3], 1):
                display_entry(entry, i)
    print("\n" + "="*80 + "\n")      
    print("\n" + "="*80 + "\n")     
    print("\n" + "="*80 + "\n")        
    print("\n" + "="*80 + "\n")
    print("\n" + "SLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKISLOWNIKI" + "\n")  
    print("\n" + "S L O W N I K I" + "\n")
    
    #a. entry_to_dict - konwersja pierwszego wpisu do słownika  
    # Przykład użycia dla pierwszego wpisu
    if logs:
        first_entry = logs[0]
        entry_dict = entry_to_dict(first_entry)
        print("Słownikowa reprezentacja pierwszego wpisu:")
        for key, value in entry_dict.items():
            print(f"{key:20}: {value}")
        print("\n" + "="*80 + "\n")
    
    #b. log_to_dict - konwersja całego logu do słownika
    # Konwersja całego logu
    session_dict = log_to_dict(logs)
    
    # Przykładowe użycie - wyświetlenie statystyk
    print(f"Liczba unikalnych sesji: {len(session_dict)}")
    
    # Wyświetlenie informacji o przykładowej sesji
    sample_uid = next(iter(session_dict))  # Pierwszy klucz słownika
    print(f"\nPrzykładowa sesja (UID: {sample_uid}):")
    print(f"Liczba wpisów w sesji: {len(session_dict[sample_uid])}")
    
    # Wyświetlenie pierwszego wpisu z sesji
    print("\nPierwszy wpis:")
    for key, value in session_dict[sample_uid][0].items():
        print(f"{key:20}: {value}")
    
    print("\n" + "="*80 + "\n")
    
    
    #c. print_dict_entry_dates - wyświetlenie statystyk dla każdej sesji
    print("=== Statystyki dla każdej sesji ===")   
    
    # Konwersja do słownika
    session_dict = log_to_dict(logs)
    request_counts = [len(entries) for entries in session_dict.values()]
    
    print("\n=== Statystyki sesji ===")
    print(f"Łączna liczba sesji: {len(session_dict)}")
    print(f"Żądań na sesję: min={min(request_counts)}, avg={sum(request_counts)/len(request_counts):.1f}, max={max(request_counts)}")
    print(f"Sesje z 1 żądaniem: {request_counts.count(1)} ({request_counts.count(1)/len(request_counts):.1%})")
    
    
    # Wyświetlenie statystyk dla pierwszych 5 sesji
    sample_sessions = dict(list(session_dict.items())[:5])
    print_dict_entry_dates(sample_sessions)   
    
    interesting_sessions = find_multi_request_sessions(session_dict)
    sample_sessions2 = dict(list(interesting_sessions.items())[:5])
    print_dict_entry_dates(sample_sessions2)
        
if __name__ == "__main__":
    main()