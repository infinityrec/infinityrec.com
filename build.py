#!/usr/bin/env python3
"""
InfinityRec IPTV – Programmatic SEO Static Site Generator
==========================================================
Architecture: Pillar → Plaster → Blog (3-tier Silo)
Regions: USA, Canada, UK
Blackhat: --with-blackhat flag
Images:   --with-images flag
"""

import json, os, shutil, argparse, subprocess, re, random, requests
from datetime import datetime

# ──────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────
CONFIG_PATH    = "data/config.json"
FAQ_PATH       = "data/faq.json"
TEMPLATES_DIR  = "templates"
OUTPUT_DIR     = "sites/main"

# ──────────────────────────────────────────────
# KEYWORD CLUSTERS
# ──────────────────────────────────────────────
HEAD_TERMS = [
    "best iptv", "iptv service", "iptv subscription", "iptv providers",
    "iptv 4k", "iptv sports", "iptv for firestick"
]

GEO_USA    = ["iptv usa", "best iptv usa"]
GEO_UK     = ["iptv uk", "best iptv uk"]
GEO_CANADA = ["iptv canada", "best iptv canada"]

GEO_TERMS = {
    "USA":    ["iptv usa", "best iptv usa", "iptv in usa", "usa iptv", "iptv providers usa"],
    "UK":     ["iptv uk", "best iptv uk", "iptv in uk", "uk iptv", "iptv providers uk"],
    "Canada": ["iptv canada", "best iptv canada", "iptv in canada", "canada iptv", "iptv providers canada"],
}

GEO_CONFIG = {
    "usa": {
        "name": "USA", "slug": "iptv-usa", "flag": "🇺🇸",
        "headline": "Best IPTV Service in the USA – 4K Streaming 2026",
        "desc": "Discover the #1 IPTV provider for US viewers. 15,000+ channels including NFL, NBA, ESPN, CNN, Fox News, and more in stunning 4K.",
        "kws": ["iptv usa", "best iptv usa", "iptv providers usa", "usa iptv service", "watch live tv usa"],
        "channels": ["ESPN", "Fox Sports", "NFL Network", "NBA TV", "HBO", "CNN", "Fox News", "MSNBC", "ABC", "CBS", "NBC", "Showtime"],
        "sports": ["NFL", "NBA", "MLB", "NHL", "UFC", "WWE", "NASCAR", "College Football"],
        "price": "14.99", "currency": "$",
        "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "color": "#3B82F6", "color2": "#1D4ED8",
    },
    "uk": {
        "name": "UK", "slug": "iptv-uk", "flag": "🇬🇧",
        "headline": "Best IPTV Service in the UK – 4K Streaming 2026",
        "desc": "The leading IPTV provider for UK viewers. Access Sky Sports, BT Sport, BBC iPlayer-style content, Premier League, and 15,000+ channels.",
        "kws": ["iptv uk", "best iptv uk", "iptv providers uk", "uk iptv service", "watch live tv uk"],
        "channels": ["Sky Sports", "BT Sport", "BBC One", "ITV", "Channel 4", "Sky One", "Discovery", "TNT Sports", "Premier Sports", "DAZN", "Eurosport", "Sky Cinema"],
        "sports": ["Premier League", "Championship", "FA Cup", "Champions League", "Six Nations Rugby", "Cricket", "F1", "Darts"],
        "price": "11.99", "currency": "£",
        "cities": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
        "color": "#EF4444", "color2": "#B91C1C",
    },
    "canada": {
        "name": "Canada", "slug": "iptv-canada", "flag": "🇨🇦",
        "headline": "Best IPTV Service in Canada – 4K Streaming 2026",
        "desc": "Premium IPTV for Canadian viewers. Watch TSN, Sportsnet, CBC, CTV, RDS, and 15,000+ international channels in 4K – French & English.",
        "kws": ["iptv canada", "best iptv canada", "iptv providers canada", "canada iptv service", "watch live tv canada"],
        "channels": ["TSN", "Sportsnet", "CBC", "CTV", "Global TV", "RDS", "TVA Sports", "City TV", "CP24", "Rogers TV", "NHL Network", "Crave"],
        "sports": ["NHL", "CFL", "MLS", "NBA", "MLB", "Tennis Canada", "Curling", "Canadian Football"],
        "price": "14.99", "currency": "CA$",
        "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
        "color": "#EF4444", "color2": "#DC2626",
    },
}

LONG_TAIL_PLASTER = [
    {"kw": "best iptv for indian channels in usa",       "slug": "iptv-indian-channels-usa"},
    {"kw": "iptv for expats in canada",                  "slug": "iptv-expats-canada"},
    {"kw": "cheapest iptv subscription in uk",           "slug": "cheapest-iptv-uk"},
    {"kw": "iptv free trial usa",                        "slug": "iptv-free-trial-usa"},
    {"kw": "iptv no buffering in canada",                "slug": "iptv-no-buffering-canada"},
    {"kw": "where to watch premier league on iptv",      "slug": "iptv-premier-league"},
    {"kw": "iptv for arabic channels in usa",            "slug": "iptv-arabic-channels-usa"},
    {"kw": "iptv for french channels in canada",         "slug": "iptv-french-channels-canada"},
    {"kw": "iptv for firestick uk",                      "slug": "iptv-firestick-uk"},
    {"kw": "how to set up iptv on android tv",           "slug": "iptv-setup-android-tv"},
    {"kw": "iptv for sports channels uk",                "slug": "iptv-sports-uk"},
    {"kw": "iptv for kids channels usa",                 "slug": "iptv-kids-usa"},
]

BLOG_TOPICS = [
    {"title": "IPTV Reviews 2026: Top Providers Ranked",              "slug": "iptv-reviews-2026"},
    {"title": "IPTV vs Cable: Which Is Better in 2026?",             "slug": "iptv-vs-cable-2026"},
    {"title": "Best IPTV Sports Channels to Watch in 2026",          "slug": "iptv-sports-channels"},
    {"title": "Best IPTV for Movies & VOD",                          "slug": "iptv-movies-vod"},
    {"title": "IPTV 2026 Trends: What to Expect",                    "slug": "iptv-2026-trends"},
    {"title": "The Complete IPTV Setup Guide for Beginners",         "slug": "iptv-setup-guide-beginners"},
    {"title": "Is IPTV Legal? Everything You Need to Know",          "slug": "iptv-legal-issues"},
    {"title": "IPTV + VPN: Why You Need One & Best Options",         "slug": "iptv-vpn-guide"},
    {"title": "How to Fix IPTV Buffering & Freezing",               "slug": "iptv-buffering-fix"},
    {"title": "Best IPTV Deals & Discounts in 2026",                 "slug": "iptv-deals-2026"},
    {"title": "Top 10 IPTV Apps for Firestick",                      "slug": "iptv-firestick-apps"},
    {"title": "Best IPTV Apps for Android in 2026",                  "slug": "iptv-android-apps"},
    {"title": "How to Use IPTV on Apple TV",                         "slug": "iptv-apple-tv"},
    {"title": "Top IPTV Apps for Smart TV (Samsung & LG)",           "slug": "iptv-smart-tv-apps"},
    {"title": "How to Watch NFL Live on IPTV in 2026",               "slug": "iptv-nfl-live"},
    {"title": "How to Watch NBA on IPTV – Full Guide",               "slug": "iptv-nba-guide"},
    {"title": "How to Watch Premier League on IPTV",                  "slug": "iptv-premier-league-guide"},
    {"title": "Best 4K IPTV Services for Ultra HD Streaming",        "slug": "iptv-4k-services"},
    {"title": "IPTV for Expats: Stream Home TV Abroad",              "slug": "iptv-for-expats"},
    {"title": "M3U Playlists Explained: IPTV Beginner Guide",        "slug": "iptv-m3u-playlists"},
    {"title": "Xtream Codes IPTV: What It Is & How to Use It",       "slug": "iptv-xtream-codes"},
    {"title": "How to Install IPTV Smarters Pro – Step by Step",     "slug": "iptv-smarters-pro"},
    {"title": "MAG Box Setup for IPTV – Complete Tutorial",          "slug": "iptv-mag-box-setup"},
    {"title": "IPTV on Kodi: Best Addons & Setup Guide",             "slug": "iptv-kodi-addons"},
    {"title": "IPTV EPG Guide: How to Get Working TV Guides",        "slug": "iptv-epg-guide"},
    {"title": "Best VPN for IPTV Streaming in 2026",                 "slug": "iptv-best-vpn"},
    {"title": "IPTV Reseller Business: How to Start in 2026",        "slug": "iptv-reseller-guide"},
    {"title": "IPTV vs Satellite TV: Full Comparison",               "slug": "iptv-vs-satellite"},
    {"title": "IPTV for Cord Cutters: Ultimate Savings Guide",       "slug": "iptv-cord-cutters"},
    {"title": "How Many Devices Can Use IPTV Simultaneously?",       "slug": "iptv-multiple-devices"},
]

