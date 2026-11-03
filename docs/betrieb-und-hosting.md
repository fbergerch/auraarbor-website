# Betrieb und Hosting – auraarbor.com

Die Website liegt auf dem bestehenden **Hoststar**-Hosting. Quelle der Wahrheit ist dieses Repository; Änderungen gehen über GitHub automatisch live.

## 1. Hochladen

**Automatisch (Standard):** Jede Änderung auf `main` unter `site/` oder `tools/` wird von GitHub geprüft (`tools/check.py`) und per SFTP (Port 5544) zu Hoststar hochgeladen. Status: Repository › **Actions** › «Website veröffentlichen». Manuell auslösen: dort **Run workflow**.

Einmalig einzurichten unter Repository › **Settings › Secrets and variables › Actions › New repository secret**:

| Secret | Inhalt |
| --- | --- |
| `FTP_SERVER` | Hoststar-Servername `lx#.hoststar.hosting` (My Panel › Hosting › Übersicht) – nicht die eigene Domain |
| `FTP_USERNAME` | FTP-Benutzer **der Domain auraarbor.com** (Besitzer `auraarbo…`) |
| `FTP_PASSWORD` | Passwort dieses Benutzers |
| `FTP_SERVER_DIR` | **`public_html`** |
| `FTP_PORT` | optional, Standard `5544` |

**Wichtig:** Der Domain-Benutzer von auraarbor.com ist von Hoststar in den Ordner `auraarbor.com` eingesperrt – für ihn ist dieser Ordner die Wurzel. Deshalb lautet der Pfad nur `public_html`, nicht `auraarbor.com/public_html` (so zeigt ihn FileZilla nur beim Hauptbenutzer an). Andere Domains (bergerpartners.ch, berger.tv) kann dieser Login nicht erreichen – eine Verwechslung ist ausgeschlossen.

Existiert der Zielordner nicht, bricht der Workflow vor dem Upload ab und listet im Log das Startverzeichnis, den Inhalt von `public_html` und den Titel der dortigen Startseite auf.

Beim ersten Lauf werden alle Dateien hochgeladen, danach nur noch geänderte. Dateien auf dem Server, die nicht aus diesem Repository stammen, bleiben unangetastet (auch nach dem Löschen einer Datei im Repo – dann auf dem Server von Hand entfernen).

**Manuell (Reserve):** `bash tools/build.sh` → Inhalt von `dist/auraarbor-website.zip` (nicht den Ordner selbst) per SFTP ins Web-Verzeichnis der Domain kopieren.

Nur der Inhalt von `site/` kommt auf den Server – `docs/` und `tools/` nicht.

## 2. Domain von HubSpot zu Hoststar umziehen (einmalig)

1. ✓ Domain auraarbor.com ist in Hoststar angelegt, erster Upload am 03.11.2026 erfolgreich.
2. Seite vor der DNS-Umstellung prüfen (z. B. über die Vorschau-Funktion im Hoststar My Panel oder einen Eintrag in der lokalen hosts-Datei).
3. SSL-Zertifikat (Let's Encrypt) für `auraarbor.com` und `www.auraarbor.com` in Hoststar aktivieren.
4. DNS umstellen: A-/AAAA-Record von `auraarbor.com` und `www` auf Hoststar zeigen lassen (Werte laut Hoststar). Wo die DNS heute verwaltet werden, steht beim Domain-Registrar.
5. **E-Mail nicht vergessen:** MX-/SPF-Einträge für `hello@auraarbor.com` beim Umstellen unverändert übernehmen.
6. In HubSpot unter Einstellungen › Domains & URLs die Domain auraarbor.com als Website-Domain trennen. Die **Formulare und Kontakte bleiben** erhalten – das neue Formular sendet weiter an dasselbe HubSpot-Formular.
7. Nach der Umstellung: Formular einmal testen und prüfen, ob der Eintrag in HubSpot ankommt.

Die `.htaccess` sorgt für HTTPS, leitet `www` auf die nackte Domain um, liefert die alten URLs ohne `.html` aus (`/environments`, `/privacy-policy` …) und zeigt `404.html` für fehlende Seiten.

## 3. Formular → HubSpot

- Portal-ID `146961124`, Formular-GUID `990b16c2-4f05-4b2a-bd91-cb6632b121a1` (in `site/assets/js/main.js` und `tools/check.py`).
- Versand über die HubSpot Forms API v3, ohne API-Schlüssel. Felder entsprechen dem bestehenden HubSpot-Formular.
- Neue Felder: zuerst in HubSpot im Formular ergänzen, dann in `tools/build.py` (Markup) und `main.js` (Versand).

## 4. Offene Punkte vor dem Livegang

- Impressum- und Datenschutztext aus HubSpot übernehmen; Datenschutz um Website-Abschnitt (HubSpot-Formular, Google Fonts) ergänzen.
- Bilder liefern (Liste: `docs/images.md`).
- Testimonials: schriftliche Freigabe der genannten Coaches.
- FAQ-Aussagen bestätigen (Headset-Miete, 30–45 Minuten, keine Aufzeichnung, Early Access kostenlos) und Whiteboard-Aussage (Client schreibt mit).
