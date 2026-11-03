#!/usr/bin/env python3
"""Builds the static pages of auraarbor.com from shared header/footer partials.

Run from the repo root:  python3 tools/build.py   (writes into site/)
Edit page content in the PAGES section below, then rebuild and commit the generated files.
Never edit site/*.html by hand: tools/check.py fails if they drift from this script.
No dependencies beyond the Python standard library.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
SITE = "https://auraarbor.com"
YEAR = 2026

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="none" stroke="#20B896" stroke-width="2.2"/>'
        '<path d="M16 27v-9" stroke="#20B896" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M16 18c0-5 3.5-8.5 9-9-.3 5.5-4 9-9 9z" fill="#20B896"/>'
        '<path d="M16 20c-.4-4-3.4-6.8-8-7 .2 4.4 3.4 7 8 7z" fill="#008C7A"/></svg>')
CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
NAV = [("environments.html", "Environments"), ("coaching-tools.html", "Coaching Tools"),
       ("spatial-objects.html", "Spatial Objects"), ("faq.html", "FAQ")]


def img(file, alt="", cls="", eager=False):
    """Image frame. Files live in assets/img; a tinted stand-in shows until they exist."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="frame {cls}" data-file="{file}">'
            f'<img src="assets/img/{file}" alt="{alt}" {load} decoding="async"></div>')


def header(active):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="index.html" aria-label="Aura Arbor home">{LOGO}AURA ARBOR</a>
      <ul class="nav-links" id="nav-links">{items}</ul>
      <a class="btn" href="index.html#beta">Join early access</a>
      <button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </nav>
  </div>
</header>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html">{LOGO}AURA ARBOR</a>
        <p style="max-width:32ch">An immersive coaching platform for professional coaches. Swiss-built, coach-shaped.</p>
      </div>
      <div>
        <h4>Contact</h4>
        <address>Aura Arbor<br>c/o Berger Digital Partners<br>Quaistrasse 53<br>4632 Trimbach, Switzerland<br><a href="mailto:hello@auraarbor.com">hello@auraarbor.com</a></address>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="environments.html">Environments</a></li>
          <li><a href="coaching-tools.html">Coaching Tools</a></li>
          <li><a href="spatial-objects.html">Spatial Objects</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="index.html#beta">Early access</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base"><span>© {YEAR} Aura Arbor. All rights reserved.</span><span><a href="imprint.html">Imprint</a> · <a href="privacy-policy.html">Privacy Policy</a></span></div>
  </div>
</footer>'''


def layout(slug, title, desc, body, active=None, extra_head="", og_image="og-image.jpg"):
    url = f"{SITE}/{'' if slug == 'index' else slug}"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aura Arbor">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F1D18">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&amp;family=Figtree:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
{extra_head}</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def cta_band(heading="Be among the first coaches inside.",
             text="We're onboarding a limited group of coaches for early access."):
    return f'''<section class="band-forest section-tight">
  <div class="wrap cta-band">
    <div><h2>{heading}</h2><p>{text}</p></div>
    <a class="btn" href="index.html#beta">Join the early access list</a>
  </div>
</section>'''


def page_hero(eyebrow, h1, sub, image, alt):
    return f'''<section class="hero hero-page">
  {img(image, alt, eager=True)}
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <span class="eyebrow light">{eyebrow}</span>
      <h1>{h1}</h1>
      <p>{sub}</p>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- PAGES

QUOTES = [
    ("CJ", "Clemens Joos", "Agile Coach",
     "What we found stunning is a quite simple but important trick the VR setting does: it minimizes distraction. In VR, you only and fully are present in the coaching.", "lead"),
    ("PA", "Philip Atkinson", "Professional Coach",
     "The app provided a safe space for good coaching. It enables even more intensive active listening. The coach feels safer and more comfortable coaching too. Absolutely love it.", ""),
    ("ML", "Michèle Landau", "Professional Coach",
     "It provides an environment which is void of background noise and enables us to see things more clearly and focus better on the coaching topic.", ""),
    ("PW", "Pinar Wennerberg", "Professional Coach",
     "I am mind blown. I truly believe that this app will open a whole world of possibilities for coaches and young humans.", ""),
    ("YH", "Youko Hamming", "Agile Coach",
     "My first impression was that it is very intuitive. I managed to find my way easily, even without the guide.", ""),
    ("C", "Coachee", "From the other side of the session",
     "It enabled me to be more sincere as I didn't feel perceived.", "client"),
]