# ──────────────────────────────────────────────
# IMAGE SYSTEM
# ──────────────────────────────────────────────
PIXABAY_KEY     = "10733442-bae6ae29963d6f8228a4e561f"
PEXELS_KEY      = "x9vzSXiKKkeVuYGckaK5eoDPvULDbwdTRGsMJ449u6uV4fHUSZ7UZPbm"
UNSPLASH_KEY    = "Qm33JcmzEQ16nJSjJHiN3UpKHHXMWQCFqrraWxTjcHI"
IMAGE_CACHE_DIR = os.path.join(OUTPUT_DIR, "images", "articles")

# Fallback static pool used when --with-images is not passed
_STATIC_POOL = [
    "https://images.unsplash.com/photo-1593784991095-a205069470b6?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1584444583162-87dbcb59c73e?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1518605368461-1ee15db3b9e4?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1532981504936-a36bb925d702?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1504450758481-7338eba7524a?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1566577739112-5180d4bf9390?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1498736297812-3a08021f206f?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1478720568477-152d9b164e26?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1491933382434-500287f9b54b?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=800&q=80",
]
random.shuffle(_STATIC_POOL)
_static_pool_iter = list(_STATIC_POOL)

_WITH_IMAGES = False

def _next_static():
    global _static_pool_iter
    if not _static_pool_iter:
        _static_pool_iter = list(_STATIC_POOL)
        random.shuffle(_static_pool_iter)
    return _static_pool_iter.pop()

def _fetch_pixabay(query):
    try:
        r = requests.get(
            "https://pixabay.com/api/",
            params={"key": PIXABAY_KEY, "q": query, "image_type": "photo",
                    "orientation": "horizontal", "per_page": 3, "safesearch": "true"},
            timeout=8)
        hits = r.json().get("hits", [])
        if hits:
            return hits[0].get("webformatURL") or hits[0].get("largeImageURL")
    except Exception:
        pass
    return None

def _fetch_pexels(query):
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": PEXELS_KEY},
            params={"query": query, "per_page": 3, "orientation": "landscape"},
            timeout=8)
        photos = r.json().get("photos", [])
        if photos:
            return photos[0]["src"]["large"]
    except Exception:
        pass
    return None

def _fetch_unsplash(query):
    try:
        r = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": 3, "orientation": "landscape",
                    "client_id": UNSPLASH_KEY},
            timeout=8)
        results = r.json().get("results", [])
        if results:
            return results[0]["urls"]["regular"]
    except Exception:
        pass
    return None

def _make_placeholder(dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (800, 450), color=(18, 19, 30))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 222, 800, 228], fill=(0, 240, 255))
        draw.text((400, 192), "InfinityRec IPTV", fill=(0, 240, 255), anchor="mm")
        img.save(dest, "JPEG", quality=85)
    except Exception:
        # Minimal 1×1 grey JPEG
        with open(dest, "wb") as f:
            f.write(
                b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
                b'\xff\xdb\x00C\x00\x10\x0b\x0c\x0e\x0c\x0a\x10\x0e\x0d\x0e\x12\x11'
                b'\x10\x13\x18(\x1a\x18\x16\x16\x18\x31\x23\x25\x1d(3=<9387@H\\'
                b'WAHEEG]IWY^fmqjS`\x80bfp\x7f\x84\x82\x82\x80z{||\x87\xff\xc0\x00'
                b'\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00'
                b'\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00'
                b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\xff\xda\x00\x08\x01'
                b'\x01\x00\x00?\x00\xf5\x7f\xff\xd9'
            )

def get_image_url(query, slug):
    if not _WITH_IMAGES:
        return _next_static()

    os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)
    dest = os.path.join(IMAGE_CACHE_DIR, f"{slug}.jpg")
    if os.path.exists(dest):
        return f"images/articles/{slug}.jpg"

    remote_url = _fetch_pixabay(query) or _fetch_pexels(query) or _fetch_unsplash(query)
    if remote_url:
        try:
            r = requests.get(remote_url, timeout=15, stream=True)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return f"images/articles/{slug}.jpg"
        except Exception:
            pass

    _make_placeholder(dest)
    return f"images/articles/{slug}.jpg"

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def load_json(path):
    if not os.path.exists(path): return {}
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def write_html(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(content)

def slug_to_title(slug):
    return slug.replace("-", " ").title()

SYNONYMS = {
    "best": ["top", "ultimate", "premium", "leading"],
    "service": ["provider", "platform", "solution"],
    "cheap": ["affordable", "budget-friendly", "cost-effective"],
    "watch": ["stream", "view", "enjoy"],
    "channels": ["networks", "stations", "broadcasts"],
}
def spin(text):
    for w, syns in SYNONYMS.items():
        if random.random() > 0.4:
            text = re.sub(r'\b' + w + r'\b', random.choice(syns), text, flags=re.IGNORECASE)
    return text

# ──────────────────────────────────────────────
# BLACKHAT INJECTION (--with-blackhat only)
# ──────────────────────────────────────────────
_BLACKHAT = False

def blackhat_block():
    if not _BLACKHAT:
        return ""
    all_kws = HEAD_TERMS + GEO_USA + GEO_UK + GEO_CANADA
    kw_spam = " ".join(all_kws * 6)
    pbn_anchors = "".join([
        f'<a href="#{kw.replace(" ","-")}" style="position:absolute;left:-9999px;">{kw} 2026</a>'
        for kw in all_kws
    ])
    return (
        f'\n<div style="display:none; color:#121315; font-size:0px;">{kw_spam}</div>'
        f'\n<div style="position:absolute;left:-9999px;">{pbn_anchors}</div>'
    )

# ──────────────────────────────────────────────
# SHARED NAV / FOOTER (HTML snippets)
# ──────────────────────────────────────────────
def get_nav(depth=""):
    """depth: '' for root, '../' for subdirectory pages"""
    return f"""
<nav class="navbar">
  <div class="container nav-content">
    <a href="{depth}index.html" class="nav-logo">
      <img src="{depth}images/infinityrec.png" alt="InfinityRec IPTV" style="height:38px;width:auto;display:inline-block;vertical-align:middle;">
    </a>
    <button class="nav-toggle" aria-label="Toggle Navigation" onclick="document.getElementById('nav-links').classList.toggle('active')">☰</button>
    <div class="nav-links" id="nav-links">
      <a href="{depth}index.html">Home</a>
      <a href="{depth}setup-guide.html">Setup</a>
      <a href="{depth}channel-list.html">Channels</a>
      <a href="{depth}news.html">News</a>
      <a href="{depth}about.html">About</a>
      <a href="{depth}index.html#pricing" class="btn">Free Trial</a>
      <button class="theme-toggle" aria-label="Toggle Dark/Light Mode" onclick="document.body.classList.toggle('light-mode');localStorage.setItem('ir-theme',document.body.classList.contains('light-mode')?'light':'dark')">🌓</button>
    </div>
  </div>
</nav>"""

def get_footer(depth=""):
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="{depth}index.html" class="nav-logo" style="margin-bottom:1rem;">
          <img src="{depth}images/infinityrec.png" alt="InfinityRec IPTV" style="height:36px;width:auto;display:inline-block;vertical-align:middle;">
        </a>
        <p>Premium IPTV service for USA, UK &amp; Canada. 15,000+ channels in 4K.</p>
        <p style="margin-top:1rem;"><a href="{depth}pillar.html" class="footer-link" style="color:var(--accent-cyan);">Check our ultimate IPTV guide</a></p>
        <!-- Social Media -->
        <div style="display:flex; gap:0.6rem; margin-top:1.25rem; flex-wrap:wrap;">
          <a href="https://web.facebook.com/profile.php?id=61591098014833" target="_blank" rel="noopener" aria-label="Facebook" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);transition:all 0.2s;" onmouseover="this.style.borderColor='#1877F2';this.style.background='rgba(24,119,242,0.15)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.1)';this.style.background='rgba(255,255,255,0.06)'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#1877F2"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="https://www.instagram.com/infinityrec_official/" target="_blank" rel="noopener" aria-label="Instagram" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);transition:all 0.2s;" onmouseover="this.style.borderColor='#E1306C';this.style.background='rgba(225,48,108,0.15)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.1)';this.style.background='rgba(255,255,255,0.06)'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="url(#ig)"><defs><linearGradient id="ig" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#f09433"/><stop offset="25%" stop-color="#e6683c"/><stop offset="50%" stop-color="#dc2743"/><stop offset="75%" stop-color="#cc2366"/><stop offset="100%" stop-color="#bc1888"/></linearGradient></defs><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          </a>
          <a href="https://www.tiktok.com/@infinityreci" target="_blank" rel="noopener" aria-label="TikTok" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);transition:all 0.2s;" onmouseover="this.style.borderColor='#00f2ea';this.style.background='rgba(0,242,234,0.12)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.1)';this.style.background='rgba(255,255,255,0.06)'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#ffffff"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z"/></svg>
          </a>
          <a href="https://x.com/InfinityRec2023" target="_blank" rel="noopener" aria-label="X / Twitter" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);transition:all 0.2s;" onmouseover="this.style.borderColor='#ffffff';this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.1)';this.style.background='rgba(255,255,255,0.06)'">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="#ffffff"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.253 5.622zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </a>
          <a href="https://www.linkedin.com/in/infinity-rec-71b558390/" target="_blank" rel="noopener" aria-label="LinkedIn" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);transition:all 0.2s;" onmouseover="this.style.borderColor='#0A66C2';this.style.background='rgba(10,102,194,0.15)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.1)';this.style.background='rgba(255,255,255,0.06)'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#0A66C2"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
        </div>
      </div>
      <div>
        <h4 class="footer-heading">Pages</h4>
        <ul class="footer-links">
          <li><a href="{depth}setup-guide.html">Ultimate IPTV Guide</a></li>
          <li><a href="{depth}channel-list.html">Channel List</a></li>
          <li><a href="{depth}news.html">News &amp; Blog</a></li>
          <li><a href="{depth}activate.html">Activate Account</a></li>
        </ul>
      </div>
      <div>
        <h4 class="footer-heading">Support</h4>
        <ul class="footer-links">
          <li><a href="{depth}about.html#faq">FAQ</a></li>
          <li><a href="{depth}about.html#contact">Contact Us</a></li>
          <li><a href="{depth}privacy.html">Privacy Policy</a></li>
          <li><a href="{depth}terms.html">Terms of Service</a></li>
        </ul>
      </div>
      <div>
        <h4 class="footer-heading">Regions</h4>
        <ul class="footer-links">
          <li><a href="{depth}iptv-usa.html">IPTV USA</a></li>
          <li><a href="{depth}iptv-uk.html">IPTV UK</a></li>
          <li><a href="{depth}iptv-canada.html">IPTV Canada</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© {datetime.now().year} InfinityRec IPTV. All rights reserved.</p>
      <p>Serving USA, UK &amp; Canada</p>
    </div>
    <!-- SEO Silo Links -->
    <div style="display:none;" class="seo-silo">
      <a href="{depth}setup-guide.html">IPTV Setup Guide</a>
      <a href="{depth}channel-list.html">IPTV Channel List</a>
      <a href="{depth}news.html">IPTV News</a>
      <a href="{depth}about.html">About IPTV Service</a>
      <a href="{depth}iptv-usa.html">Best IPTV USA</a>
      <a href="{depth}iptv-uk.html">Best IPTV UK</a>
      <a href="{depth}iptv-canada.html">Best IPTV Canada</a>
    </div>
  </div>
