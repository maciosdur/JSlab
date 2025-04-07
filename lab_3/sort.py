from typing import List, Tuple

def sort_log(log: List[Tuple], index: int) -> List[Tuple]:
    """
    Sortuje listę krotek (log) według elementu o podanym indeksie.
    
    Args:
        log: Lista krotek reprezentujących wpisy z logów
        index: Indeks elementu krotki, według którego należy sortować (0-based)
    
    Returns:
        List[Tuple]: Posortowana lista krotek
        
    Raises:
        IndexError: Gdy podany indeks jest poza zakresem krotek
        TypeError: Gdy nie można porównać elementów pod danym indeksem
    """
    if not log:
        return []
    
    try:
        # Sprawdzenie czy indeks jest prawidłowy
        if index < 0 or index >= len(log[0]):
            raise IndexError(f"Indeks {index} jest poza zakresem. Krotki mają {len(log[0])} elementów.")
        
        # Sortowanie z obsługą None
        def get_sort_key(x):
            val = x[index]
            # None traktujemy jako najmniejsze wartości
            return (val is None, val)
        
        return sorted(log, key=get_sort_key)
        
    except IndexError as e:
        print(f"Błąd: {str(e)}", file=sys.stderr)
        return log.copy()  # Zwróć kopię oryginalnej listy
    except TypeError as e:
        print(f"Błąd sortowania: {str(e)}", file=sys.stderr)
        print("Nie można porównać elementów pod podanym indeksem.", file=sys.stderr)
        return log.copy()