def quotes_html():
    out = []
    for ini, name, role, text, kind in QUOTES:
        cls = {"lead": "quote quote-lead", "client": "quote quote-client"}.get(kind, "quote")
        out.append(f'''<figure class="{cls}">
          <blockquote>{text}</blockquote>
          <figcaption class="who"><span class="ini" aria-hidden="true">{ini}</span><span><b>{name}</b><small>{role}</small></span></figcaption>
        </figure>''')
    return "\n        ".join(out)


BETA_FORM = f'''<section class="section" id="beta">
  <div class="wrap beta-grid">
    <div class="beta-intro">
      <span class="eyebrow">Early access</span>
      <h2>Be among the first coaches inside.</h2>
      <p>We're onboarding a limited group of coaches for early access. You'll get hands-on time with the platform, direct access to the team, and real influence over what we build next.</p>
      <ul class="perks">
        <li>{CHECK}Run real sessions with your own clients</li>
        <li>{CHECK}Direct line to the product team</li>
        <li>{CHECK}Shape the features we build next</li>
      </ul>
    </div>

    <div class="form-card">
      <form id="beta-form" novalidate>
        <div class="progress" aria-hidden="true"><span class="on"></span><span id="bar-2"></span></div>

        <fieldset id="step-1">
          <legend class="step-label">Step 1 of 2</legend>
          <h3>About you</h3>
          <div class="fields">
            <div class="field"><label for="firstname">First name <span class="req" aria-hidden="true">*</span></label><input id="firstname" name="firstname" type="text" autocomplete="given-name" required><span class="err" aria-live="polite"></span></div>
            <div class="field"><label for="lastname">Last name <span class="req" aria-hidden="true">*</span></label><input id="lastname" name="lastname" type="text" autocomplete="family-name" required><span class="err" aria-live="polite"></span></div>
            <div class="field full"><label for="email">Email <span class="req" aria-hidden="true">*</span></label><input id="email" name="email" type="email" autocomplete="email" placeholder="We'll send updates and early access details here" required><span class="err" aria-live="polite"></span></div>
            <div class="field full"><label for="company">Company or coaching practice</label><input id="company" name="company" type="text" autocomplete="organization"></div>
            <label class="check field full"><input id="beta_tester" name="beta_tester" type="checkbox" checked> I'm interested in becoming a beta tester.</label>
            <div class="hp" aria-hidden="true"><label for="website">Website</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          </div>
          <div class="form-actions"><span></span><button class="btn" type="button" id="next">Continue</button></div>
        </fieldset>

        <fieldset id="step-2" hidden>
          <legend class="step-label">Step 2 of 2</legend>
          <h3>Your VR setup</h3>
          <div class="fields">
            <div class="field full"><label for="prev_app">Are you already using VR applications for coaching?</label>
              <select id="prev_app" name="prev_app">
                <option value="">Select an option</option>
                <option>Horizon Workrooms</option><option>Engage</option><option>Arthur</option><option>Other</option>
              </select></div>
            <div class="field full" id="prev_other_wrap" hidden><label for="prev_other">Which application?</label><input id="prev_other" name="prev_other" type="text"></div>
            <div class="field full"><span class="legend" id="device-legend">Which Meta Quest devices do you own or have access to?</span>
              <div class="chips" role="group" aria-labelledby="device-legend">
                <label class="chip"><input type="checkbox" name="vr_device" value="Meta Quest 3" id="d-q3"><span>Quest 3</span></label>
                <label class="chip"><input type="checkbox" name="vr_device" value="Meta Quest 3 S" id="d-q3s"><span>Quest 3S</span></label>
                <label class="chip"><input type="checkbox" name="vr_device" value="Meta Quest Pro" id="d-qp"><span>Quest Pro</span></label>
                <label class="chip"><input type="checkbox" name="vr_device" value="Meta Quest 2" id="d-q2"><span>Quest 2</span></label>
                <label class="chip"><input type="checkbox" name="vr_device" value="I don't have access to a Meta Quest Device" id="d-none"><span>None yet</span></label>
              </div></div>
            <div class="field" id="horizon_wrap"><label for="horizon_user">Meta Horizon username</label><input id="horizon_user" name="horizon_user" type="text" autocomplete="off"></div>
            <div class="field" id="horizon_mail_wrap"><label for="horizon_mail">Meta Horizon account email</label><input id="horizon_mail" name="horizon_mail" type="email" autocomplete="off"></div>
            <div class="field full"><label for="other_device">Using another headset? Tell us which</label><input id="other_device" name="other_device" type="text" placeholder="e.g. Pico 4, Apple Vision Pro"></div>
          </div>
          <div class="form-actions"><button class="btn-text" type="button" id="back">← Back</button><button class="btn" type="submit" id="submit">Join the early access list</button></div>
        </fieldset>

        <div id="done" class="success" hidden>
          <div class="badge"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg></div>
          <h3 tabindex="-1" style="margin:0">You're on the list.</h3>
          <p>Thanks for your interest in Aura Arbor. We'll be in touch personally at <b id="done-mail"></b> with next steps.</p>
        </div>

        <div class="form-foot" id="form-foot">
          <p>No cost during early access. We'll be in touch personally. You won't land in an automated funnel.</p>
          <p>We use your details only to contact you about Aura Arbor. See our <a href="privacy-policy.html">privacy policy</a>.</p>
        </div>
      </form>
    </div>
  </div>
</section>'''

