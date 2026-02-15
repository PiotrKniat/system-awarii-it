System Zgłaszania Awarii IT (HelpDesk IT)

Technologie
- Django 5
- SQLite3
- Bootstrap 5 (CSS/JS via CDN)
- Python 3

Funkcjonalności

Moduł Pracownika:
- Rejestracja nowego konta i logowanie
- Formularz zgłaszania awarii (kategoria, opis, priorytet)
- Podgląd listy własnych zgłoszeń wraz z ich aktualnym statusem
- Możliwość usunięcia własnego zgłoszenia

Moduł Administratora:
- Panel zarządzania
- Przeglądanie wszystkich zgłoszeń w firmie
- Filtrowanie po statusie i wyszukiwarka tekstowa (tytuł/opis)
- Szybka zmiana statusu (Nowe → W trakcie → Zamknięte) bez przeładowania strony
- Możliwość usuwania dowolnych zgłoszeń

Instrukcja uruchomienia

Aplikacja nie wymaga Node.js ani narzędzi do budowania frontendu. Wszystko jest zintegrowane w Django.

1. Pobierz projekt i przejdź do katalogu projektu:

cd system_awarii

2. Utwórz i aktywuj wirtualne środowisko:

python -m venv venv
na Windows (PowerShell):
.\venv\Scripts\Activate.ps1
na Windows (cmd):
.\venv\Scripts\activate
na macOS / Linux:
source venv/bin/activate

3. Zainstaluj zależności:

pip install -r requirements.txt

4. Wykonaj migracje i uruchom serwer deweloperski:

python manage.py migrate
python manage.py runserver

Serwis będzie dostępny pod adresem: http://127.0.0.1:8000/

Konto testowe
- Login: `admin`
- Hasło: `q1w2e3r4`

