# 💡 Feature-Ideen für Useful Utilities Collection

Basierend auf einer Code-Analyse der bestehenden Architektur (PySide6/Qt, modulares Page-System, Service-Layer, Toast-Benachrichtigungen, Settings-Persistierung über QSettings).

---

## 1. Erweiterte Mikrofon-Guard-Funktionen

### 1.1 App-Whitelist / -Blacklist
- Bestimmte Apps dürfen den Pegel ändern, ohne dass der Guard zurücksetzt (z.B. Discord bei Voice-Chats).
- Erkennung über Window-Title oder Prozessname (via `pycaw`/`psutil`).

### 1.2 Per-App / Per-Kontext-Profile
- Unterschiedliche Zielpegel je nach aktivem Fenster (z.B. 80% für Teams, 100% für Streaming).
- Schnell-Umschaltung zwischen Profilen per Tray oder Hotkey.

### 1.3 Pegel-Historie & Visualisierung
- Live-Graph im Dashboard, der den tatsächlichen Pegel über die letzten Minuten anzeigt.
- Korrektur-Historie mit Timestamps (bereits in `last_correction_text` gespeichert, aber nicht visualisiert).

### 1.4 Geräuschpegel-gesteuerter Guard
- Automatische Deaktivierung des Guards, wenn für X Sekunden kein Geräusch erkannt wird (via `sounddevice` Stream).
- Spart Ressourcen und verhindert unnötige Korrekturen bei Stille.

### 1.5 Geräte-Synchronisation
- Mehrere Mikrofone gleichzeitig auf denselben Zielpegel bringen.
- Per-Device Auto-Restore (bereits teilweise vorhanden, aber UI-seitig nicht ausgebaut).

### 1.6 Mikrofon-Test / Kalibrierung
- Kurze Testaufnahme, um Empfindlichkeit zu prüfen.
- Pegel-Visualisierung während der Aufnahme.

---

## 2. Input-Lock-Erweiterungen

### 2.1 Timer / Countdown-Sperre ~~(geplant)~~ ✅ IMPLEMENTIERT
- "Sperre in 5 Minuten" – nützlich für geplante Reinigungsphasen oder Pausen.
- Countdown-Anzeige in der Seite (Eingabesperre) mit Preset-Dropdown (30s, 1min, 5min, 10min, 30min, 1h, Custom, Unbegrenzt).
- Custom-Eingabe mit Einheitenwahl (Sekunden/Minuten/Stunden).
- Start/Stop-Buttons, automatische Freigabe bei Ablauf.
- Verbleibende Zeit als MM:SS oder HH:MM:SS.

### 2.2 Touchpad-Sperre
- Zusätzlich zu Tastatur/Maus das Touchpad temporär deaktivieren (via `pydirectinput` oder Touchpad-Treiber-Hook).
- Besonders nützlich für Laptop-Reinigung.

### 2.3 Automatische Sperre bei Inaktivität
- Wenn X Minuten keine Eingabe, automatisch Tastatur sperren (zum Schutz vor Staub).
- Whitelist für bestimmte Apps (z.B. VS Code während Coding).

### 2.4 Bildschirmsperre / Überlagerung
- Optional: Schwarz-Overlay über den Bildschirm legen, wenn Maus gesperrt ist.
- Verhindert versehentliches Anklicken von Passwortfeldern.

### 2.5 Hotkey-Profile
- Verschiedene Unlock-Hotkeys je nach Kontext (Arbeit vs. Privat).

---

## 3. Dashboard & Status-Monitoring

### 3.1 System-Info-Karten
- CPU-Auslastung, RAM, Temperatur (via `psutil`).
- Netzwerk-Status (online/offline, aktive Verbindungen).
- Batterie-Status für Laptops (via `psutil`).

### 3.2 Live-Pegelkurve im Dashboard
- Echtzeit-Verlauf des Mikrofonpegels als kleiner Sparkline-Graph.
- Korrektur-Ereignisse als Marker im Graph.

### 3.3 Ereignis-Log
- Tabellenansicht aller Sperrungen, Korrekturen und Statusänderungen.
- Export als CSV/JSON.

---

## 4. UI / UX-Verbesserungen

### 4.1 Theme-Toggle (Dark / Light / System)
- Aktuell ist das Theme hart auf Dark mode fixiert.
- Helles Theme + automatische Erkennung der Windows-Farbeinstellungen (`uiautomation` oder Registry).

### 4.2 Akzentfarben wählen
- Nutzer können die App-Akzentfarbe individuell setzen (Blau, Grün, Lila, etc.).
- Umschaltung ohne Neustart via Qt Dynamic Stylesheet.

### 4.3 Sidebar-Position
- Optionale Links-Positionierung der Sidebar (aktuell nur links, aber manche Nutzer bevorzugen rechts).

### 4.4 Mini-Kompressions-Modus
- Kompakte Seitenleiste ohne Beschriftungen (nur Icons) für mehr Content-Platz.
- Nützlich auf kleinen Bildschirmen/Tablets.

### 4.5 Erweiterte Tray-Interaktionen
- Tray-Icon-Doppelklick öffnet direkt die letzte Seite (statt nur Show/Hide).
- Tray-Kontextmenü mit Schnellzugriff auf "Guard an/aus", "Maus sperren", etc.

### 4.6 Globale Hotkeys für alle Hauptfunktionen
- Aktuell nur ein Hotkey (Mouse-Unlock).
- Weitere Hotkeys: Guard toggeln, Keyboard sperren, App ein/ausblenden.

### 4.7 Toast-Historie
- Verpasste Toasts werden in einem kleinen Overlay oder der Sidebar gesammelt.
- "Du hast 3 neue Benachrichtigungen".