SWISS = '<svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="4" fill="#D52B1E"/><path d="M13 6h6v7h7v6h-7v7h-6v-7H6v-6h7z" fill="#fff"/></svg>'

HOME = f'''<section class="hero hero-home" id="top">
  {img("hero-forest.webp", "", eager=True)}
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <span class="eyebrow light">Immersive coaching platform</span>
      <h1>Coaching that finally has room to breathe.</h1>
      <p>Aura Arbor is an immersive coaching platform for professional coaches. Meet your clients in a distraction-free virtual space where presence deepens, insight comes faster, and the work goes further than a video call ever allowed.</p>
      <div class="hero-cta">
        <a class="btn" href="#beta">Join the early access list</a>
        <a class="btn btn-ghost" href="#how">See how it works</a>
      </div>
      <div class="hero-meta">Built in Switzerland</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap problem-grid">
    <div class="section-head" style="margin:0">
      <span class="eyebrow">The problem</span>
      <h2>The session is right. The medium isn't.</h2>
    </div>
    <div>
      <div class="prose">
        <p>You know the moment. Your client is close to something real, and a notification pulls them away. A chat window blinks. Someone glances at a second monitor. The thread breaks, and you spend the next ten minutes finding it again.</p>
        <p>Video calls made coaching accessible to everyone, everywhere. But they also made it flat. Presence is hard to build through a screen, body language disappears into a rectangle, and the tools that make coaching powerful in a room (space, movement, metaphor, distance) simply don't translate.</p>
        <p>In-person coaching solves that, but only for the clients who can reach you.</p>
      </div>
      <p class="pull">Aura Arbor gives you the depth of a room and the reach of a video call.</p>
    </div>
  </div>
</section>

<section class="section band-mist" id="features">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What makes it different</span>
      <h2>Presence you can feel. Depth you can't fake.</h2>
    </div>
    <div class="cards">
      <article class="card">
        {img("feature-space.webp", "A quiet studio space lit by a single glowing orb")}
        <div class="card-body">
          <span class="card-tag">The space</span>
          <h3>A space that shapes the work</h3>
          <p>A calm studio for structured dialogue. A forest for grounding and emotional work. A view of the stars when someone is stuck inside an immediate concern and needs distance. Inside the headset there's no inbox and no second screen. The environment is part of the intervention.</p>
          <a class="link-arrow" href="environments.html">Explore the environments <span aria-hidden="true">→</span></a>
        </div>
      </article>
      <article class="card">
        {img("feature-tools.webp", "A translucent board mapping a path from current state to desired outcome")}
        <div class="card-body">
          <span class="card-tag">The tools</span>
          <h3>Think with your hands, not just your words</h3>
          <p>A shared whiteboard for mapping themes. Objects your client can place, move and work with: a bridge, a backpack, a door. Set two of them at whatever distance feels true, then move one and watch what shifts.</p>
          <a class="link-arrow" href="coaching-tools.html">See the coaching tools <span aria-hidden="true">→</span></a>
        </div>
      </article>
      <article class="card">
        {img("feature-presence.webp", "Two avatars meeting in a calm virtual room")}
        <div class="card-body">
          <span class="card-tag">The presence</span>
          <h3>A different kind of presence</h3>
          <p>Meeting as avatars shifts something in the dynamic. Without the intensity of face-to-face scrutiny, many clients feel freer to speak openly and get to what matters sooner. The connection is real. It simply works differently than it does on a screen.</p>
          <a class="link-arrow" href="#voices">How VR changes coaching <span aria-hidden="true">→</span></a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section" id="voices">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Social proof</span>
      <h2>Coaches who've been inside.</h2>
    </div>
    <div class="voices-grid">
        {quotes_html()}
    </div>
    <p class="voices-note">Aura Arbor has been shaped in testing with professional and agile coaches across Europe. Their feedback drives what we build next.</p>
  </div>
</section>

<section class="band-forest" id="how">
  <div class="how-grid">
    <div class="how-copy">
      <span class="eyebrow light">How it works</span>
      <h2>Four steps from booking to breakthrough.</h2>
      <ol class="steps">
        <li><div><strong>Create your session</strong><span>Set it up in seconds and invite up to two clients. No software install for them to figure out alone.</span></div></li>
        <li><div><strong>Share the session code</strong><span>Each client gets a unique code and joins directly. That's the whole handoff.</span></div></li>
        <li><div><strong>Meet in the space you chose</strong><span>Studio, forest, abstract space or cosmic room: whatever the session calls for.</span></div></li>
        <li><div><strong>Guide with tools and objects</strong><span>Whiteboard, objects and the room itself become part of how you work.</span></div></li>
      </ol>
      <div><a class="btn" href="#beta">Apply as a beta tester</a></div>
    </div>
    {img("how-it-works.webp", "A coach wearing a headset inside a holographic studio")}
  </div>
</section>

<section class="section band-mist">
  <div class="wrap statement-grid">
    <div class="statement light">
      <span class="eyebrow">Why now</span>
      <h2>Immersive coaching isn't a someday technology.</h2>
      <div class="prose">
        <p>Headsets have become lighter, cheaper and comfortable to wear for the length of a real session. A generation of clients has grown up at home in digital spaces. And coaching itself has largely moved online, so the question is no longer whether you coach through a screen, but how much the screen costs you.</p>
        <p>We built Aura Arbor for coaches who'd rather shape what comes next than adapt to it later.</p>
      </div>
      <p class="closing">Built in VR today. Designed for the immersive devices of tomorrow.</p>
    </div>
    <div class="statement light">
      <span class="eyebrow">Who we are</span>
      <h2>Swiss-built. Coach-shaped.</h2>
      <div class="prose">
        <p>Aura Arbor is developed in Lucerne, Switzerland, by VRFX Realtime Studio, a team that has been building professional real-time and VR experiences for years.</p>
        <p>The coaching methodology behind the product comes from working coaches, not from a product roadmap. Every environment, object and tool has been tested in real sessions with real clients, and refined based on what came back.</p>
      </div>
      <p class="swiss">{SWISS}Developed in Lucerne by VRFX Realtime Studio GmbH</p>
    </div>
  </div>
</section>

{BETA_FORM}'''

