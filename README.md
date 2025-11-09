# 🕸️ Google Maps Web Scraper

Dieses Projekt durchsucht **Google Maps** nach einem bestimmten *Topic* (z. B. „Apotheken“) und sammelt Informationen zu den gefundenen Einträgen.  
Es extrahiert bis zu **100 Ergebnisse**, speichert deren URLs (falls vorhanden) und ruft anschließend die jeweilige Webseite auf, um **Name** und **E-Mail-Adresse** zu extrahieren.  
Der Output ist eine **CSV-Datei**, die folgende Spalten enthält: Name, URL, E-Mail

## 🚀 Features

- 🔍 Automatisierte Suche auf **Google Maps** nach einem beliebigen Thema (z. B. Restaurants, Apotheken, Zahnärzte …)  
- 📄 Extraktion der Webseiten-URLs aus den Suchergebnissen (max. 100)  
- ✉️ Besuch jeder Webseite zur automatischen Erkennung von **E-Mail-Adressen** und **Namen**  
- 💾 Export aller Ergebnisse als **CSV-Datei**  

