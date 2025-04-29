import csv
from datetime import datetime  # Usuń import date
import numpy as np
from abc import ABC, abstractmethod

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
def load_timeseries(filename, column_idx=2):  # Domyślnie kolumna 2 (indeks 1 w Pythonie)
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Wczytanie nagłówków
        headers = [next(reader) for _ in range(6)]
        
        # Pobranie metadanych dla wybranej kolumny
        station_code = headers[1][column_idx - 1]  # -1 bo indeksy w Pythonie zaczynają się od 0
        indicator = headers[2][column_idx - 1]
        averaging_time = headers[3][column_idx - 1]
        unit = headers[4][column_idx - 1]
        
        # Przygotowanie danych
        dates = []
        values = []
        
        for row in reader:
            date_str = row[0]
            value_str = row[column_idx - 1]  # Dane z wybranej kolumny
            
            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%y %H:%M")  # Zostaw datetime
            except ValueError:
                continue
            
            try:
                value = float(value_str) if value_str else np.nan
            except ValueError:
                value = np.nan
            
            dates.append(date_obj)
            values.append(value)
        
        return TimeSeries(
            indicator_name=indicator,
            station_code=station_code,
            averaging_time=averaging_time,
            dates=dates,
            values=values,
            unit=unit
        )

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
        messages = []
        if series.mean is None or series.stddev is None:
            return ["Brak danych do analizy odchyleń."]
        
        mean = series.mean
        stddev = series.stddev
        for i, value in enumerate(series.values):
            if not np.isnan(value) and (value < mean - self.k * stddev or value > mean + self.k * stddev):
                messages.append(f"Outlier detected at index {i}: {value}")
        return messages


class ZeroSpikeDetector(SeriesValidator):
    """Wykrywa co najmniej 3 zera lub braki danych z rzędu."""
    
    def analyze(self, series: TimeSeries) -> list[str]:
        messages = []
        consecutive_zeros = 0
        
        for i, value in enumerate(series.values):
            if np.isnan(value) or value == 0:
                consecutive_zeros += 1
                if consecutive_zeros >= 3:
                    messages.append(f"Zero spike detected ending at index {i}.")
            else:
                consecutive_zeros = 0
        
        return messages


class ThresholdDetector(SeriesValidator):
    """Wykrywa wartości przekraczające zadany próg."""
    
    def __init__(self, threshold: float):
        self.threshold = threshold
    
    def analyze(self, series: TimeSeries) -> list[str]:
        messages = []
        for i, value in enumerate(series.values):
            if not np.isnan(value) and value > self.threshold:
                messages.append(f"Threshold exceeded at index {i}: {value}")
        return messages
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


if __name__ == "__main__":
    # 1 
    print("1\n-------------------------------------------------------")
    stations = load_stations("stacje.csv")
    print(stations[0])  # Wykorzystuje __str__
    print(repr(stations[0]))  # Wykorzystuje __repr__
    
    # Test równości
    s1 = stations[0]
    s2 = stations[1]
    s3 = Station(kod_stacji=s1.kod_stacji, nr=999, kod_miedzynarodowy='', nazwa_stacji='Test', 
                 stary_kod='', data_uruchomienia='', data_zamkniecia='', typ_stacji='', 
                 typ_obszaru='', rodzaj_stacji='', wojewodztwo='', miejscowosc='', 
                 adres='', lat=0, lon=0)
    
    print(f"Czy s1 == s2? {s1 == s2}")  # False
    print(f"Czy s1 == s3? {s1 == s3}")  # True (bo ten sam kod stacji)
    
    
    
    # 2
    print("\n2\n-------------------------------------------------------")
    ts = load_timeseries("measurements/2023_C6H6_1g.csv", 17)  # Wczytanie danych z kolumny 3
    print(repr(ts))  # Test __repr__
    print(ts)        # Test __str__
    
    # Test __getitem__ z indeksem
    print("\nPierwsze 5 pomiarów:")
    for date, value in ts[:5]:
        print(f"{date}: {value if not np.isnan(value) else 'brak danych'} {ts.unit}")
    
    # # Test __getitem__ z datą
    # test_date = date(2023, 1, 1)  # Używamy date_type zamiast date
    # try:
    #     value = ts[test_date]
    #     print(f"\nWartość dla {test_date}: {value if not np.isnan(value) else 'brak danych'} {ts.unit}")
    # except KeyError as e:
    #     print(e)
    print(ts[0])        # zwróci (datetime(2023,1,1), 12.5)
    print("\n" + str(ts[1:5]))  
    print("\n")
    print(ts[datetime(2023, 1, 1, 12, 0)])  # Zwróci wartość dla daty i czasu 2023-01-01 12:00
    
    # 3
    print("\n3\n-------------------------------------------------------")
    # Przykład użycia
    print(f"Średnia wartości: {ts.mean}")  # Wyświetli średnią arytmetyczną
    print(f"Odchylenie standardowe: {ts.stddev}")  # Wyświetli odchylenie standardowe
    
    # 4
    print("\n4\n-------------------------------------------------------")
    # Załóżmy, że ts to obiekt TimeSeries
    ts = load_timeseries("measurements/2023_C6H6_1g.csv", 17)

    # OutlierDetector
    outlier_detector = OutlierDetector(k=20)
    outlier_messages = outlier_detector.analyze(ts)
    print("\nOutlier Detector:")
    for msg in outlier_messages:
        print(msg)

    # ZeroSpikeDetector
    zero_spike_detector = ZeroSpikeDetector()
    zero_spike_messages = zero_spike_detector.analyze(ts)
    print("\nZero Spike Detector:")
    for msg in zero_spike_messages:
        print(msg)

    # ThresholdDetector
    threshold_detector = ThresholdDetector(threshold=100)
    threshold_messages = threshold_detector.analyze(ts)
    print("\nThreshold Detector:")
    for msg in threshold_messages:
        print(msg)
        
    # # Kompozytowy walidator w trybie AND
    # composite_and = CompositeValidator(
    #     validators=[outlier_detector, threshold_detector],
    #     mode="AND"
    # )
    # and_messages = composite_and.analyze(ts)
    # print("\nComposite Validator (AND):")
    # for msg in and_messages:
    #     print(msg)