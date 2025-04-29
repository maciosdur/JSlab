import csv
from datetime import datetime  # Usuń import date
import numpy as np
from abc import ABC, abstractmethod
import os
from typing import List

class Station:
    def __init__(self, nr, kod_stacji, kod_miedzynarodowy, nazwa_stacji, stary_kod, data_uruchomienia, data_zamkniecia, typ_stacji, typ_obszaru, rodzaj_stacji, wojewodztwo, miejscowosc, adres, lat, lon):
        self.nr = nr
        self.kod_stacji = kod_stacji
        self.kod_miedzynarodowy = kod_miedzynarodowy
        self.nazwa_stacji = nazwa_stacji
        self.stary_kod = stary_kod
        self.data_uruchomienia = data_uruchomienia
        self.data_zamkniecia = data_zamkniecia
        self.typ_stacji = typ_stacji
        self.typ_obszaru = typ_obszaru
        self.rodzaj_stacji = rodzaj_stacji
        self.wojewodztwo = wojewodztwo
        self.miejscowosc = miejscowosc
        self.adres = adres
        self.lat = lat
        self.lon = lon
    
    def __str__(self):
        return f"Station({self.nazwa_stacji}, kod: {self.kod_stacji}, {self.miejscowosc})"
    
    def __repr__(self):
        return f"Station(nr={self.nr}, kod_stacji='{self.kod_stacji}', nazwa='{self.nazwa_stacji}')"
    
    def __eq__(self, other):
        if not isinstance(other, Station):
            return False
        return self.kod_stacji == other.kod_stacji

# Przykład użycia:
def load_stations(filename):
    stations = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pomijamy nagłówek
        for row in reader:
            station = Station(
                nr=int(row[0]),
                kod_stacji=row[1],
                kod_miedzynarodowy=row[2],
                nazwa_stacji=row[3],
                stary_kod=row[4],
                data_uruchomienia=row[5],
                data_zamkniecia=row[6],
                typ_stacji=row[7],
                typ_obszaru=row[8],
                rodzaj_stacji=row[9],
                wojewodztwo=row[10],
                miejscowosc=row[11],
                adres=row[12],
                lat=float(row[13]) if row[13] else None,
                lon=float(row[14]) if row[14] else None
            )
            stations.append(station)
    return stations

class TimeSeries:
    def __init__(self, indicator_name, station_code, averaging_time, dates, values, unit):
        self.indicator_name = indicator_name
        self.station_code = station_code
        self.averaging_time = averaging_time
        self.dates = dates
        self.values = np.array(values, dtype=float)  # Konwersja na numpy array
        self.unit = unit
    
    def __getitem__(self, key):
        # Część i: obsługa indeksu lub slice'a
        if isinstance(key, int):
            return (self.dates[key], self.values[key])
        elif isinstance(key, slice):
            selected_dates = self.dates[key]
            selected_values = self.values[key]
            return list(zip(selected_dates, selected_values))
        
        # Część ii: obsługa daty
        elif isinstance(key, datetime):  # Użyj tylko datetime
            try:
                idx = self.dates.index(key)
                return self.values[idx]
            except ValueError:
                raise KeyError(f"No data for date {key}")
        else:
            raise TypeError("Invalid key type. Use int, slice, or datetime")
    
    def __str__(self):
        return (f"TimeSeries({self.indicator_name}, station: {self.station_code}, "
                f"from {self.dates[0]} to {self.dates[-1]}, {len(self.dates)} measurements)")
    
    def __repr__(self):
        return (f"TimeSeries(indicator='{self.indicator_name}', station='{self.station_code}', "
                f"averaging='{self.averaging_time}', unit='{self.unit}')")
    
    @property
    def mean(self):
        """Zwraca średnią arytmetyczną wartości (ignorując brakujące dane)."""
        if np.isnan(self.values).all():  # Jeśli wszystkie wartości to NaN
            return None
        return np.nanmean(self.values)  # Oblicza średnią ignorując NaN

    @property
    def stddev(self):
        """Zwraca odchylenie standardowe wartości (ignorując brakujące dane)."""
        if np.isnan(self.values).all():  # Jeśli wszystkie wartości to NaN
            return None
        return np.nanstd(self.values)  # Oblicza odchylenie standardowe ignorując NaN

