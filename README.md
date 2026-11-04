# auraarbor.com

Website von **Aura Arbor**, der immersiven Coaching-Plattform. Statisches HTML/CSS/JS ohne Framework, gehostet bei Hoststar, automatisch veröffentlicht über GitHub Actions.

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `site/` | **Alles, was auf den Server kommt** |
| `site/*.html` | Seiten – werden von `tools/build.py` erzeugt, nie von Hand bearbeiten |
| `site/assets/css/styles.css` | Design-Tokens und alle Styles |
| `site/assets/js/main.js` | Menü, Bild-Platzhalter, Early-Access-Formular → HubSpot |
| `site/assets/img/` | Bilder (Liste und Formate: `docs/images.md`) |
| `site/.htaccess` | HTTPS, www-Weiterleitung, URLs ohne `.html`, 404 |
| `tools/build.py` | **Alle Seiteninhalte** und gemeinsamer Header/Footer; erzeugt `site/*.html`, `sitemap.xml`, `robots.txt` |
| `tools/check.py` | Prüfskript – muss vor jeder Auslieferung fehlerfrei laufen |
| `tools/build.sh` | Bauen + prüfen + ZIP für manuellen Upload nach `dist/` |
| `.github/workflows/deploy.yml` | Automatische Veröffentlichung per SFTP zu Hoststar nach jedem Push auf `main` |
| `docs/betrieb-und-hosting.md` | Hosting, Secrets, Domain-Umzug, HubSpot |
| `docs/images.md` | Bildliste mit Dateinamen und Formaten |

## Ablauf bei jeder Änderung

1. Repository holen bzw. aktualisieren (`git pull`).
2. Inhalt in `tools/build.py` ändern (Styles in `styles.css`, Formularlogik in `main.js`).
3. `python3 tools/build.py`
4. `python3 tools/check.py --browser` → muss mit **0 Fehler** enden. Screenshots liegen danach in `dist/screenshots/`.
5. Vorschau ansehen (Desktop 1440 px, Handy 390 px), bei Bedarf als Artefakt zum Kommentieren.
6. Commit mit kurzer deutscher Beschreibung, `git push` auf `main`.
7. GitHub prüft erneut und lädt `site/` per SFTP zu Hoststar (Actions › «Website veröffentlichen»). Schlägt die Prüfung fehl, wird nichts hochgeladen.

## Regeln

**Inhalt und Sprache**
- Website-Texte in **American English** (color, organize, center …). Kein «ß».
- Positionierung: Aura Arbor ist eine **immersive coaching platform** – nie «VR app». VR ist das heutige Medium, nicht das Produkt.
- Zielgruppe der Website sind **Coaches**; Clients sind die Nutzniessenden.
- Avatar-Thema ausgewogen formulieren («A different kind of presence»): nicht als reinen Vorteil verkaufen – manche Coaches vermissen die Mimik.
- Jede Sektionsüberschrift muss alle Karten/Punkte darunter abdecken.
- Öffentlich **nicht** verwenden: Marktgrössen, Wettbewerbsvergleiche, Preise/Business-Modell, Funding, datierte Roadmap. Die Website verkauft ein Werkzeug, nicht ein Investment.
- Keine erfundenen Zahlen, Kunden oder Zitate. Testimonials nur mit schriftlicher Freigabe der Person.
- Claim im Hero: «Built in Switzerland». Herkunft nur als «developed in Switzerland» – kein VRFX, kein Lucerne.

**Kontakt**
- Adresse: Aura Arbor, c/o Berger Digital Partners, Quaistrasse 53, 4632 Trimbach, Switzerland · hello@auraarbor.com
- Bei Änderung: `tools/build.py` (Footer, Impressum) **und** `ADDRESS_LINES` / `CONTACT_EMAIL` in `tools/check.py` anpassen.

**Technik**
- Seiten nur über `tools/build.py` ändern; `check.py` meldet Abweichungen.
- Neuer externer Dienst (Analytics, Video, Karte, weitere Fonts …) → zuerst `privacy-policy` anpassen, dann Host in `ALLOWED_EXTERNAL_HOSTS` freigeben. Im Zweifel fragen.
- Relative Links (`environments.html`, `assets/...`), damit die Seite lokal und auf jedem Pfad funktioniert.
- Neue Bilder: WebP, Format und Breite laut `docs/images.md`, `alt`-Text auf Englisch. Hero-Motiv rechts, links liegt ein Verlauf über dem Bild.
- Formular: Feldnamen müssen dem HubSpot-Formular entsprechen (Portal 146961124). Neue Felder zuerst in HubSpot anlegen.
- Prüfregeln nie lockern, um einen Fehler zu umgehen – ausser der Nutzer will die Regel bewusst ändern; dann README und `check.py` gemeinsam anpassen.

## Lokal ansehen

```bash
python3 -m http.server 8000 --directory site
# http://localhost:8000
```
