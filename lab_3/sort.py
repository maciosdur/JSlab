def sort_log(log: List[Tuple], index: int) -> List[Tuple]:
    """
    Sortuje listę krotek (log) według elementu o podanym indeksie.
    
    Args:
        log: Lista krotek reprezentujących wpisy z logów
        index: Indeks elementu krotki, według którego należy sortować
    
    Returns:
        List[Tuple]: Posortowana lista krotek
        
    Raises:
        IndexError: Gdy podany indeks jest poza zakresem krotek
        TypeError: Gdy nie można porównać elementów pod danym indeksem
    """
    try:
        # Sprawdź czy lista nie jest pusta
        if not log:
            return []
            
        # Sprawdź czy indeks nie wykracza poza rozmiar krotek
        if index >= len(log[0]) or index < 0:
            raise IndexError(f"Indeks {index} jest poza zakresem. Krotki mają {len(log[0])} elementów.")
        
        # Sortowanie z obsługą None (traktowane jako najmniejsze wartości)
        sorted_log = sorted(log, key=lambda x: (x[index] is not None, x[index]))
        
        return sorted_log
        
    except IndexError as e:
        print(f"Błąd indeksu: {str(e)}")
        return log  # Zwraca oryginalną listę w przypadku błędu
    except TypeError as e:
        print(f"Błąd typu podczas sortowania: {str(e)}")
        print("Nie można porównać elementów pod podanym indeksem.")
        return log  # Zwraca oryginalną listę w przypadku błędu