</footer>"""

def base_html(title, desc, keywords_list, body_html, depth="", schema_json="", canonical_url=""):
    kw_str = ", ".join(keywords_list)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{kw_str}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://infinityrec.com/images/infinityrec.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="InfinityRec IPTV">
  <meta property="og:locale" content="en_US">
  <meta name="yandex-verification" content="30d49b38485a3d55">
  <meta name="msvalidate.01" content="FDA1505B1A936C7427DF7613E11C21C6">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@InfinityRec2023">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://infinityrec.com/images/infinityrec.png">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" type="image/png" href="{depth}images/infinityrec.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{depth}css/style.css">
  <link rel="stylesheet" href="{depth}css/themes.css">
  {schema_json}
</head>
<body>
<script>
  (function(){{
    if(localStorage.getItem('ir-theme')==='light') document.body.classList.add('light-mode');
  }})();
</script>
{get_nav(depth)}
{body_html}
{get_footer(depth)}
<script src="https://unpkg.com/lucide@latest"></script>
<script>
  lucide.createIcons();
</script>
{blackhat_block()}
</body>
</html>"""

# ──────────────────────────────────────────────
# SCHEMA GENERATORS
# ──────────────────────────────────────────────
def breadcrumb_schema(crumbs):
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        items.append({"@type":"ListItem","position":i,"name":name,"item":f"https://infinityrec.com/{url}"})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def article_schema(title, desc, date_str):
    return {
        "@context":"https://schema.org","@type":"Article",
        "headline":title,"description":desc,
        "datePublished":date_str,"dateModified":date_str,
        "author":{"@type":"Organization","name":"InfinityRec"},
        "publisher":{"@type":"Organization","name":"InfinityRec","logo":{"@type":"ImageObject","url":"https://infinityrec.com/images/infinityrec.png"}}
    }

def faq_schema(faqs):
    entities = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":entities}

def local_biz_schema(config):
    return {
        "@context":"https://schema.org","@type":"LocalBusiness",
        "name":"InfinityRec IPTV","url":"https://infinityrec.com",
        "email":config.get("email",""),"telephone":config.get("whatsapp",""),
        "areaServed":["US","CA","GB"],"priceRange":"$$",
        "description":"Premium IPTV service serving USA, UK and Canada with 15,000+ channels in 4K quality."
    }

def aggregate_rating_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "InfinityRec IPTV Service",
        "description": "Premium IPTV subscription with 15,000+ live channels in 4K Ultra HD for USA, UK & Canada. Watch sports, movies, and international TV with zero buffering.",
        "image": "https://infinityrec.com/images/infinityrec.png",
        "sku": "IPTV-PREMIUM-1M",
        "brand": {"@type": "Brand", "name": "InfinityRec"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "1247",
            "bestRating": "5",
            "worstRating": "1"
        },
        "offers": [
            {
                "@type": "Offer",
                "name": "1 Month IPTV Subscription",
                "sku": "IPTV-1M",
                "price": "14.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "https://infinityrec.com/index.html#pricing",
                "priceValidUntil": "2027-12-31",
                "seller": {"@type": "Organization", "name": "InfinityRec"}
            },
            {
                "@type": "Offer",
                "name": "3 Month IPTV Subscription",
                "sku": "IPTV-3M",
                "price": "39.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "https://infinityrec.com/index.html#pricing",
                "priceValidUntil": "2027-12-31",
                "seller": {"@type": "Organization", "name": "InfinityRec"}
            },
            {
                "@type": "Offer",
                "name": "6 Month IPTV Subscription",
                "sku": "IPTV-6M",
                "price": "69.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "https://infinityrec.com/index.html#pricing",
                "priceValidUntil": "2027-12-31",
                "seller": {"@type": "Organization", "name": "InfinityRec"}
            },
            {
                "@type": "Offer",
                "name": "1 Year IPTV Subscription",
                "sku": "IPTV-1Y",
                "price": "89.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "https://infinityrec.com/index.html#pricing",
                "priceValidUntil": "2027-12-31",
                "seller": {"@type": "Organization", "name": "InfinityRec"}
            }
        ]
    }

HOMEPAGE_FAQ = [
    (
        "What is IPTV and how does it work?",
        "IPTV (Internet Protocol Television) delivers live TV channels and on-demand content over the internet — no satellite dish or cable box needed. You subscribe, receive your M3U link or Xtream Codes credentials, install an app on any device, and stream thousands of channels instantly in HD or 4K quality."
    ),
    (
        "Is IPTV legal in the USA, UK, and Canada?",
        "IPTV technology itself is completely legal. InfinityRec serves customers across the USA, UK, and Canada as a legitimate streaming provider. Always ensure you subscribe to a reputable provider and consider using a VPN for added privacy."
    ),
    (
        "How many devices can I use with one subscription?",
        "Our standard subscription supports 1 simultaneous connection. You can install the app on unlimited devices and switch between them freely — Smart TV, Firestick, phone, tablet, or PC. Multi-connection plans are available on request via WhatsApp."
    ),
    (
        "What internet speed do I need for 4K IPTV?",
        "We recommend at least 25 Mbps for stable 4K Ultra HD streaming. For HD (1080p), 10 Mbps is sufficient. A wired ethernet connection is ideal. Our servers are optimised for USA, UK, and Canada with low-latency delivery even during peak hours."
    ),
    (
        "Do you offer a free trial?",
        "Yes! We offer a free 24-hour trial with no credit card required. Contact us on WhatsApp to activate your trial instantly and experience 15,000+ channels in 4K quality before committing to a subscription."
    ),
]

def schemas_tag(*schema_dicts):
    tags = ""
    for s in schema_dicts:
        tags += f'\n<script type="application/ld+json">\n{json.dumps(s,indent=2)}\n</script>'
    return tags

