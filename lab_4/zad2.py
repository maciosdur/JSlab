#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import stat
import platform

def is_executable(filepath):
    """Sprawdza, czy plik jest wykonywalny w zależności od systemu operacyjnego."""
    if platform.system() == 'Windows':
        return filepath.lower().endswith(('.exe', '.bat', '.cmd', '.ps1'))
    else:
         return False

def print_path_directories():
    """Wypisuje wszystkie katalogi ze zmiennej PATH, każdy w osobnej linii."""
    path_dirs = os.getenv('PATH', '').split(os.pathsep)
    for directory in path_dirs:
        if directory:  # Pomijanie pustych ścieżek
            print(directory)

def print_path_with_executables():
    """Wypisuje katalogi z PATH wraz z listą plików wykonywalnych."""
    path_dirs = os.getenv('PATH', '').split(os.pathsep)
    
    for directory in path_dirs:
        if not directory:  # Pomijanie pustych ścieżek
            continue
            
        print(f"\nKatalog: {directory}")
        
        try:
            files = os.listdir(directory)
            executables = []
            
            for file in files:
                full_path = os.path.join(directory, file)
                if os.path.isfile(full_path) and is_executable(full_path):
                    executables.append(file)
            
            if executables:
                print("Pliki wykonywalne:")
                for exe in sorted(executables):
                    print(f"  - {exe}")
            else:
                print("Brak plików wykonywalnych w tym katalogu.")
                
        except PermissionError:
            print("  Brak uprawnień do odczytu katalogu")
        except FileNotFoundError:
            print("  Katalog nie istnieje")
        except Exception as e:
            print(f"  Błąd podczas przetwarzania katalogu: {str(e)}")

def show_help():
    """Wyświetla pomoc dotyczącą użycia skryptu."""
    print("Użycie:")
    print("  python path_script.py [OPCJA]")
    print("\nOpcje:")
    print("  --list        Wyświetla katalogi z PATH (domyślne zachowanie)")
    print("  --executables Wyświetla katalogi z PATH wraz z plikami wykonywalnymi")
    print("  --help        Wyświetla tę pomoc")

if __name__ == "__main__":
    # Domyślna akcja
    action = print_path_directories
    
    # Sprawdzenie argumentów
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == '--executables' or arg == '-e':
            action = print_path_with_executables
        elif arg == '--help' or arg == '-h':
            show_help()
            sys.exit(0)
        elif arg == '--list' or arg == '-l':
            pass  # Domyślna akcja
        else:
            print(f"Nieznana opcja: {sys.argv[1]}")
            show_help()
            sys.exit(1)
    
    # Wykonanie wybranej akcji
    action()