### 4.8 Animations-Check
- Toast-Bug ist behoben; weitere Animationen prüfen (Seitenwechsel, Hover-Effekte).

---

## 5. Performance & Robustheit

### 5.1 Polling-Intervall dynamisch anpassen
- Bei hoher CPU-Last oder Akkubetrieb (`psutil.sensors_battery`) das Polling-Intervall automatisch erhöhen.
- Spart Akku auf Laptops.

### 5.2 CPU-Limiter
- Maximal X% CPU-Zeit für den Guard-Timer; bei Überschreitung Intervall vergrößern.

### 5.3 Graceful Degradation
- Wenn `pycaw`/`comtypes` fehlschlägt, Fallback auf `sounddevice`-API.
- Wenn beide fehlschlagen, klare Fehlermeldung statt Crash.

### 5.4 Multi-Monitor-Support
- Sidebar und Fenster merken sich pro Monitor Position und Größe.
- Tray-Icon auf allen Monitoren sichtbar halten.

### 5.5 High-DPI / 4K-Verbesserungen
- Skalierungsfaktor pro Monitor berücksichtigen (`devicePixelRatio`).
- Icons und Fonts in höheren Auflösungen bereitstellen.

---

## 6. Datenschutz & Sicherheit

### 6.1 Privacy-Dashboard
- Übersicht: "Wie oft wurde das Mikrofon korrigiert?", "Welche Apps wurden erkannt?".
- Alle Daten lokal; keine Cloud-Anbindung.

### 6.2 Mikrofon-Zugriffs-Log
- Windows Event Log oder `pycaw`-Änderungs-Hook nutzen, um zu loggen, **welche App** den Pegel wann geändert hat.
- Höhere Transparenz für den Nutzer.

### 6.3 Automatische Deaktivierung bei bestimmten Apps
- Wenn Teams/Discord/Zoom erkannt wird, Guard automatisch auf "nur warnen" statt "sofort korrigieren" umstellen.

---

## 7. Einstellungen & Verwaltung

### 7.1 Export/Import der Einstellungen
- `settings.json` exportieren/importieren, um Konfiguration auf anderen PCs zu übertragen.
- Nützlich nach Neuinstallation.

### 7.2 Backup / Restore
- Automatisches Backup der Einstellungen in `%APPDATA%`.
- Wiederherstellung nach Crash oder Deinstallation.

### 7.3 Startup-Optimierung
- Aktuell wird die App bei Autostart direkt gestartet.
- Optional: Nur Tray-Icon beim Start, Hauptfenster erst bei Bedarf öffnen (Performance-Gewinn).

---

## 8. Entwickler- & Power-User-Features

### 8.1 Debug-Modus & erweitertes Logging
- `--debug` CLI-Flag für detaillierte Konsolenausgaben.
- Log-Datei unter `%LOCALAPPDATA%` mit Rotation.

### 8.2 Simulierte Korrekturen
- Einstellungsseite: "Test-Korrektur simulieren" für Debug-Zwecke.
- Ohne tatsächliche Volume-Änderung, nur UI-Feedback.

### 8.3 Plugin-System (langfristig)
- Modulare Erweiterungen via Entry-Points (`importlib.metadata`).
- Dritte könnten eigene Pages (z.B. Battery Monitor, Clipboard Manager) hinzufügen.

### 8.4 CLI-Schnittstelle
- `uuc --toggle-guard`, `uuc --lock-keyboard`, `uuc --status`.
- Nützlich für Skripte und Automatisierung.

---

## 9. Barrierefreiheit (Accessibility)

### 9.1 Screen-Reader-Support
- Bessere `accessibleName` und `accessibleDescription` Properties auf allen Widgets.
- Testen mit Windows Narrator / NVDA.

### 9.2 Hoher Kontrast / Vergrößerung
- Theme-Variante mit höheren Kontrasten.
- Schriftgröße und UI-Skalierung in den Einstellungen anpassbar.

### 9.3 Tastaturnavigation
- Sicherstellen, dass alle Seiten komplett per Tab erreichbar sind.
- Focus-Indikatoren verbessern.

---

## 10. Internationalisierung (i18n)

### 10.1 Weitere Sprachen
- Französisch, Spanisch, Japanisch etc. sind bereits im Sprach-Dropdown gelistet, aber nicht übersetzt.
- Community-Translation via Crowdin oder PO-Files.

### 10.2 Regionale Formate
- Datums- und Zeitformate je nach Locale anpassen (aktuell hardcoded `dd.mm.yyyy`).
- Tausender-Trennzeichen, Währungssymbole (falls später monetäre Features dazu kommen).

---

## Priorisierung (Vorschlag)

| Priorität | Feature | Aufwand | Nutzen |
|-----------|---------|---------|--------|
| Hoch | App-Whitelist für Mic-Guard | Mittel | Hoch |
| Hoch | CPU-Limiter / Akku-Modus | Niedrig | Hoch |
| Hoch | Toast-Historie | Niedrig | Mittel |
| Hoch | ~~Timer / Countdown-Sperre~~ ✅ | Niedrig | Hoch |
| Hoch | Globale Hotkeys | Mittel | Hoch |
| Mittel | Pegel-Historie Graph | Mittel | Hoch |
| Mittel | Export/Import Settings | Niedrig | Mittel |
| Mittel | Debug-Modus & Logging | Niedrig | Mittel |
| Mittel | Privacy-Dashboard | Mittel | Mittel |
| Niedrig | Theme-Toggle | Hoch | Mittel |
| Niedrig | Plugin-System | Sehr Hoch | Niedrig |

---

*Erstellt am 21.07.2026 – soll als lebendes Dokument dienen und bei jedem Sprint geupdated werden.*