ENVS = [
    ("env-studio.webp", "The Studio", "A clean, modern interior built for clarity and structure. Soft light, natural materials and quiet visual anchors.",
     ["Focused dialogue", "Goal-setting", "Structured reflection", "First sessions"],
     "A familiar professional setting helps a client settle in their first session."),
    ("env-abstract.webp", "The Abstract Space", "A contemporary architectural environment with reduced visual noise and gentle accents, free from the associations a real room carries.",
     ["Creative thinking", "Systems mapping", "Patterns and mental models"], ""),
    ("env-cosmic.webp", "The Cosmic Room", "A calm, expansive space against a quiet field of stars. Especially useful when a client is caught inside an immediate concern and needs to see it from further out.",
     ["Perspective work", "Emotional distance", "Big-picture thinking"], ""),
    ("env-forest.webp", "The Forest Sanctuary", "A natural, grounding environment inspired by real woodland. Soft light, organic texture, natural depth.",
     ["Emotional work", "Embodiment", "Regulation", "Closing intensive sessions"], ""),
]


def env_html():
    out = []
    for file, name, text, best, extra in ENVS:
        chips = "".join(f"<li>{b}</li>" for b in best)
        extra_p = f"<p>{extra}</p>" if extra else ""
        out.append(f'''<article class="env">
        {img(file, f"{name} environment in Aura Arbor")}
        <div class="env-copy">
          <h2>{name}</h2>
          <p>{text}</p>{extra_p}
          <p class="best-label">Best for</p>
          <ul class="best">{chips}</ul>
        </div>
      </article>''')
    return "\n      ".join(out)


