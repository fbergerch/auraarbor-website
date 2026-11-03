# auraarbor.com

Static website for **Aura Arbor**, the immersive coaching platform by VRFX Realtime Studio GmbH, Lucerne.
Plain HTML, CSS and JavaScript. No framework, no build dependencies.

## Structure

```
index.html              Home (hero, problem, features, voices, how it works, why now, early access form)
environments.html       Environments
coaching-tools.html     Coaching Tools
spatial-objects.html    Spatial Objects
faq.html                FAQ (with FAQPage structured data)
imprint.html            Imprint            (legal text still to migrate)
privacy-policy.html     Privacy Policy     (legal text still to migrate + website/HubSpot section)
404.html                Not found page
assets/css/styles.css   Design tokens and all styles
assets/js/main.js       Menu, image fallbacks, early access form → HubSpot
assets/img/             Images (see assets/img/README.md for the file list)
tools/build.py          Generates the .html pages from shared header/footer
```

## Editing content

Page content lives in `tools/build.py`. Edit it, then rebuild:

```bash
python3 tools/build.py
```

Commit both `tools/build.py` and the generated `.html` files. Styles and the form script are edited directly in `assets/`.

## Early access form → HubSpot

The form is rendered natively and posts to the HubSpot Forms API v3:

- Portal ID: `146961124`
- Form GUID: `990b16c2-4f05-4b2a-bd91-cb6632b121a1`

Field names match the existing HubSpot form (`firstname`, `lastname`, `email`, company `name`, `previous_applications_used`, `previous_other_application_used`, `i_m_interested_in_becoming_a_beta_tester_`, `vr_device`, `meta_horizon_username`, `meta_horizon_account_email`, `other_vr_devices`). Submissions land in the same form, so existing HubSpot notifications and workflows keep working. A honeypot field filters simple bots.

`vr_device` is sent as a semicolon-separated list, which is what HubSpot expects for multi-checkbox properties.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Hosting

Works on any static host. On GitHub Pages: Settings → Pages → Deploy from branch `main`, folder `/`. Old URLs like `/environments` resolve to `environments.html` automatically. Point the domain only once the site is ready to replace the HubSpot version.
