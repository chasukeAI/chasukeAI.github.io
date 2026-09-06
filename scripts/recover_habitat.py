import base64
import re
import subprocess
from pathlib import Path

HISTORICAL_COMMIT = "f00d15a0a674158da84bad8844dd080236e940e9"
ALT = "Pixel-art scene of Chasuke, an otter, and a crow standing together in a cold purple northern landscape."

old_html = subprocess.check_output(
    ["git", "show", f"{HISTORICAL_COMMIT}:index.html"],
    text=True,
)
match = re.search(
    r'<img src="data:image/webp;base64,([^"]+)" alt="Pixel-art scene of Chasuke, an otter, and a crow standing together in a cold purple northern landscape\.">',
    old_html,
)
if not match:
    raise SystemExit("Could not recover historical habitat image")

image_bytes = base64.b64decode(match.group(1), validate=True)
if not image_bytes.startswith(b"RIFF") or b"WEBP" not in image_bytes[:16]:
    raise SystemExit("Recovered data is not a WEBP image")
Path("habitat.webp").write_bytes(image_bytes)

path = Path("index.html")
html = path.read_text(encoding="utf-8")
placeholder = '''        <div style="min-height:240px;display:grid;place-items:center;padding:34px;background:radial-gradient(circle at 50% 35%,rgba(145,92,255,.32),transparent 18rem),linear-gradient(180deg,#171323,#0c0c10);font-size:clamp(2.2rem,8vw,5rem);letter-spacing:.12em">🐙 🦦 🐦‍⬛</div>
        <figcaption class="habitat-caption">
          <strong>🐙 🦦 🐦‍⬛</strong>
          <span>north habitat · living system</span>'''
restored = f'''        <img src="habitat.webp" alt="{ALT}">
        <figcaption class="habitat-caption">
          <strong>🐙 🦦 🐦‍⬛</strong>
          <span>north habitat visual · 2026-08-30</span>'''

if placeholder not in html:
    raise SystemExit("Current habitat placeholder not found; refusing broad edit")
html = html.replace(placeholder, restored, 1)
path.write_text(html, encoding="utf-8")