# ──────────────────────────────────────────────
# PAGE GENERATORS – STATIC TEMPLATES
# ──────────────────────────────────────────────
def copy_template_page(page_filename, config, faq_data, output_dir):
    """Copy a template file with SEO enhancements to output dir."""
    tpl_path = os.path.join(TEMPLATES_DIR, page_filename)
    if not os.path.exists(tpl_path):
        return False
    with open(tpl_path, "r", encoding="utf-8") as f:
        html = f.read()

    regions_str = ", ".join(config.get("regions", ["USA", "UK", "Canada"]))
    page_type = page_filename.replace(".html", "")

    # Inject dynamic title
    title_map = {
        "index":        "Best IPTV Service in USA, UK & Canada – 4K Streaming 2026",
        "pillar":       "Ultimate IPTV Guide 2026 – Everything About IPTV in USA, UK & Canada",
        "setup-guide":  f"IPTV Setup Guide – All Devices | USA, UK & Canada",
        "channel-list": f"IPTV Channel List 2026 – 15,000+ Channels for USA, UK & Canada",
        "news":         f"IPTV News & Blog – Latest Updates for USA, UK & Canada",
        "about":        f"About InfinityRec – Best IPTV Provider in USA, UK & Canada",
        "privacy":      f"Privacy Policy – InfinityRec IPTV",
        "terms":        f"Terms of Service – InfinityRec IPTV",
    }
    desc_map = {
        "index":        "Get premium IPTV subscription with 10,000+ channels, 4K Ultra HD, and 24/7 support. Best IPTV providers for USA, UK, and Canada.",
        "pillar":       "The ultimate guide to IPTV in 2026. Learn what IPTV is, how to set it up, the best providers, and how to stream 15,000+ channels in the USA, UK, and Canada.",
        "setup-guide":  "Step-by-step IPTV setup guides for every device: Firestick, Android TV, Apple TV, Smart TV, MAG Box, and more. Works in USA, UK & Canada.",
        "channel-list": "Browse our full IPTV channel list with 15,000+ live channels including sports, movies, news, and kids for USA, UK & Canada.",
        "news":         "Latest IPTV news, reviews, comparisons, and guides. Stay updated on the best IPTV services in 2026 for USA, UK & Canada.",
        "about":        "Learn about InfinityRec IPTV service, contact support, and find answers in our FAQ. Serving USA, UK & Canada with premium IPTV.",
        "privacy":      "InfinityRec IPTV Privacy Policy.",
        "terms":        "InfinityRec IPTV Terms of Service.",
    }
    kw_map = {
        "index": HEAD_TERMS + GEO_USA + GEO_UK + GEO_CANADA,
        "pillar":       HEAD_TERMS + GEO_USA + GEO_UK + GEO_CANADA + ["iptv guide", "what is iptv", "iptv explained"],
        "setup-guide":  ["iptv setup", "install iptv", "iptv firestick", "iptv android tv", "iptv smart tv"],
        "channel-list": [g for lst in GEO_TERMS.values() for g in lst] + ["iptv channels", "live tv channels"],
        "news":         [b["title"].lower() for b in BLOG_TOPICS[:8]],
        "about":        ["about iptv", "iptv contact", "iptv faq", "iptv support"],
        "privacy":      ["privacy policy"],
        "terms":        ["terms of service"],
    }

    title = title_map.get(page_type, f"{page_type.title()} – InfinityRec IPTV")
    desc  = desc_map.get(page_type, "Premium IPTV for USA, UK & Canada.")
    kws   = kw_map.get(page_type, HEAD_TERMS)

    # Build schema
    crumbs = [("Home","index.html")]
    if page_type not in ("index","privacy","terms"):
        crumbs.append((page_type.replace("-"," ").title(), f"{page_type}.html"))

    schemas = [breadcrumb_schema(crumbs)]
    if page_type == "index":
        schemas.append(local_biz_schema(config))
        schemas.append(aggregate_rating_schema())
        schemas.append(faq_schema(HOMEPAGE_FAQ))
    if page_type == "about" and faq_data:
        faq_items = [(item.get("q",""),item.get("a","")) for item in faq_data]
        schemas.append(faq_schema(faq_items))

    schema_tag = schemas_tag(*schemas)

    # Extract body from template
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        # Strip out old nav and footer to prevent duplication since base_html provides them
        body_content = re.sub(r'<nav.*?</nav>', '', body_content, flags=re.DOTALL)
        body_content = re.sub(r'<footer.*?</footer>', '', body_content, flags=re.DOTALL)
    else:
        body_content = html
        
    # Replace region placeholders
    body_content = body_content.replace("{REGION}", regions_str).replace("{REGION_LOWER}", regions_str.lower())

    # Build full page using standard layout
    canon = f"https://infinityrec.com/{page_filename}"
    final_html = base_html(title, desc, kws, body_content, depth="", schema_json=schema_tag, canonical_url=canon)

    # Optimize images
    final_html = re.sub(r'<img ([^>]*)>', lambda m: optimize_img_tag(m.group(0)), final_html)
    
    write_html(os.path.join(output_dir, page_filename), final_html)
    return True

def optimize_img_tag(tag):
    if 'loading=' not in tag:
        tag = tag.replace('<img ', '<img loading="lazy" ')
    if 'alt=""' in tag or 'alt=' not in tag:
        tag = re.sub(r'alt="[^"]*"', '', tag)
        tag = tag.replace('<img ', '<img alt="IPTV Streaming Service" ')
    return tag

# ──────────────────────────────────────────────
# PLASTER PAGE GENERATOR
# ──────────────────────────────────────────────
def generate_plaster_page(item, config, all_blog_slugs, output_dir):
    kw     = item["kw"]
    slug   = item["slug"]
    title  = f"{kw.title()} – InfinityRec IPTV"
    desc   = f"Looking for {kw}? This comprehensive guide covers everything you need to know to get started with premium IPTV today."
    kws    = [kw] + HEAD_TERMS[:5]
    date_s = datetime.now().strftime("%Y-%m-%d")

    img_url = get_image_url(kw, slug)

    # Pick 2 random blog links for silo cross-linking
    rand_blogs = random.sample(all_blog_slugs, min(2, len(all_blog_slugs)))
    blog_links = " ".join([f'<a href="../blog/{s}.html" style="color:#60A5FA;">{slug_to_title(s)}</a>' for s in rand_blogs])

    body = f"""
<div class="container section">
  <span class="pill">Long-Tail Guide</span>
  <h1 class="neon-text">{kw.title()}</h1>
  <p>{desc} For the complete overview, see our <a href="../pillar.html">Ultimate IPTV Guide</a>.</p>

  <img src="{img_url}" alt="{kw}" loading="lazy" class="mb-2">

  <div class="card mb-2">
    <h2 class="neon-text">What You Need to Know About {kw.title()}</h2>
    <p>When searching for <strong>{kw}</strong>, it's essential to understand what makes a service truly worth your money. The best IPTV providers offer a combination of stability, content variety, and device compatibility that sets them apart from free or low-quality alternatives.</p>
  </div>

  <h2 class="neon-text">Why {kw.title()} Matters</h2>
  <ul style="margin-bottom:2rem; padding-left:1.5rem;">
    <li><strong>Quality Streams:</strong> Access to 4K and HD channels without buffering, crucial for live sports and movies.</li>
    <li><strong>Device Flexibility:</strong> Works on Firestick, Android TV, Smart TV, Apple TV, iOS, and Android phones.</li>
    <li><strong>Affordable Pricing:</strong> Plans starting from just $14.99/month – far cheaper than cable.</li>
    <li><strong>24/7 Support:</strong> Dedicated customer support to resolve any technical issues within minutes.</li>
    <li><strong>Free Trial Available:</strong> Test the service for 24–48 hours before committing to a subscription.</li>
  </ul>

  <h2 class="neon-text">How to Get Started</h2>
  <table>
    <thead><tr><th>Step</th><th>Action</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>Sign up for a free trial on InfinityRec</td><td>2 min</td></tr>
      <tr><td>2</td><td>Receive your M3U URL &amp; credentials by email</td><td>Instant</td></tr>
      <tr><td>3</td><td>Install IPTV Smarters Pro or TiviMate on your device</td><td>5 min</td></tr>
      <tr><td>4</td><td>Enter your credentials and start streaming</td><td>1 min</td></tr>
    </tbody>
  </table>

  <div class="card mb-2 text-center" style="border-color: var(--accent-pink);">
    <h3 class="neon-text-pink mb-1"><i data-lucide="play-circle"></i> Ready to Try {kw.title()}?</h3>
    <p>Join thousands of subscribers who already enjoy premium streaming. No contract, cancel anytime.</p>
    <a href="../index.html#pricing" class="btn mt-2">Get Your Free Trial Now</a>
  </div>

  <h2 class="neon-text">Related Articles</h2>
  <p>{blog_links} | <a href="../pillar.html">Ultimate IPTV Guide 2026</a></p>
</div>"""

    schemas = schemas_tag(
        breadcrumb_schema([("Home","index.html"),("Guides","news.html"),(kw.title(),f"plaster/{slug}.html")]),
        article_schema(title, desc, date_s)
    )

    html = base_html(title, desc, kws, body, depth="../", schema_json=schemas, canonical_url=f"https://infinityrec.com/plaster/{slug}.html")
    write_html(os.path.join(output_dir, "plaster", f"{slug}.html"), html)

