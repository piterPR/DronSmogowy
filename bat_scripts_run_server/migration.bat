@ECHO OFF 
:: Migration latest data from GCP database
TITLE Migracja danych aplikacja Dron smogowy
ECHO Uruchamiam skrypt do migraji najnowszych danych z GCP 
:: Section 1: Windows 10 information
ECHO ==========================
ECHO migration.py
ECHO ============================
python migration.py
ECHO ==========================
ECHO Migration completed
ECHO ============================
PAUSE