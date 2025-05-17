# SnackAutomat OS

## Was ist das?
**SnackAutomat OS** ist ein modular aufgebautes System zur Steuerung eines selbstgebauten Süßigkeitenautomaten auf Basis des Raspberry Pi Pico. Ziel ist es, ein vollständig konfigurierbares System für Eingabe, Steuerung und Ausgabe zu entwickeln – optimiert für schulische und private Projekte.

## Features

- Vollständig konfigurierbarer Automat (Konfigurationsdateien)
- Codeeingabe über 9-stelliges Tastenfeld
- Servogesteuerte Ausgabe der Süßigkeiten
- Optionale Statusanzeige mit LEDs oder Display

## Hardware

| Komponente             | Funktion                                    |
|------------------------|---------------------------------------------|
| Raspberry Pi Pico      | Steuerung und Programmausführung            |
| 9-stelliges Keypad     | Benutzereingabe (Produkt-IDs oder PINs)     |
| Servomotor             | Mechanismus zur Produktausgabe              |
| Stromversorgung        | USB oder extern, je nach Aufbau             |
| LEDs / Display (optional) | Anzeige von Statusinformationen oder Fehlern |

## Software

- **Sprache:** MicroPython  
- **Entwicklungsumgebung:** Thonny  
- **Bibliotheken:**
  - `machine`, `time`
  - Eigene Module für Motorsteuerung, Tasteneingabe, LED-Steuerung und Display-Ausgabe

## Aufbau & Architektur

Die Software ist modular aufgebaut:
- `main.py`: Hauptlogik
- `lib/`: Bibliotheken für Komponenten (Keypad, Motor, LEDs, etc.)
- `config/`: Konfigurationsdateien zur Definition von Produkten, Passwörtern und Verhalten

## Team

| Name     | Aufgabenbereich                      |
|----------|--------------------------------------|
| Karim    | Konstruktion, Holzdesign             |
| Jakob    | Programmierung, Systemlogik          |
| Jonas    | Entwicklung der Bibliotheken, Extras |

## Ziel

Dieses Projekt ist im Rahmen eines Schulprojekts entstanden und verbindet Hardwaresteuerung mit Softwareentwicklung. Es fördert technische Fähigkeiten, Teamarbeit und Kreativität.

## Medien

Screenshots, Aufbaupläne und Demonstrationen folgen im Verlauf des Projekts.

---

> Entwickelt mit Sorgfalt, Neugier und einer Prise Zucker.