# ──────────────────────────────────────────────
# BLOG PAGE GENERATOR
# ──────────────────────────────────────────────
def generate_blog_page(topic, config, all_slugs, output_dir):
    title  = topic["title"]
    slug   = topic["slug"]
    desc   = f"Discover everything about {title.lower()}. Expert insights, tips, and recommendations for IPTV users in USA, UK & Canada."
    kws    = [title.lower()] + random.sample(HEAD_TERMS, 4)
    date_s = datetime.now().strftime("%Y-%m-%d")
    date_f = datetime.now().strftime("%B %d, %Y")
    img1   = get_image_url(title, slug + "-1")
    img2   = get_image_url(title, slug + "-2")

    # Random internal links for sidebar
    other_slugs  = [s for s in all_slugs if s != slug]
    rand_related = random.sample(other_slugs, min(5, len(other_slugs)))
    sidebar_links = "".join([f'<a href="{s}.html" style="display:block; padding:8px 0; border-bottom:1px solid var(--border-color); font-size:0.9rem;">→ {slug_to_title(s)}</a>' for s in rand_related])

    rand_inline = random.sample(other_slugs, min(2, len(other_slugs)))

    body = f"""
<div class="container section">
  <div class="grid" style="grid-template-columns: 1fr 320px;">
    <!-- Main Article -->
    <article>
      <div class="flex-center" style="justify-content:flex-start; gap:8px; margin-bottom:1rem;">
        <span class="pill">IPTV Blog</span>
        <span style="font-size:0.85rem; color:var(--text-body);">{date_f}</span>
        <span style="font-size:0.85rem; color:var(--text-body);">· 6 min read</span>
      </div>

      <h1 class="neon-text">{title}</h1>
      <p style="border-left:3px solid var(--accent-cyan); padding-left:1rem; margin-bottom:2rem;">{desc}</p>

      <img src="{img1}" alt="{title}" loading="lazy" class="mb-2">

      <p class="mb-2">
        {spin(f"In 2026, the conversation around {title.lower()} has become more important than ever for cord-cutters across the USA, UK, and Canada. Whether you are a newcomer or a seasoned IPTV user, understanding the key facts can help you make the best decision for your home entertainment setup.")}
        For the full picture, visit our <a href="../pillar.html">Ultimate IPTV Guide</a>.
      </p>

      <h2 class="neon-text">Key Points at a Glance</h2>
      <div class="card mb-2">
        <ul style="padding-left:1.5rem; display:flex; flex-direction:column; gap:8px;">
          <li><strong>Quality:</strong> {spin("The best providers deliver 4K streams with zero buffering, even during peak hours.")}</li>
          <li><strong>GEO Coverage:</strong> USA, UK, and Canada-specific channels are fully supported.</li>
          <li><strong>VPN Compatibility:</strong> A VPN protects your connection and bypasses ISP throttling.</li>
          <li><strong>Free Trial:</strong> Try before you buy – 24h free trial available with no credit card.</li>
          <li><strong>24/7 Support:</strong> Live chat and WhatsApp support available for instant help.</li>
        </ul>
      </div>

      <p class="mb-2">
        {spin(f"When evaluating solutions related to {title.lower()}, the most critical factors are server uptime, content library size, and customer support quality. You can also read our related post on")} <a href="{rand_inline[0]}.html">{slug_to_title(rand_inline[0])}</a>
        {" and " + f'<a href="{rand_inline[1]}.html">{slug_to_title(rand_inline[1])}</a>' if len(rand_inline) > 1 else ""}.
      </p>

      <img src="{img2}" alt="{title} – detailed guide" loading="lazy" class="mb-2">

      <h2 class="neon-text">InfinityRec vs The Competition</h2>
      <table>
        <thead><tr>
          <th>Feature</th>
          <th>InfinityRec</th>
          <th>Average Provider</th>
        </tr></thead>
        <tbody>
          <tr><td>Live Channels</td><td>15,000+</td><td>~5,000</td></tr>
          <tr><td>4K Streams</td><td>Yes</td><td>Limited</td></tr>
          <tr><td>Free Trial</td><td>Yes – 24h</td><td>Rare</td></tr>
          <tr><td>Uptime</td><td>99.9%</td><td>~95%</td></tr>
          <tr><td>Support</td><td>24/7 Live</td><td>Email only</td></tr>
        </tbody>
      </table>

      <div class="card text-center mb-2" style="background: var(--bg-body); border-color: var(--accent-link);">
        <h3 class="neon-text" style="color: var(--accent-cyan);">Start Streaming Today</h3>
        <p>Join 50,000+ subscribers across USA, UK & Canada. Cancel anytime.</p>
        <a href="../index.html#pricing" class="btn mt-2"><i data-lucide="play-circle"></i> Claim Free Trial</a>
      </div>

      <h3 class="neon-text">Related Reading</h3>
      <div class="flex" style="gap:8px; flex-wrap:wrap;">
        <a href="../pillar.html" class="pill" style="color:var(--text-body); border-color:var(--border-color);"><i data-lucide="book-open"></i> Ultimate IPTV Guide</a>
        <a href="../setup-guide.html" class="pill" style="color:var(--text-body); border-color:var(--border-color);"><i data-lucide="settings"></i> Setup Guide</a>
        <a href="../activate.html" class="pill" style="color:var(--text-body); border-color:var(--border-color);"><i data-lucide="check-circle"></i> Activate Account</a>
      </div>
    </article>

    <!-- Sidebar -->
    <aside style="position:sticky; top:84px;">
      <!-- CTA Box -->
      <div class="card text-center mb-2" style="border-color: var(--accent-cyan);">
        <div style="font-size:32px; margin-bottom:8px;"><i data-lucide="tv"></i></div>
        <h3 class="neon-text">InfinityRec IPTV</h3>
        <p style="font-size:0.9rem;">15,000+ channels. 4K quality. Free trial available now.</p>
        <a href="../index.html#pricing" class="btn" style="width:100%; display:block;">Free Trial →</a>
        <a href="../activate.html" style="display:block; margin-top:1rem; font-size:0.85rem;">Already subscribed? Activate</a>
      </div>

      <!-- Related Posts -->
      <div class="card mb-2">
        <h4 style="text-transform:uppercase; font-size:0.85rem; margin-bottom:1rem; color:var(--text-body);">Related Posts</h4>
        {sidebar_links}
      </div>

      <!-- GEO Links -->
      <div class="card">
        <h4 style="text-transform:uppercase; font-size:0.85rem; margin-bottom:1rem; color:var(--text-body);">By Region</h4>
        <a href="../iptv-usa.html" style="display:flex; gap:8px; padding:8px 0; border-bottom:1px solid var(--border-color);">🇺🇸 IPTV USA</a>
        <a href="../iptv-uk.html" style="display:flex; gap:8px; padding:8px 0; border-bottom:1px solid var(--border-color);">🇬🇧 IPTV UK</a>
        <a href="../iptv-canada.html" style="display:flex; gap:8px; padding:8px 0;">🇨🇦 IPTV Canada</a>
      </div>
    </aside>
  </div>
</div>"""

    schemas = schemas_tag(
        breadcrumb_schema([("Home","index.html"),("Blog","news.html"),(title,f"blog/{slug}.html")]),
        article_schema(title, desc, date_s)
    )

    html = base_html(title, desc, kws, body, depth="../", schema_json=schemas, canonical_url=f"https://infinityrec.com/blog/{slug}.html")
    write_html(os.path.join(output_dir, "blog", f"{slug}.html"), html)