ENVIRONMENTS = f'''{page_hero("Environments", "The room is part of the method.", "Where a conversation happens changes what becomes sayable. Four environments, each built for a different kind of work.", "hero-environments.webp", "")}

<section class="section-tight">
  <div class="wrap narrow">
    <p class="lead">In a physical practice you can't change the room to suit the session. Here you can. Move a stuck client from a structured studio into open space and watch the problem change shape. Bring someone doing hard emotional work into a forest instead of a boardroom. The environment is a lever you can pull.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap env-list">
      {env_html()}
  </div>
</section>

<section class="section band-mist">
  <div class="wrap narrow statement light">
    <span class="eyebrow">In every space</span>
    <h2>What stays the same.</h2>
    <p class="lead">Distraction falls away. Attention settles into the conversation. The shared sense of being somewhere together builds trust faster than a video window does, and gives you room to work with presence, silence and pace the way you would in person.</p>
  </div>
</section>

{cta_band()}'''

TOOLS = f'''{page_hero("Coaching tools", "Shape the conversation.", "Structure ideas, capture insight and guide the session without ever breaking immersion.", "hero-tools.webp", "")}

<section class="section-tight">
  <div class="wrap narrow">
    <p class="lead">Coaching conversations rarely move in straight lines. A client circles a theme three times before naming it. Something said in minute six turns out to matter in minute forty. Aura Arbor gives you tools to hold that complexity visibly, inside the session, without reaching for a notepad or dropping out of the space.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split">
    {img("tools-whiteboard.webp", "The shared whiteboard inside an Aura Arbor session")}
    <div class="prose">
      <span class="eyebrow">The shared whiteboard</span>
      <h2>Map themes as they emerge.</h2>
      <p>Sketch a system. Write the one word your client keeps returning to and leave it standing where you both can see it. You and your client work on it together in real time. It's a shared surface, not a coach's presentation screen.</p>
    </div>
  </div>
</section>

<section class="section band-forest">
  <div class="wrap narrow statement">
    <span class="eyebrow light">Why it works in VR</span>
    <h2>You turn toward it and keep talking.</h2>
    <p class="lead">On a video call, switching to a screen-share tool means everyone stops being present and starts operating software. Here the whiteboard is simply in the room with you.</p>
  </div>
</section>

{cta_band()}'''

