---
title: Contributions
parent: Team Evaluation
nav_order: 4
---

{: .label }
[PartWatch]

{: .no_toc }
# Summary of individual contributions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Tim Luhmann]

Contributions
: # Automotive Parts Marketplace - Entwicklungstagebuch

## Oktober 2024

### 13.10. - GitHub Pages und Startseite
- Erstellung von GitHub Pages
- Anpassung der `index.md` mit allgemeinen Informationen

### 21.10. - Login und Registrierung
- Löschen von unnötigen Template-HTMLs
- Erstellen von `login.html` und `register.html`
- Referenz: [GeeksforGeeks Tutorial](https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/)
- Anpassung der `base.html` für Login-Status
  - Dynamische Anzeige von Login/Logout/Register
  - Grundgerüst für weitere Seiten

### 24.10. - Benutzerrollen
- Hinzufügen der Rollen "Customer" und "Supplier"
- Integration in `base.html` und `register.html`

### 25.10. - Angebots-Funktionalität
- Button "+ Automotive Part" für Supplier
- Neue Route in `app.py`
- Erstellung der `catalogue_index`
  - Login-Button rechts oben
  - Platzhalter für Logo
  - Zwei Teile mit verdeckten Informationen

### 26.10. - Angebotserstellung
- Seite "Offer New Automotive Part"
- Formular mit Feldern:
  - Supplier
  - Preis
  - Verfügbarkeit
  - Menge
  - Geschätzte Lieferzeit
- Bild-Upload-Funktionalität
- Erstellung `OfferPartForm` in `forms.py`
  - Integration von FloatField, SelectField, FileField

## November 2024

### 29.10. - Katalog-Entwicklung
- Erstellung `catalogue.html`
- Datenbankabfrage für Teile
- Verlinkung zwischen Katalogseiten

### 01.11. - Weitere Funktionen
- Geplant:
  - Filtermöglichkeit nach Modell/Hersteller
  - Suchleisten-Positionierung
  - Hintergrundfarben-Anpassung

### 04.11. - Navigation
- Navbar-Dropdown implementiert
- Bootstrap-Struktur
- Referenzen:
  - [Bootstrap Navbar](https://getbootstrap.com/docs/4.0/components/navbar/)
  - [Dropdown-Tutorial](https://www.youtube.com/watch?v=VQWu4e6agPc)

### 05.11. - Kaufprozess
- Kaufformular in `forms.py`
- Neues Datenbankmodell
- Route für Artikeldetails
- `view_item.html` mit:
  - Produktdetails
  - Kaufformular
  - Kreditkartenoptionen

### 06.11. - Benutzerführung
- "How to use" Button
- Sprechblase mit Tutorial
- Kontextabhängige Anzeige

### 09.11. - Erweiterungen
- "How to use" nur für authentifizierte Nutzer
- CSS-Optimierung
- "My Orders" Seite
  - Anzeige von Benutzer-Käufen

### 01.12. - Weitere Verbesserungen
- Out-of-Stock-Banner
- "My Listings" für Supplier
  - Eigene Listings ansehen
  - Bearbeiten/Löschen von Artikeln
- Architektur-Dokumentation erstellt

### 14.12. - Zahlungsprozess
- Nur Vorkasse
- Vereinfachte Datenbankspeicherung
- Zusammenfassen mehrerer Teile pro Bestellung

## [Joe Doe]

Contributions
: Diam nonumy eirmod
: Tempor invidunt ut labore
: ...