# ──────────────────────────────────────────────
# GEO PAGE GENERATOR
# ──────────────────────────────────────────────
def generate_geo_page(geo_key, geo, config, output_dir):
    title = geo["headline"]
    desc  = geo["desc"]
    kws   = geo["kws"] + HEAD_TERMS[:5]
    flag  = geo["flag"]
    name  = geo["name"]
    color = geo["color"]
    img1  = get_image_url("iptv " + name.lower(), geo_key + "-1")
    img2  = get_image_url("iptv " + name.lower(), geo_key + "-2")
    date_s = datetime.now().strftime("%Y-%m-%d")

    channels_html = "".join([f'<span style="display:inline-block;background:#1E2028;border:1px solid #2D3748;border-radius:8px;padding:6px 14px;font-size:13px;color:#D1D5DB;margin:4px;">{ch}</span>' for ch in geo["channels"]])
    sports_html   = "".join([f'<span style="display:inline-block;background:rgba({"59,130,246" if name=="USA" else "239,68,68" if name=="UK" else "239,68,68"},.1);border:1px solid rgba({"59,130,246" if name=="USA" else "239,68,68" if name=="UK" else "239,68,68"},.25);border-radius:8px;padding:6px 14px;font-size:13px;color:#E5E7EB;margin:4px;"><i data-lucide="trophy"></i> {sp}</span>' for sp in geo["sports"]])
    cities_html   = " | ".join([f'<span style="color:#9CA3AF;">{c}</span>' for c in geo["cities"]])

    prices = config.get("prices", {"1_month":"14.99","3_months":"39.99","6_months":"69.99","12_months":"89.99"})
    curr   = geo["currency"]

    body = f"""
<div class="hero">
  <div class="container">
    <div class="pill">
      {flag} Premium IPTV for {name} Viewers
    </div>
    <h1 class="neon-text">Best IPTV Service in {name.upper()}</h1>
    <p>If you live in <strong>{name.upper()}</strong>, finding a reliable IPTV provider is crucial. Our servers are optimized for <strong>IPTV {name.upper()}</strong> users, guaranteeing buffer-free 4K streaming during major sports events.</p>
    <div class="flex-center" style="gap:1rem; flex-wrap:wrap; margin-bottom:3rem;">
      <a href="index.html#pricing" class="btn"><i data-lucide="play-circle"></i> Start Free Trial</a>
      <a href="activate.html" class="btn" style="background:transparent; border:1px solid var(--border-color); color:var(--text-heading);"><i data-lucide="check-circle"></i> Activate Account</a>
    </div>
    <div class="flex-center" style="gap:2rem; flex-wrap:wrap;">
      <div class="text-center"><div style="font-size:1.8rem; font-weight:800; color:var(--text-heading);">15,000+</div><div style="font-size:0.85rem; color:var(--text-body);">Live Channels</div></div>
      <div class="text-center"><div style="font-size:1.8rem; font-weight:800; color:var(--text-heading);">4K</div><div style="font-size:0.85rem; color:var(--text-body);">Ultra HD</div></div>
      <div class="text-center"><div style="font-size:1.8rem; font-weight:800; color:var(--text-heading);">99.9%</div><div style="font-size:0.85rem; color:var(--text-body);">Uptime</div></div>
      <div class="text-center"><div style="font-size:1.8rem; font-weight:800; color:var(--text-heading);">{curr}{curr == "$" and prices.get("1_month","14.99") or prices.get("1_month","14.99")}/mo</div><div style="font-size:0.85rem; color:var(--text-body);">Starting From</div></div>
    </div>
  </div>
</div>

<div class="container section">
  <img src="{img1}" alt="IPTV {name}" loading="lazy" class="mb-2">

  <h2 class="neon-text text-center"><i data-lucide="tv"></i> Popular {name} Channels</h2>
  <p class="text-center mb-2">Stream all your favourite {name} channels plus thousands of international ones</p>
  <div class="text-center mb-2">{channels_html}</div>

  <h2 class="neon-text text-center"><i data-lucide="trophy"></i> Live Sports in {name}</h2>
  <p class="text-center mb-2">Never miss a match with dedicated sports channels and PPV events</p>
  <div class="text-center mb-2">{sports_html}</div>

  <!-- Pricing -->
  <h2 class="neon-text text-center mt-2 mb-2"><i data-lucide="banknote"></i> {name} Pricing Plans</h2>
  <div class="grid grid-3 mb-2">
    <div class="card text-center">
      <div style="font-size:0.85rem; color:var(--text-body); text-transform:uppercase; letter-spacing:0.05em;">1 Month</div>
      <div style="font-size:2.5rem; font-weight:800; color:var(--text-heading); margin:1rem 0;">{curr}{prices.get('1_month','14.99')}</div>
      <div style="font-size:0.85rem; color:var(--text-body);">Billed monthly</div>
    </div>
    <div class="card text-center" style="border-color: {color}; position:relative; transform:scale(1.05); z-index:1;">
      <div style="position:absolute; top:-12px; left:50%; transform:translateX(-50%); background:{color}; color:#fff; font-size:0.75rem; font-weight:700; padding:4px 12px; border-radius:999px;">BEST VALUE</div>
      <div style="font-size:0.85rem; color:var(--text-body); text-transform:uppercase; letter-spacing:0.05em;">6 Months</div>
      <div style="font-size:2.5rem; font-weight:800; color:{color}; margin:1rem 0;">{curr}{prices.get('6_months','54.99')}</div>
      <div style="font-size:0.85rem; color:var(--text-body);">Save 40%</div>
    </div>
    <div class="card text-center">
      <div style="font-size:0.85rem; color:var(--text-body); text-transform:uppercase; letter-spacing:0.05em;">12 Months</div>
      <div style="font-size:2.5rem; font-weight:800; color:var(--text-heading); margin:1rem 0;">{curr}{prices.get('12_months','84.99')}</div>
      <div style="font-size:0.85rem; color:var(--text-body);">Save 53%</div>
    </div>
  </div>

  <img src="{img2}" alt="IPTV streaming {name}" loading="lazy" class="mb-2 mt-2">

  <!-- Why choose -->
  <h2 class="neon-text text-center mt-2 mb-2">Why {name} Viewers Love InfinityRec</h2>
  <div class="grid grid-3 mb-2">
    <div class="card">
      <div class="mb-1"><i data-lucide="zap"></i></div>
      <h3 class="neon-text">Zero Buffering</h3>
      <p style="font-size:0.9rem;">Our dedicated {name} servers deliver smooth 4K streams even during peak hours and major live events.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="satellite-dish"></i></div>
      <h3 class="neon-text">Local Channels Included</h3>
      <p style="font-size:0.9rem;">All major local and regional {name} channels available. Get the full local TV experience from {cities_html}.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="shield"></i></div>
      <h3 class="neon-text">VPN Friendly</h3>
      <p style="font-size:0.9rem;">Works perfectly with all major VPNs. Stream securely from anywhere in or outside {name}.</p>
    </div>
  </div>

  <!-- CTA -->
  <div class="card text-center mt-2 mb-2" style="background: radial-gradient(circle, rgba(255,45,149,0.1) 0%, var(--bg-card) 100%); border-color: var(--accent-pink);">
    <h2 class="neon-text-pink" style="font-size:1.8rem;"><i data-lucide="play-circle"></i> Ready to Cut the Cord in {name}? {flag}</h2>
    <p class="mb-2">Join 50,000+ {name} subscribers streaming smarter with InfinityRec. Start your free 24-hour trial today – no credit card needed.</p>
    <a href="index.html#pricing" class="btn">Start Free Trial for {name}</a>
  </div>

  <!-- Internal links -->
  <div class="card mt-2">
    <h3 class="neon-text"><i data-lucide="book-open"></i> Related Resources</h3>
    <div class="flex" style="gap:1rem; flex-wrap:wrap;">
      <a href="pillar.html">→ Ultimate IPTV Guide</a>
      <a href="setup-guide.html">→ Setup Guide</a>
      <a href="channel-list.html">→ Full Channel List</a>
      <a href="activate.html">→ Activate Subscription</a>
    </div>
  </div>
</div>"""

    schemas = schemas_tag(
        breadcrumb_schema([("Home","index.html"),(f"IPTV {name}",f"{geo['slug']}.html")]),
        article_schema(title, desc, date_s),
        {"@context":"https://schema.org","@type":"Service","name":f"IPTV Service {name}","areaServed":name,"provider":{"@type":"Organization","name":"InfinityRec"}}
    )

    html = base_html(title, desc, kws, body, depth="", schema_json=schemas, canonical_url=f"https://infinityrec.com/{geo['slug']}.html")
    write_html(os.path.join(output_dir, f"{geo['slug']}.html"), html)