OBJECTS = f'''{page_hero("Spatial objects", "Shift the perspective.", "Explore dynamics through embodied, symbolic interaction, the kind of work that's been out of reach online.", "hero-objects.webp", "")}

<section class="section">
  <div class="wrap split">
    <div class="prose">
      <span class="eyebrow">How it works</span>
      <h2>A bridge. A backpack. A door.</h2>
      <p>Objects that carry meaning without needing explanation, brought into the session so your client can work with them directly.</p>
      <p>Place the backpack down and ask what's in it. Position the door across the room and ask what's on the other side. Have a client set two objects at whatever distance feels true, then move one and notice what happens in their body when they do. Abstract feelings become things with location, weight and distance, visible to both of you.</p>
    </div>
    {img("objects.webp", "Glowing outlines of a door, a bridge and a backpack")}
  </div>
</section>

<section class="section band-mist">
  <div class="wrap statement-grid">
    <div class="statement light">
      <span class="eyebrow">Why this matters</span>
      <h2>The tools coaching lost online come back.</h2>
      <p class="lead">Constellation work, embodiment and metaphor have always been among coaching's most powerful tools, and among the first casualties of moving online. In a virtual space they come back, with a flexibility that even a physical room can't offer.</p>
    </div>
    <div class="note" style="align-self:center">
      <h3>A note on method</h3>
      <p>Objects support the client's own imagery. They're offered, never imposed. If a client's internal metaphor doesn't match what's on the shelf, the metaphor wins.</p>
    </div>
  </div>
</section>

{cta_band()}'''

FAQS = [
    ("What equipment do I need?", "A standalone VR headset for you, and one for each participating client. No PC, cables or external sensors required. If you're testing the waters, headsets can be rented affordably for a single session."),
    ("Do my clients need to know VR?", "No. Most first-time users find their way without a guide. Clients join with a session code. That's the entire technical requirement on their side."),
    ("How long does setup take?", "Creating a session takes seconds. For a client's first time, plan a short orientation at the start so they can get comfortable in the space before the coaching begins."),
    ("Does it work for online and hybrid practices?", "Yes. Aura Arbor is built for coaches working with clients anywhere. If you can currently coach someone on a video call, you can coach them here."),
    ("Is it suitable for corporate and executive coaching?", "Yes. Coaches use it for leadership development, career and role transitions, team dynamics and conflict work, as well as personal development."),
    ("What about confidentiality?", "Sessions are private between coach and invited clients. Nothing is recorded unless you choose to. Full details are in our privacy policy."),
    ("How long should a session be?", "Coaches in testing generally find 30 to 45 minutes works well for a full VR session, often shorter than a video call while covering as much ground."),
    ("Can I take notes during a session?", "This is one of the most frequent requests from coaches, and it's actively in development. We're building for the coach who doesn't want to remove the headset mid-session."),
    ("What does it cost?", "Early access is free. We'll share pricing with early access members well before anything changes, and you'll have input into how it's structured."),
    ("How do I get started?", "Join the early access list. We onboard coaches personally, so you'll speak with a real person, not a sequence of automated emails."),
]
faq_items = "\n      ".join(
    f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>'
    for i, (q, a) in enumerate(FAQS))
FAQ_LD = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}, ensure_ascii=False)

FAQ = f'''<section class="hero-plain">
  <div class="wrap hero-inner">
    <div class="hero-copy" style="max-width:640px">
      <span class="eyebrow light">FAQ</span>
      <h1>Questions before you step in.</h1>
      <p style="color:rgba(255,255,255,.8);font-size:var(--step-1)">Equipment, setup, session length, confidentiality and cost. The practical questions coaches ask before their first immersive session.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="faq">
      {faq_items}
    </div>
    <p style="margin-top:32px;color:var(--ink-2)">Still have a question? Write to us at <a href="mailto:hello@auraarbor.com" style="color:var(--teal)">hello@auraarbor.com</a>.</p>
  </div>
</section>

{cta_band()}'''


def legal(h1, sections, note):
    secs = "\n    ".join(f'<section><h2>{h}</h2><p class="todo">{t}</p></section>' for h, t in sections)
    return f'''<section class="hero-plain">
  <div class="wrap hero-inner"><div class="hero-copy"><span class="eyebrow light">Legal</span><h1>{h1}</h1></div></div>
</section>
<section class="section">
  <div class="wrap legal">
    <p class="todo">{note}</p>
    {secs}
  </div>
</section>'''


