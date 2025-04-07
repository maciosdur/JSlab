import socket
from typing import List, Tuple

def get_entries_by_host(log: List[Tuple], host: str) -> List[Tuple]:
    """
    Filtruje wpisy logów według hosta (adres IP lub nazwa domenowa serwera)
    
    Args:
        log: Lista krotek z logami
        host: Adres IP lub nazwa domenowa serwera (pole host w logach)
    
    Returns:
        List[Tuple]: Lista wpisów pasujących do podanego hosta
    """
    def validate_address(addr: str) -> bool:
        """Sprawdza czy adres jest poprawnym IP lub hostname"""
        try:
            # Sprawdź czy to IP (IPv4 lub IPv6)
            socket.inet_pton(socket.AF_INET, addr)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, addr)
                return True
            except socket.error:
                try:
                    # Sprawdź czy to poprawna nazwa domenowa
                    socket.gethostbyname(addr)
                    return True
                except socket.error:
                    return False

    if not validate_address(host):
        raise ValueError(f"Nieprawidłowy adres hosta: {host}")

    HOST_INDEX = 8  # Indeks pola host w krotce
    return [entry for entry in log if entry[HOST_INDEX] and 
           (entry[HOST_INDEX] == host or 
            entry[HOST_INDEX].endswith(f".{host}"))]
    
    
def get_entries_by_code(log: List[Tuple], status_code: int) -> List[Tuple]:
    VALID_STATUS_CODES = {
        100, 101, 102, 103,
        200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
        300, 301, 302, 303, 304, 305, 306, 307, 308,
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
        410, 411, 412, 413, 414, 415, 416, 417, 418, 421,
        422, 423, 424, 425, 426, 428, 429, 431, 451,
        500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
    }

    if not isinstance(status_code, int) or status_code not in VALID_STATUS_CODES:
        raise ValueError(f"Invalid HTTP status code: {status_code}")

    STATUS_CODE_INDEX = 14  # Nowa pozycja status_code w pełnej krotce
    return [entry for entry in log if entry[STATUS_CODE_INDEX] == status_code]


from typing import List, Tuple, Union

def get_failed_reads(log: List[Tuple], concatenate: bool = True) -> Union[List[Tuple], Tuple[List[Tuple], List[Tuple]]]:
    """
    Zwraca nieudane żądania HTTP (4xx i 5xx) z logów
    
    Args:
        log: Lista krotek z logami
        concatenate: 
            True - zwraca pojedynczą listę 4xx+5xx
            False - zwraca krotkę (lista_4xx, lista_5xx)
    
    Returns:
        W zależności od parametru concatenate:
        - jedna lista z błędami 4xx i 5xx (domyślnie)
        - lub krotka z dwiema osobnymi listami
    """
    STATUS_CODE_INDEX = 14  # Indeks pola z kodem statusu
    
    errors_4xx = []
    errors_5xx = []
    
    for entry in log:
        status = entry[STATUS_CODE_INDEX]
        if status is None:
            continue
            
        if 400 <= status < 500:
            errors_4xx.append(entry)
        elif 500 <= status < 600:
            errors_5xx.append(entry)
    
    return errors_4xx + errors_5xx if concatenate else (errors_4xx, errors_5xx)

def get_entries_by_extension(log: List[Tuple], extension: str) -> List[Tuple]:
    """
    Filtruje wpisy logów według rozszerzenia pliku w URI
    
    Args:
        log: Lista krotek z logami
        extension: Rozszerzenie do wyszukania (np. "jpg", "pdf")
    
    Returns:
        List[Tuple]: Lista wpisów zawierających podane rozszerzenie w URI
    """
    URI_INDEX = 9  # Indeks pola URI w krotce
    
    # Usuń kropkę z rozszerzenia jeśli istnieje i zrób małe litery
    clean_extension = extension.lower().lstrip('.')
    
    results = []
    for entry in log:
        uri = entry[URI_INDEX]
        if not uri:
            continue
            
        # Podziel URI na części i sprawdź rozszerzenie ostatniej części
        parts = uri.rsplit('.', 1)
        if len(parts) > 1 and parts[1].lower() == clean_extension:
            results.append(entry)
    
    return results