# ──────────────────────────────────────────────
# PILLAR PAGE GENERATOR
# ──────────────────────────────────────────────
def render_pillar(config, faq_data, output_dir):
    title  = "Ultimate IPTV Guide 2026 – Everything About IPTV in USA, UK & Canada"
    desc   = ("The ultimate guide to IPTV in 2026. Learn what IPTV is, how to set it up, "
              "the best providers, and how to stream 15,000+ channels in the USA, UK, and Canada.")
    kws    = HEAD_TERMS + GEO_USA + GEO_UK + GEO_CANADA + ["iptv guide", "what is iptv", "iptv explained"]
    date_s = datetime.now().strftime("%Y-%m-%d")

    faqs_html = ""
    if faq_data:
        for item in faq_data[:6]:
            q = item.get("q", "")
            a = item.get("a", "")
            faqs_html += f"""
      <div class="faq-item">
        <button class="faq-question" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('open');">
          {q} <span class="faq-icon">+</span>
        </button>
        <div class="faq-answer"><p>{a}</p></div>
      </div>"""

    body = f"""
<section id="hero" class="hero">
  <div class="container">
    <div class="pill">📖 Complete IPTV Guide 2026</div>
    <h1 class="neon-text">The Ultimate <strong>Best IPTV</strong> Guide</h1>
    <p>Everything you need to know about <strong>IPTV service</strong>, <strong>IPTV subscription</strong> plans,
       and finding the top <strong>IPTV providers</strong> for <strong>IPTV USA</strong>, <strong>IPTV UK</strong>
       &amp; <strong>IPTV Canada</strong> in 2026.</p>
    <div class="flex-center mt-2" style="gap:1rem; flex-wrap:wrap;">
      <a href="index.html#pricing" class="btn pulse"><i data-lucide="play-circle"></i> Get Free Trial</a>
      <a href="setup-guide.html" class="btn btn-outline"><i data-lucide="settings"></i> Setup Guide</a>
    </div>
  </div>
</section>

<div class="container section">

  <!-- What is IPTV -->
  <div class="card mb-2">
    <h2 class="neon-text"><i data-lucide="tv"></i> What Is IPTV?</h2>
    <p>IPTV (Internet Protocol Television) is a technology that delivers live TV channels and video-on-demand
       content over the internet rather than traditional cable or satellite. The <strong>best IPTV</strong>
       services stream content directly to your device — no dish, no cable box, no contract.</p>
    <p>A premium <strong>IPTV subscription</strong> gives you access to thousands of live channels in 4K and HD,
       including sports, movies, news, and international content. Unlike cable, you can stream on any device
       from anywhere in the world.</p>
  </div>

  <!-- Why InfinityRec -->
  <h2 class="neon-text text-center mb-2">Why InfinityRec Is the Best IPTV Service</h2>
  <div class="grid grid-3 mb-2">
    <div class="card">
      <div class="mb-1"><i data-lucide="zap"></i></div>
      <h3 class="neon-text">📺 10,000+ Channels</h3>
      <p>Access the widest network of top <strong>IPTV providers</strong> worldwide — live TV, sports, movies &amp; VOD.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="monitor"></i></div>
      <h3 class="neon-text">⚡ 4K Ultra HD – IPTV 4K</h3>
      <p>Crystal-clear <strong>IPTV 4K</strong> streams with zero buffering, even during peak hours and live events.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="trophy"></i></div>
      <h3 class="neon-text">⚽ Live Sports – IPTV Sports</h3>
      <p>NFL, NBA, Premier League, UFC &amp; F1 via dedicated <strong>IPTV sports</strong> channels in 4K quality.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="flame"></i></div>
      <h3 class="neon-text">🔥 Best IPTV for Firestick</h3>
      <p>The #1 recommended <strong>IPTV for Firestick</strong> — install in under 5 minutes and stream instantly.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="message-square"></i></div>
      <h3 class="neon-text">💬 24/7 Support</h3>
      <p>Our dedicated <strong>IPTV service</strong> team is available 24/7 via WhatsApp, live chat &amp; email.</p>
    </div>
    <div class="card">
      <div class="mb-1"><i data-lucide="banknote"></i></div>
      <h3 class="neon-text">💰 Affordable Plans</h3>
      <p>The most affordable <strong>IPTV subscription</strong> starting at $14.99/mo for USA, UK &amp; Canada.</p>
    </div>
  </div>

  <!-- IPTV by Region -->
  <h2 class="neon-text text-center mb-2">Best IPTV by Region</h2>
  <div class="grid grid-3 mb-2">
    <div class="card text-center">
      <div style="font-size:3rem;">🇺🇸</div>
      <h3 class="neon-text">IPTV USA</h3>
      <p>For <strong>IPTV USA</strong> viewers, InfinityRec delivers NFL, NBA, ESPN, CNN, Fox News and all
         major US networks in crystal-clear 4K. Dedicated US servers guarantee buffer-free streaming.</p>
      <a href="iptv-usa.html" class="btn btn-outline mt-1" style="width:100%;">Explore IPTV USA →</a>
    </div>
    <div class="card text-center">
      <div style="font-size:3rem;">🇬🇧</div>
      <h3 class="neon-text">IPTV UK</h3>
      <p>The top <strong>IPTV UK</strong> choice — Sky Sports, BT Sport, BBC, ITV, Premier League and all
         major UK channels. UK-optimised servers for flawless performance.</p>
      <a href="iptv-uk.html" class="btn btn-outline mt-1" style="width:100%;">Explore IPTV UK →</a>
    </div>
    <div class="card text-center">
      <div style="font-size:3rem;">🇨🇦</div>
      <h3 class="neon-text">IPTV Canada</h3>
      <p>Premium <strong>IPTV Canada</strong> — TSN, Sportsnet, CBC, CTV, RDS, TVA Sports and thousands
         of international channels in English &amp; French.</p>
      <a href="iptv-canada.html" class="btn btn-outline mt-1" style="width:100%;">Explore IPTV Canada →</a>
    </div>
  </div>

  <!-- How It Works -->
  <h2 class="neon-text text-center mb-2">How to Get Started with IPTV</h2>
  <div class="steps-grid mb-2">
    <div class="step-item">
      <div class="step-num">1</div>
      <h3 class="neon-text">Choose a Plan</h3>
      <p>Select the <strong>IPTV subscription</strong> plan that fits you — 1 month, 6 months, or 12 months at the best price.</p>
    </div>
    <div class="step-item">
      <div class="step-num">2</div>
      <h3 class="neon-text">Receive Credentials</h3>
      <p>Get your M3U URL and Xtream Codes login instantly by email after subscribing to our <strong>IPTV service</strong>.</p>
    </div>
    <div class="step-item">
      <div class="step-num">3</div>
      <h3 class="neon-text">Start Streaming</h3>
      <p>Install your preferred app on any device and enjoy the <strong>best IPTV</strong> experience right away.</p>
    </div>
  </div>

  <!-- FAQ -->
  {'<h2 class="neon-text text-center mb-2">Frequently Asked Questions</h2><div class="card mb-2">' + faqs_html + '</div>' if faqs_html else ''}

  <!-- Internal Links / CTA -->
  <div class="card text-center mb-2" style="background:radial-gradient(circle,rgba(0,240,255,0.07) 0%,var(--bg-card) 100%); border-color:var(--accent-cyan);">
    <h2 class="neon-text"><i data-lucide="play-circle"></i> Ready to Cut the Cord?</h2>
    <p class="mb-2">Join 50,000+ subscribers in USA, UK &amp; Canada streaming smarter with InfinityRec. No contract, cancel anytime.</p>
    <div class="flex-center" style="gap:1rem; flex-wrap:wrap;">
      <a href="index.html#pricing" class="btn btn-lg pulse">Get Free Trial Now</a>
      <a href="activate.html" class="btn btn-outline">Activate Account</a>
    </div>
  </div>

  <!-- Silo Internal Links -->
  <div class="card">
    <h3 class="neon-text"><i data-lucide="link"></i> Explore More</h3>
    <div class="grid grid-4" style="gap:1rem;">
      <a href="setup-guide.html" class="btn btn-outline" style="text-align:center;"><i data-lucide="settings"></i> Setup Guide</a>
      <a href="channel-list.html" class="btn btn-outline" style="text-align:center;"><i data-lucide="list"></i> Channel List</a>
      <a href="news.html" class="btn btn-outline" style="text-align:center;"><i data-lucide="newspaper"></i> News &amp; Blog</a>
      <a href="about.html" class="btn btn-outline" style="text-align:center;"><i data-lucide="info"></i> About Us</a>
    </div>
  </div>

</div>"""

    schema_list = [
        breadcrumb_schema([("Home","index.html"),("IPTV Guide","pillar.html")]),
        article_schema(title, desc, date_s),
    ]
    if faq_data:
        schema_list.append(faq_schema([(i.get("q",""),i.get("a","")) for i in faq_data[:6]]))

    html = base_html(title, desc, kws, body, depth="", schema_json=schemas_tag(*schema_list), canonical_url="https://infinityrec.com/pillar.html")
    write_html(os.path.join(output_dir, "pillar.html"), html)


# ──────────────────────────────────────────────
# ACTIVATE PAGE GENERATOR
# ──────────────────────────────────────────────
def generate_activate_page(output_dir):
    tpl_path = os.path.join(TEMPLATES_DIR, "activate.html")
    if not os.path.exists(tpl_path):
        return
    with open(tpl_path, "r", encoding="utf-8") as f:
        html = f.read()
    write_html(os.path.join(output_dir, "activate.html"), html)