MIGRATE = "Paste the current text from the HubSpot page here before going live."
IMPRINT = legal("Imprint", [
    ("Contact", "Aura Arbor, c/o Berger Digital Partners, Quaistrasse 53, 4632 Trimbach, Switzerland · hello@auraarbor.com. " + MIGRATE),
    ("Disclaimer", MIGRATE), ("External links", MIGRATE), ("Intellectual property", MIGRATE)],
    "Content to migrate: the legal text from auraarbor.com/imprint is not copied automatically.")
PRIVACY = legal("Privacy Policy", [
    ("1. General information", MIGRATE), ("2. Data processing in the app", MIGRATE),
    ("Website and early access form", "New section needed: the website now sends early access applications to HubSpot (Forms API) and loads fonts from Google Fonts. Describe this processing here."),
    ("3. Your rights", MIGRATE), ("4. Changes to this policy", MIGRATE)],
    "Content to migrate: the policy text from auraarbor.com/privacy-policy is not copied automatically.")

NOTFOUND = f'''<section class="hero-plain" style="min-height:70vh;display:flex;align-items:center">
  <div class="wrap hero-inner"><div class="hero-copy" style="max-width:560px">
    <span class="eyebrow light">404</span>
    <h1>This page took a different path.</h1>
    <p style="color:rgba(255,255,255,.8)">The page you're looking for doesn't exist or has moved.</p>
    <div class="hero-cta"><a class="btn" href="index.html">Back to the homepage</a></div>
  </div></div>
</section>'''

PAGES = [
    ("index", "Aura Arbor | Immersive Coaching for Professional Coaches",
     "Meet clients in a distraction-free virtual space built for coaching. Deeper presence, embodied tools, and real transformation, from anywhere.", HOME, None, ""),
    ("environments", "Coaching Environments | Aura Arbor",
     "Four immersive spaces built for different coaching work: a focused studio, an abstract space, a cosmic room for perspective, and a forest sanctuary.", ENVIRONMENTS, "environments.html", ""),
    ("coaching-tools", "Interactive Coaching Tools | Aura Arbor",
     "A shared whiteboard and session tools that let you structure ideas and capture insight without ever breaking immersion.", TOOLS, "coaching-tools.html", ""),
    ("spatial-objects", "Experiential Objects for Insight | Aura Arbor",
     "Bring symbolic objects into the session so clients can externalize experience, explore dynamics, and shift perspective through embodied interaction.", OBJECTS, "spatial-objects.html", ""),
    ("faq", "FAQ | Aura Arbor Immersive Coaching",
     "Equipment, setup, session length, confidentiality, and cost: the practical questions coaches ask before their first immersive session.", FAQ, "faq.html",
     f'<script type="application/ld+json">{FAQ_LD}</script>\n'),
    ("imprint", "Imprint | Aura Arbor", "Legal information about Aura Arbor, c/o Berger Digital Partners, Trimbach, Switzerland.", IMPRINT, None, '<meta name="robots" content="noindex">\n'),
    ("privacy-policy", "Privacy Policy | Aura Arbor", "How Aura Arbor processes personal data in the app and on this website.", PRIVACY, None, ""),
    ("404", "Page not found | Aura Arbor", "This page doesn't exist or has moved. Head back to the Aura Arbor homepage.", NOTFOUND, None, '<meta name="robots" content="noindex">\n'),
]

def render():
    """All generated files as {relative path: content}. Used by build and by tools/check.py."""
    files = {f"{slug}.html": layout(slug, title, desc, body, active, head)
             for slug, title, desc, body, active, head in PAGES}
    urls = "".join(f"  <url><loc>{SITE}/{'' if s == 'index' else s}</loc></url>\n"
                   for s, *_ in PAGES if s not in ("404", "imprint"))
    files["sitemap.xml"] = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    files["robots.txt"] = f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n"
    return files


if __name__ == "__main__":
    for name, content in render().items():
        (OUT / name).write_text(content, encoding="utf-8")
    print("Built", len(PAGES), "pages into site/")
