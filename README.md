System Zgłaszania Awarii IT (HelpDesk IT)

Technologie
Framework Django 5
Baza danych SQLite3
Frontend Bootstrap 5 (CSS/JS via CDN)
Język Python 3

Funkcjonalności
Moduł Pracownika:
- Rejestracja nowego konta i logowanie
- Formularz zgłaszania awarii (Kategoria, Opis, Priorytet)
- Podgląd listy własnych zgłoszeń wraz z ich aktualnym statusem
- Możliwość usunięcia własnego zgłoszenia

Moduł Administratora:
- Dostęp do panelu zarządzania (panel-it) chroniony uprawnieniami `is_staff`
- Przeglądanie wszystkich zgłoszeń z całej firmy
- Filtrowanie po statusie oraz wyszukiwarka tekstowa (tytuł/opis)
- Szybka zmiana statusu (Nowe -> W trakcie -> Zamknięte) bez wychodzenia z panelu
- Możliwość usuwania dowolnych zgłoszeń

Instrukcja uruchomienia

Aplikacja nie wymaga środowiska Node.js ani dodatkowych systemów budowania frontendu. Wszystkie komponenty są zintegrowane wewnątrz frameworka Django.

1. Pobierz projekt i przejdź do folderu:
   bash
   cd system_awarii

   python -m venv venv
   # Windows:
   .\venv\Scripts\activate

   pip install -r requirements.txt

   python manage.py migrate
   
   python manage.py runserver

Aplikacja będzie dostępna pod adresem http://127.0.0.1:8000/

Konto testowe
admin
q1w2e3r4