# Funkcja pomocnicza do wczytywania danych z pliku
def load_timeseries(filename) -> list[TimeSeries]:
    """
    Wczytuje dane z pliku CSV i zwraca listę obiektów TimeSeries dla każdej stacji.
    """
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Wczytanie nagłówków
        headers = [next(reader) for _ in range(6)]
        
        # Pobranie metadanych
        station_codes = headers[1][1:]  # Pomijamy pierwszą kolumnę (Nr)
        indicators = headers[2][1:]
        averaging_times = headers[3][1:]
        units = headers[4][1:]
        
        # Przygotowanie danych dla każdej stacji
        time_series_list = []
        dates = []
        values_by_station = {code: [] for code in station_codes}
        
        for row in reader:
            date_str = row[0]
            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%y %H:%M")
            except ValueError:
                continue
            
            dates.append(date_obj)
            for i, station_code in enumerate(station_codes):
                value_str = row[i + 1]  # Dane dla stacji zaczynają się od drugiej kolumny
                try:
                    value = float(value_str) if value_str else np.nan
                except ValueError:
                    value = np.nan
                values_by_station[station_code].append(value)
        
        # Tworzenie obiektów TimeSeries dla każdej stacji
        for i, station_code in enumerate(station_codes):
            time_series = TimeSeries(
                indicator_name=indicators[i],
                station_code=station_code,
                averaging_time=averaging_times[i],
                dates=dates,
                values=values_by_station[station_code],
                unit=units[i]
            )
            time_series_list.append(time_series)
        
        return time_series_list

class SeriesValidator(ABC):
    """Klasa abstrakcyjna definiująca metodę analyze."""
    
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        """Analizuje dane w obiekcie TimeSeries i zwraca listę komunikatów o anomaliach."""
        pass


class OutlierDetector(SeriesValidator):
    """Wykrywa wartości oddalone o więcej niż k odchyleń standardowych od średniej."""
    
    def __init__(self, k: float):
        self.k = k
    
    def analyze(self, series: TimeSeries) -> list[str]:
        if series.mean is None or series.stddev is None:
            return ["Brak danych do analizy odchyleń."]
        
        mean = series.mean
        stddev = series.stddev
        for value in series.values:
            if not np.isnan(value) and (value < mean - self.k * stddev or value > mean + self.k * stddev):
                return [f"Outliers detected in TimeSeries: {series.indicator_name} (station: {series.station_code})."]
        return []


class ZeroSpikeDetector(SeriesValidator):
    """Wykrywa co najmniej 3 zera lub braki danych z rzędu."""
    
    def analyze(self, series: TimeSeries) -> list[str]:
        consecutive_zeros = 0
        
        for value in series.values:
            if np.isnan(value) or value == 0:
                consecutive_zeros += 1
                if consecutive_zeros >= 3:
                    return [f"Zero spike detected in TimeSeries: {series.indicator_name} (station: {series.station_code})."]
            else:
                consecutive_zeros = 0
        
        return []


class ThresholdDetector(SeriesValidator):
    """Wykrywa wartości przekraczające zadany próg."""
    
    def __init__(self, threshold: float):
        self.threshold = threshold
    
    def analyze(self, series: TimeSeries) -> list[str]:
        for value in series.values:
            if not np.isnan(value) and value > self.threshold:
                return [f"Threshold exceeded in TimeSeries: {series.indicator_name} (station: {series.station_code})."]
        return []

class CompositeValidator(SeriesValidator):
    """Kompozytowy walidator, który łączy wiele walidatorów w trybie OR lub AND."""
    
    def __init__(self, validators: list[SeriesValidator], mode: str = "OR"):
        """
        Inicjalizuje CompositeValidator.
        
        :param validators: Lista walidatorów (obiektów dziedziczących z SeriesValidator).
        :param mode: Tryb działania ("OR" lub "AND").
        """
        if mode not in {"OR", "AND"}:
            raise ValueError("Mode must be 'OR' or 'AND'.")
        self.validators = validators
        self.mode = mode
    
    def analyze(self, series: TimeSeries) -> list[str]:
        """
        Analizuje dane w obiekcie TimeSeries za pomocą wszystkich walidatorów.
        
        :param series: Obiekt TimeSeries do analizy.
        :return: Lista komunikatów o wykrytych anomaliach.
        """
        all_messages = []
        
        if self.mode == "OR":
            # Tryb OR: Zwraca komunikaty z dowolnego walidatora
            for validator in self.validators:
                messages = validator.analyze(series)
                all_messages.extend(messages)
        
        elif self.mode == "AND":
            for i, value in enumerate(series.values):
                if not np.isnan(value):  # Ignoruj brakujące dane
                    print(f"Sprawdzanie wartości na indeksie {i}: {value}")  # Debug
                    valid = True
                    messages = []
                    for validator in self.validators:
                        validator_messages = validator.analyze(series)
                        if not any(f"{value}" in msg for msg in validator_messages):
                            valid = False
                            break
                        messages.extend(validator_messages)
                    if valid:
                        all_messages.extend(messages)
        
        return all_messages  