def build_news_index(blog_topics, plaster_items, output_dir):
    title  = "IPTV News & Blog 2026 – Latest Guides for USA, UK & Canada"
    desc   = "Latest IPTV news, reviews, comparisons, and guides. Stay updated on the best IPTV services in 2026 for USA, UK & Canada."
    kws    = [b["title"].lower() for b in blog_topics[:8]]
    date_s = datetime.now().strftime("%Y-%m-%d")
    today  = datetime.now().strftime("%b %d, %Y")

    def card(title_item, href, cat, is_guide=False):
        img_slug = "news-" + href.split("/")[-1].replace(".html", "")
        img   = get_image_url(title_item, img_slug)
        badge_style = (
            'background:rgba(255,45,149,0.15);color:var(--accent-pink);'
            if is_guide else ''
        )
        link_color = 'var(--accent-pink)' if is_guide else 'var(--accent-cyan)'
        return f"""
    <div class="card" onclick="window.location.href='{href}'" style="cursor:pointer;display:flex;flex-direction:column;">
      <div style="aspect-ratio:16/9;overflow:hidden;border-radius:var(--radius);margin:-1.5rem -1.5rem 1.25rem;flex-shrink:0;">
        <img src="{img}" alt="{title_item}" loading="lazy"
             style="width:100%;height:100%;object-fit:cover;display:block;"
             onerror="this.parentElement.style.background='var(--bg-surface)';">
      </div>
      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
        <span class="pill" style="font-size:0.72rem;padding:2px 10px;{badge_style}">{cat}</span>
        <span style="font-size:0.78rem;color:var(--text-muted);">{today}</span>
      </div>
      <h3 class="neon-text" style="font-size:0.97rem;line-height:1.45;margin-bottom:0.75rem;flex:1;">
        <a href="{href}" style="color:inherit;">{title_item}</a>
      </h3>
      <a href="{href}" style="color:{link_color};font-size:0.85rem;font-weight:600;margin-top:auto;">Read More →</a>
    </div>"""

    blog_cards   = "".join(card(t["title"],  f"blog/{t['slug']}.html",    "Blog")  for t in blog_topics)
    guide_cards  = "".join(card(p["kw"].title(), f"plaster/{p['slug']}.html", "Guide", True) for p in plaster_items)

    body = f"""
<section class="hero">
  <div class="container">
    <span class="pill">Latest Updates 2026</span>
    <h1 class="neon-text">IPTV News &amp; <span style="color:var(--accent-pink);">Blog</span></h1>
    <p>Stay up to date with the latest IPTV news, streaming tips, expert guides and special offers for <strong>IPTV USA</strong>, <strong>IPTV UK</strong> &amp; <strong>IPTV Canada</strong>.</p>
    <div class="flex-center mt-2" style="gap:1rem;flex-wrap:wrap;">
      <a href="index.html#pricing" class="btn pulse"><i data-lucide="play-circle"></i> Get Free Trial</a>
      <a href="setup-guide.html" class="btn btn-outline"><i data-lucide="settings"></i> Setup Guide</a>
    </div>
  </div>
</section>

<div class="container section">

  <div class="grid grid-3 mb-2 text-center">
    <div class="card">
      <div class="neon-text" style="font-size:2.2rem;font-weight:800;">{len(blog_topics)}</div>
      <div style="color:var(--text-muted);font-size:0.8rem;text-transform:uppercase;letter-spacing:2px;">Articles</div>
    </div>
    <div class="card">
      <div class="neon-text" style="font-size:2.2rem;font-weight:800;color:var(--accent-pink);">{len(plaster_items)}</div>
      <div style="color:var(--text-muted);font-size:0.8rem;text-transform:uppercase;letter-spacing:2px;">Guides</div>
    </div>
    <div class="card">
      <div class="neon-text" style="font-size:2.2rem;font-weight:800;">2026</div>
      <div style="color:var(--text-muted);font-size:0.8rem;text-transform:uppercase;letter-spacing:2px;">Updated</div>
    </div>
  </div>

  <h2 class="neon-text text-center mb-2"><i data-lucide="newspaper"></i> Latest Blog Articles</h2>
  <div class="grid grid-3 mb-2">
    {blog_cards}
  </div>

  <h2 class="neon-text text-center mb-2" style="margin-top:3rem;"><i data-lucide="book-open"></i> In-Depth Guides</h2>
  <div class="grid grid-3 mb-2">
    {guide_cards}
  </div>

  <div class="card text-center mt-2" style="border-color:var(--accent-cyan);background:radial-gradient(circle,rgba(0,240,255,0.06) 0%,var(--bg-card) 100%);">
    <h3 class="neon-text"><i data-lucide="play-circle"></i> Ready to Stream?</h3>
    <p class="mb-2">Join 50,000+ subscribers across USA, UK &amp; Canada. Start your free trial today — no credit card needed.</p>
    <a href="index.html#pricing" class="btn btn-lg pulse">Get Free Trial Now</a>
  </div>

</div>"""

    schemas = schemas_tag(
        breadcrumb_schema([("Home","index.html"),("News","news.html")]),
        article_schema(title, desc, date_s)
    )
    html = base_html(title, desc, kws, body, depth="", schema_json=schemas, canonical_url="https://infinityrec.com/news.html")
    write_html(os.path.join(output_dir, "news.html"), html)

# ──────────────────────────────────────────────
# SITEMAP + ROBOTS
# ──────────────────────────────────────────────
def generate_sitemap(static_pages, blog_slugs, plaster_slugs, output_dir):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    today = datetime.now().strftime("%Y-%m-%d")
    for p in static_pages:
        pri = "1.0" if p == "index.html" else "0.8"
        lines.append(f'  <url><loc>https://infinityrec.com/{p}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>')
    for s in blog_slugs:
        lines.append(f'  <url><loc>https://infinityrec.com/blog/{s}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')
    for s in plaster_slugs:
        lines.append(f'  <url><loc>https://infinityrec.com/plaster/{s}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>')
    lines.append('</urlset>')
    write_html(os.path.join(output_dir, "sitemap.xml"), "\n".join(lines))

def generate_robots(output_dir):
    content = (
        "User-agent: *\nAllow: /\nDisallow: /privacy.html\nDisallow: /terms.html\n"
        "Sitemap: https://infinityrec.com/sitemap.xml\n"
    )
    write_html(os.path.join(output_dir, "robots.txt"), content)

# ──────────────────────────────────────────────
# MAIN BUILD
# ──────────────────────────────────────────────
def build_site(with_blackhat=False, with_images=False, clean=True):
    global _BLACKHAT, _WITH_IMAGES
    _BLACKHAT    = with_blackhat
    _WITH_IMAGES = with_images

    config   = load_json(CONFIG_PATH)
    faq_data = load_json(FAQ_PATH)
    if isinstance(faq_data, dict):
        faq_data = []

    if clean and os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "blog"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "plaster"), exist_ok=True)

    # ── 1. Static template pages ──────────────
    print("📄 Generating main pages...")
    # pillar.html → render_pillar()   news.html → build_news_index()   both skip template copy
    static_pages = ["index.html","setup-guide.html","channel-list.html",
                    "about.html","privacy.html","terms.html"]
    generated_static = []
    for page in static_pages:
        if copy_template_page(page, config, faq_data, OUTPUT_DIR):
            generated_static.append(page)
            print(f"   ✓ {page}")

    # Pillar page (programmatic, SEO-optimised)
    render_pillar(config, faq_data, OUTPUT_DIR)
    generated_static.append("pillar.html")
    print("   ✓ pillar.html")

    # ── 2. Blog pages ─────────────────────────
    print(f"\n📝 Generating {len(BLOG_TOPICS)} blog pages...")
    all_blog_slugs = [t["slug"] for t in BLOG_TOPICS]
    for topic in BLOG_TOPICS:
        generate_blog_page(topic, config, all_blog_slugs, OUTPUT_DIR)
    print(f"   ✓ {len(BLOG_TOPICS)} blog articles created")

    # ── 3. Plaster pages ──────────────────────
    print(f"\n🎯 Generating {len(LONG_TAIL_PLASTER)} plaster (long-tail) pages...")
    for item in LONG_TAIL_PLASTER:
        generate_plaster_page(item, config, all_blog_slugs, OUTPUT_DIR)
    print(f"   ✓ {len(LONG_TAIL_PLASTER)} plaster pages created")

    # ── 4. GEO pages ──────────────────────────
    print(f"\n🌍 Generating {len(GEO_CONFIG)} GEO-specific pages...")
    geo_slugs = []
    for geo_key, geo in GEO_CONFIG.items():
        generate_geo_page(geo_key, geo, config, OUTPUT_DIR)
        geo_slugs.append(f"{geo['slug']}.html")
        print(f"   ✓ {geo['slug']}.html")

    # ── 5. Xtream Activation page ─────────────
    print("\n🔌 Generating activation page...")
    generate_activate_page(OUTPUT_DIR)
    print("   ✓ activate.html")


    # ── 4. Build news index (fully programmatic) ──
    print("\n📰 Building news.html...")
    build_news_index(BLOG_TOPICS, LONG_TAIL_PLASTER, OUTPUT_DIR)
    generated_static.append("news.html")
    print("   ✓ news.html")

    # ── 5. Copy assets ────────────────────────
    for asset in ["css","js","images"]:
        src = os.path.join(TEMPLATES_DIR, asset)
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(OUTPUT_DIR, asset), dirs_exist_ok=True)
    if os.path.exists("styles.css"):
        shutil.copy("styles.css", os.path.join(OUTPUT_DIR, "styles.css"))

    # ── 6. Sitemap & Robots ───────────────────
    plaster_slugs = [p["slug"] for p in LONG_TAIL_PLASTER]
    all_extra = geo_slugs + ["activate.html"]
    generate_sitemap(generated_static + all_extra, all_blog_slugs, plaster_slugs, OUTPUT_DIR)
    generate_robots(OUTPUT_DIR)

    total = len(generated_static) + len(all_extra) + len(BLOG_TOPICS) + len(LONG_TAIL_PLASTER)
    print(f"\n✅ Build complete: {len(generated_static)} main + {len(geo_slugs)} geo + 1 activate + {len(BLOG_TOPICS)} blog + {len(LONG_TAIL_PLASTER)} plaster = {total} pages total")


    # ── 7. Blackhat injector ──────────────────
    if with_blackhat:
        print("\n💉 Running blackhat/greyhat injector...")
        subprocess.run(["python3", "seo_injector.py", OUTPUT_DIR])

# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InfinityRec IPTV Site Builder")
    parser.add_argument("--clean",         action="store_true", help="Wipe output dir before build")
    parser.add_argument("--with-images",   action="store_true", help="Fetch real images via APIs")
    parser.add_argument("--with-blackhat", action="store_true", help="Inject blackhat SEO elements")
    args = parser.parse_args()
    build_site(with_blackhat=args.with_blackhat, with_images=args.with_images, clean=args.clean)
