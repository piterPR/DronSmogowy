@ECHO OFF 
:: This batch file details Windows 10, hardware, and networking configuration.
TITLE Aplikacja Dron smogowy
ECHO Uruchamiam serwer xampp oraz aplikacje dron smogowy 
:: Section 1: Windows 10 information
ECHO ============================
ECHO Aplikacja Angular
ECHO ============================
start cmd /c "C:\Users\Admin\PycharmProjects\DronSmogowy\bat_scripts\start_angular.bat"
start cmd /c "C:\Users\Admin\PycharmProjects\DronSmogowy\bat_scripts\start_apache.bat"