class Measurements:
    """
    Klasa agregująca dane z wielu plików CSV zawierających pomiary różnych wskaźników.
    """
    def __init__(self, directory: str):
        """
        Inicjalizuje Measurements, identyfikując pliki w katalogu, ale nie wczytując danych od razu.
        """
        self.directory = directory
        self.metadata = []  # Przechowuje metadane o plikach (leniwe ładowanie)
        self._load_metadata()

    def _load_metadata(self):
        """
        Wczytuje metadane z nazw plików w katalogu i zapisuje je w `metadata`.
        """
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".csv"):
                    # Rozbij nazwę pliku na części: <rok>_<mierzona wielkość>_<częstotliwość>.csv
                    parts = file[:-4].split("_")
                    if len(parts) == 3:
                        year, parameter_name, frequency = parts
                        file_path = os.path.join(root, file)
                        self.metadata.append({
                            "file_path": file_path,
                            "parameter_name": parameter_name,
                            "frequency": frequency,
                            "year": int(year)
                        })

    def __len__(self):
        """
        Zwraca liczbę obiektów TimeSeries możliwych do załadowania.
        """
        return len(self.metadata)

    def __contains__(self, parameter_name: str):
        """
        Sprawdza, czy co najmniej jeden TimeSeries zawiera podany wskaźnik.
        """
        return any(meta["parameter_name"] == parameter_name for meta in self.metadata)

    def get_by_parameter(self, param_name: str) -> list[TimeSeries]:
        """
        Zwraca wszystkie obiekty TimeSeries, których parameter_name == param_name.
        """
        result = []
        for meta in self.metadata:
            if meta["parameter_name"] == param_name:
                result.extend(load_timeseries(meta["file_path"]))
        return result

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        """
        Zwraca wszystkie serie danych dla danej stacji (różne wskaźniki, lata i częstotliwości).
        """
        result = []
        for meta in self.metadata:
            time_series_list = load_timeseries(meta["file_path"])
            for ts in time_series_list:
                if ts.station_code == station_code:
                    result.append(ts)
        return result
    
    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict:
        """
        Wykrywa anomalie we wszystkich seriach danych za pomocą podanych walidatorów.

        :param validators: Lista walidatorów (obiektów dziedziczących z SeriesValidator).
        :param preload: Jeśli True, wymusza pełne załadowanie danych. Jeśli False, waliduje tylko wcześniej załadowane serie.
        :return: Słownik, gdzie kluczem jest obiekt TimeSeries, a wartością lista komunikatów o anomaliach.
        """
        anomalies = {}

        if preload:
            # Wymuszenie pełnego załadowania danych
            for meta in self.metadata:
                time_series_list = load_timeseries(meta["file_path"])
                for ts in time_series_list:
                    messages = []
                    for validator in validators:
                        messages.extend(validator.analyze(ts))
                    if messages:
                        anomalies[ts] = messages
        else:
            # Walidacja tylko wcześniej załadowanych serii
            for meta in self.metadata:
                time_series_list = load_timeseries(meta["file_path"])
                for ts in time_series_list:
                    if ts in anomalies:  # Sprawdź, czy seria była już załadowana
                        messages = []
                        for validator in validators:
                            messages.extend(validator.analyze(ts))
                        if messages:
                            anomalies[ts] = messages

        return anomalies
    
if __name__ == "__main__":
    
    # 5
    print("\n5\n-------------------------------------------------------")
    
    # Ścieżka do katalogu z plikami CSV
    directory = "C:\\Users\\Maciek\\OneDrive\\Dokumenty\\JSlab\\lab_6\\measurements"

    # Tworzenie obiektu Measurements
    measurements = Measurements(directory)

    # Liczba dostępnych TimeSeries
    print(f"Liczba Plików csv: {len(measurements)}")

    # Sprawdzenie, czy istnieje wskaźnik "SO2"
    print(f"Czy istnieje wskaźnik 'C6H6': {'C6H6' in measurements}")

    # Pobranie wszystkich TimeSeries dla wskaźnika "SO2"
    so2_series = measurements.get_by_parameter("C6H6")
    print(f"Liczba TimeSeries dla 'C6H6': {len(so2_series)}")

    # Pobranie wszystkich TimeSeries dla stacji "DsSniezkaObs"
    station_series = measurements.get_by_station("DsSniezkaObs")
    print(f"Liczba TimeSeries dla stacji 'DsSniezkaObs': {len(station_series)}")
    
    # 6
    print("\n6\n-------------------------------------------------------")
    # Tworzenie walidatorów
    outlier_detector = OutlierDetector(k=20.0)
    zero_spike_detector = ZeroSpikeDetector()
    threshold_detector = ThresholdDetector(threshold=100.0)

    # Lista walidatorów
    validators = [outlier_detector, zero_spike_detector, threshold_detector]

    # Wykrywanie anomalii
    so2_series = measurements.get_by_parameter("C6H6")
    anomalies = measurements.detect_all_anomalies(validators, preload=True)

    # Wyświetlenie wyników
    for ts, messages in anomalies.items():
        print(f"Anomalies in {ts}:")
        for message in messages:
            print(f"  - {message}")