#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def display_environment_variables(filters=None):
    """
    Wyświetla zmienne środowiskowe, opcjonalnie filtrując je.
    
    Args:
        filters (list): Lista stringów do filtrowania zmiennych
    """
    env_vars = os.environ
    
    # Jeśli podano filtry, zastosuj je
    if filters:
        filtered_vars = {}
        for name, value in env_vars.items():
            for filter_str in filters:
                if filter_str.lower() in name.lower():
                    filtered_vars[name] = value
                    break
        env_vars = filtered_vars
    
    # Posortuj zmienne alfabetycznie
    sorted_vars = sorted(env_vars.items(), key=lambda x: x[0])
    
    # Wyświetl wyniki
    for name, value in sorted_vars:
        print(f"{name}={value}")

if __name__ == "__main__":
    # Pobierz argumenty z linii komend (pomijając nazwę skryptu)
    filters = sys.argv[1:] if len(sys.argv) > 1 else None
    
    display_environment_variables(filters)