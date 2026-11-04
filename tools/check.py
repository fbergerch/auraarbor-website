#!/usr/bin/env python3
"""Prüfskript für auraarbor.com – muss vor jeder Auslieferung mit 0 Fehlern enden.

  python3 tools/check.py            Struktur-, Inhalts- und Link-Prüfung (läuft auch in GitHub Actions)
  python3 tools/check.py --browser  zusätzlich Desktop/Handy im Browser rendern (Playwright, lokal)

Fehler (ERROR) blockieren den Upload, Hinweise (WARN) nicht.
Regeln nie lockern, um einen Fehler zu umgehen – ausser der Nutzer will die Regel bewusst ändern
(dann README und dieses Skript gemeinsam anpassen).
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "tools"))

# ---------- Konfiguration ----------
HUBSPOT_PORTAL = "146961124"
HUBSPOT_FORM = "990b16c2-4f05-4b2a-bd91-cb6632b121a1"
CONTACT_EMAIL = "hello@auraarbor.com"
ADDRESS_LINES = ["c/o Berger Digital Partners", "Quaistrasse 53", "4632 Trimbach"]
REQUIRED_PAGES = ["index.html", "environments.html", "coaching-tools.html", "spatial-objects.html",
                  "faq.html", "imprint.html", "privacy-policy.html", "404.html"]
ALLOWED_EXTERNAL_HOSTS = {
    "fonts.googleapis.com", "fonts.gstatic.com",   # Webfonts (in Datenschutz erwähnen)
    "api.hsforms.com",                              # HubSpot Forms API (Formularversand)
    "auraarbor.com",                                # eigene Domain (canonical, og:image)
    "www.sitemaps.org", "schema.org", "www.w3.org", # Namespaces, keine Requests
}
# Veraltete Angaben, die nirgends mehr vorkommen dürfen
FORBIDDEN = {  # Regex (Gross-/Kleinschreibung egal) → Begründung
    r"Hirschengraben": "alte Adresse – neu: c/o Berger Digital Partners, Quaistrasse 53, 4632 Trimbach",
    r"Built in Lucerne": "Claim lautet «Built in Switzerland»",
    r"VRFX|Lucerne": "Aura Arbor wird ohne Firmen- und Ortsnennung als «developed in Switzerland» beschrieben",
    r"lorem ipsum": "Platzhaltertext",
    r"\bVR[- ]apps?\b": "Positionierung: «immersive coaching platform», nie «VR app»",
}
# British spellings → American English
BRITISH = ["colour", "organisation", "behaviour", "centre", "optimise", "realise", "favourite"]

errors, warns = [], []
def err(msg): errors.append(msg)
def warn(msg): warns.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.h1, self.title, self.meta = [], set(), 0, "", {}
        self.lang, self.canonical, self.imgs_no_alt, self._in_title = None, None, 0, False
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "html": self.lang = a.get("lang")
        if tag == "h1": self.h1 += 1
        if tag == "title": self._in_title = True
        if tag == "meta" and a.get("name"): self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        if tag == "img" and "alt" not in a: self.imgs_no_alt += 1
        for k in ("href", "src"):
            if a.get(k): self.links.append((tag, k, a[k]))

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False

    def handle_data(self, data):
        if self._in_title: self.title += data
        self.text.append(data)


def check_generated_in_sync():
    try:
        import build
    except Exception as e:  # noqa: BLE001
        err(f"tools/build.py lässt sich nicht laden: {e}")
        return
    for name, content in build.render().items():
        p = SITE / name
        if not p.exists():
            err(f"site/{name} fehlt – python3 tools/build.py ausführen")
        elif p.read_text(encoding="utf-8") != content:
            err(f"site/{name} weicht von tools/build.py ab – Inhalte nur in build.py ändern, dann neu bauen")


def check_pages():
    pages = {}
    for name in REQUIRED_PAGES:
        if not (SITE / name).exists():
            err(f"Pflichtseite fehlt: site/{name}")
    for p in sorted(SITE.glob("*.html")):
        parser = Page()
        parser.feed(p.read_text(encoding="utf-8"))
        pages[p.name] = parser
    for name, pg in pages.items():
        if pg.lang != "en": err(f"{name}: <html lang=\"en\"> fehlt")
        if not pg.title.strip(): err(f"{name}: <title> fehlt")
        elif len(pg.title) > 65: warn(f"{name}: Titel länger als 65 Zeichen ({len(pg.title)})")
        d = pg.meta.get("description", "")
        if not d: err(f"{name}: meta description fehlt")
        elif not 50 <= len(d) <= 165: warn(f"{name}: meta description {len(d)} Zeichen (ideal 50–160)")
        if pg.h1 != 1: err(f"{name}: genau eine <h1> erwartet, gefunden {pg.h1}")
        if name not in ("404.html",) and not pg.canonical: err(f"{name}: canonical fehlt")
        if pg.imgs_no_alt: err(f"{name}: {pg.imgs_no_alt} Bild(er) ohne alt-Attribut")

        for tag, attr, url in pg.links:
            if url.startswith(("mailto:", "tel:", "data:")):
                continue
            m = re.match(r"https?://([^/]+)", url)
            if m:
                host = m.group(1)
                if host not in ALLOWED_EXTERNAL_HOSTS:
                    err(f"{name}: externer Host nicht freigegeben: {host} – zuerst Datenschutz anpassen, dann in ALLOWED_EXTERNAL_HOSTS aufnehmen")
                continue
            path, _, frag = url.partition("#")
            target = name if not path else path
            fp = SITE / target
            if not fp.exists():
                if target.startswith("assets/img/") and attr == "src" and tag == "img":
                    warn(f"{name}: Bild noch nicht vorhanden: {target} (Platzhalter wird angezeigt)")
                elif target.startswith("assets/img/"):
                    warn(f"{name}: Datei noch nicht vorhanden: {target}")
                else:
                    err(f"{name}: Link-Ziel fehlt: {url}")
                continue
            if frag and target.endswith(".html"):
                ids = pages[target].ids if target in pages else set()
                if frag not in ids:
                    err(f"{name}: Anker #{frag} existiert nicht in {target}")
    return pages


def check_text_rules(pages):
    for p in list(SITE.rglob("*.html")) + list(SITE.rglob("*.js")) + list(SITE.rglob("*.css")) + [ROOT / "tools/build.py"]:
        t = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        for bad, why in FORBIDDEN.items():
            m = re.search(bad, t, re.IGNORECASE)
            if m:
                err(f"{rel}: «{m.group(0)}» gefunden – {why}")
        if p.suffix == ".html":
            low = t.lower()
            for w in BRITISH:
                if re.search(rf"\b{w}", low):
                    warn(f"{rel}: britische Schreibweise «{w}» – American English verwenden")
            if "ß" in t:
                err(f"{rel}: «ß» gefunden")
    for name, pg in pages.items():
        if name == "404.html":
            continue
        body = " ".join(pg.text)
        if CONTACT_EMAIL not in body:
            err(f"{name}: Kontakt-E-Mail {CONTACT_EMAIL} fehlt")
        for line in ADDRESS_LINES:
            if line not in body:
                err(f"{name}: Adresszeile «{line}» fehlt im Footer")


def check_form():
    js = (SITE / "assets/js/main.js").read_text(encoding="utf-8")
    if f'portalId: "{HUBSPOT_PORTAL}"' not in js: err("main.js: HubSpot portalId stimmt nicht mit tools/check.py überein")
    if f'formGuid: "{HUBSPOT_FORM}"' not in js: err("main.js: HubSpot formGuid stimmt nicht mit tools/check.py überein")
    idx = (SITE / "index.html").read_text(encoding="utf-8")
    for fid in ["firstname", "lastname", "email", "company", "prev_app", "prev_other", "beta_tester",
                "horizon_user", "horizon_mail", "other_device", "d-none", "website", "submit", "next", "back", "done"]:
        if f'id="{fid}"' not in idx:
            err(f"index.html: Formularfeld #{fid} fehlt (main.js erwartet es)")
    if (SITE / ".htaccess").exists() is False:
        err("site/.htaccess fehlt (saubere URLs, 404, HTTPS auf Hoststar)")


def check_browser():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        warn("--browser: Playwright nicht installiert (pip install playwright && playwright install chromium) – übersprungen")
        return
    import threading, http.server, functools, socketserver
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(SITE))
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    shots = ROOT / "dist" / "screenshots"
    shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for label, w in (("desktop", 1440), ("mobile", 390)):
            pg = b.new_page(viewport={"width": w, "height": 900})
            console = []
            pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: console.append(str(e)))
            for name in REQUIRED_PAGES:
                console.clear()
                pg.goto(f"http://127.0.0.1:{port}/{name}", wait_until="networkidle")
                sw = pg.evaluate("document.documentElement.scrollWidth")
                if sw > w + 1:
                    err(f"{name} ({label}): seitliches Scrollen – Breite {sw}px > {w}px")
                real = [c for c in console if "Failed to load resource" not in c and "fonts.g" not in c]
                for c in real:
                    err(f"{name} ({label}): JS-Fehler: {c[:160]}")
                pg.screenshot(path=str(shots / f"{name[:-5]}-{label}.png"), full_page=True)
        b.close()
    srv.shutdown()
    print(f"Screenshots: {shots.relative_to(ROOT)}/")


if __name__ == "__main__":
    check_generated_in_sync()
    pages = check_pages()
    check_text_rules(pages)
    check_form()
    if "--browser" in sys.argv:
        check_browser()
    for w in warns: print("WARN ", w)
    for e in errors: print("ERROR", e)
    print(f"\n{len(errors)} Fehler, {len(warns)} Hinweise")
    sys.exit(1 if errors else 0)
