"""Genera la página publicada (docs/index.html) a partir del notebook ya ejecutado.

Uso (desde la raíz del repo):
    python scripts/build_site.py              # exporta las salidas guardadas
    python scripts/build_site.py --execute    # ejecuta el notebook antes de exportar

- Tema oscuro de JupyterLab + `site/theme.css` (fondo neón, código estilo editor).
- Oculta el código de las celdas con la etiqueta `presentation` (estilos y GUI).
- Agrega una barra superior con enlaces a la app, el notebook y el repositorio.
- Agrega la pestaña "Video" (#video): lee la URL de `docs/video.json`, así que el video se
  puede publicar después editando solo ese archivo desde GitHub.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from traitlets.config import Config

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "LogiExpress.ipynb"
THEME = ROOT / "site" / "theme.css"
OUTPUT = ROOT / "docs" / "index.html"
VIDEO_CONFIG = ROOT / "docs" / "video.json"
ASSETS = ("logo.png", "favicon.png")

REPO = "https://github.com/CamilaQuimbaya/logiexpress"
BINDER = "https://mybinder.org/v2/gh/CamilaQuimbaya/logiexpress/HEAD"
APP_URL = f"{BINDER}?urlpath=voila%2Frender%2Fapp.ipynb%3Fvoila-theme%3Ddark"
NOTEBOOK_URL = f"{BINDER}?labpath=LogiExpress.ipynb"


NAVBAR = f"""
<nav class="lx-nav">
  <a class="lx-brand" href="#"><img src="assets/favicon.png" alt=""><b>Logi<em>Express</em></b></a>
  <div class="lx-tabs">
    <a href="#" data-tab="project">📘 Proyecto</a>
    <a href="#video" data-tab="video">🎬 Video</a>
  </div>
  <div class="lx-links">
    <a class="primary" href="{APP_URL}" target="_blank" rel="noopener">🚀 App interactiva</a>
    <a href="{NOTEBOOK_URL}" target="_blank" rel="noopener">💻 Notebook</a>
    <a href="{REPO}" target="_blank" rel="noopener">GitHub</a>
  </div>
</nav>
"""

VIDEO_PANEL = r"""
<section id="lx-video" class="lx-video" hidden>
  <div class="lx-video-head">
    <div class="lx-eyebrow">Proyecto final · video</div>
    <h1>🎬 Explicación y demostración</h1>
    <p>Primeros 5 minutos: cómo representamos el grafo y la lógica de Dijkstra y Floyd-Warshall.
       Últimos 5 minutos: el sistema de rutas en acción.</p>
  </div>
  <div id="lx-video-player" class="lx-video-player">
    <div class="lx-video-soon">
      <img src="assets/logo.png" alt="">
      <b>Video en preparación</b>
      <span>Muy pronto aquí 🚚💨</span>
    </div>
  </div>
</section>
<script>
(function () {
  var main = document.querySelector("body > main");
  var panel = document.getElementById("lx-video");
  function showTab() {
    var onVideo = location.hash === "#video";
    panel.hidden = !onVideo;
    if (main) main.style.display = onVideo ? "none" : "";
    document.querySelectorAll("[data-tab]").forEach(function (tab) {
      tab.classList.toggle("active", (tab.dataset.tab === "video") === onVideo);
    });
    if (onVideo) window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", showTab);
  showTab();

  // Convierte enlaces de YouTube, Google Drive, Loom o Vimeo en su versión para incrustar.
  function toEmbed(url) {
    try {
      var u = new URL(url), host = u.hostname.replace(/^www\./, ""), m;
      if (host === "youtu.be") return "https://www.youtube.com/embed/" + u.pathname.slice(1);
      if (host.endsWith("youtube.com")) {
        if (u.searchParams.get("v")) return "https://www.youtube.com/embed/" + u.searchParams.get("v");
        m = u.pathname.match(/\/(shorts|embed|live)\/([^/?]+)/);
        if (m) return "https://www.youtube.com/embed/" + m[2];
      }
      if (host === "drive.google.com" && (m = u.pathname.match(/\/file\/d\/([^/]+)/)))
        return "https://drive.google.com/file/d/" + m[1] + "/preview";
      if (host.endsWith("loom.com")) return url.replace("/share/", "/embed/");
      if (host === "vimeo.com") return "https://player.vimeo.com/video/" + u.pathname.split("/")[1];
    } catch (error) { /* URL inválida: se muestra como enlace */ }
    return null;
  }

  fetch("video.json", { cache: "no-store" })
    .then(function (response) { return response.ok ? response.json() : {}; })
    .catch(function () { return {}; })
    .then(function (config) {
      var url = ((config && config.url) || "").trim();
      if (!url) return;                                   // sin video todavía: queda el aviso
      var player = document.getElementById("lx-video-player");
      var embed = toEmbed(url), element;
      if (embed) {
        element = document.createElement("iframe");
        element.src = embed;
        element.title = "Video de LogiExpress";
        element.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        element.allowFullscreen = true;
      } else {
        element = document.createElement("a");
        element.href = url;
        element.target = "_blank";
        element.rel = "noopener";
        element.className = "lx-video-link";
        element.textContent = "▶ Ver el video";
      }
      player.replaceChildren(element);
    });
})();
</script>
"""

FOOTER = f"""
<footer class="lx-footer">
  Proyecto final · Estructuras de datos y algoritmos de grafos ·
  <a href="{REPO}" target="_blank" rel="noopener">código fuente</a>
</footer>
"""


def load_notebook(execute: bool) -> nbformat.NotebookNode:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    if execute:
        ExecutePreprocessor(timeout=600, kernel_name="python3", store_widget_state=True).preprocess(
            notebook, {"metadata": {"path": str(ROOT)}})
        nbformat.write(notebook, NOTEBOOK)
    return notebook


def export_html(notebook: nbformat.NotebookNode) -> str:
    config = Config()
    config.HTMLExporter.theme = "dark"
    config.TagRemoveInputPreprocessor.enabled = True
    config.TagRemoveInputPreprocessor.remove_input_tags = {"presentation"}
    html, _ = HTMLExporter(config=config, template_name="lab").from_notebook_node(notebook)
    return html


def decorate(html: str) -> str:
    """Inserta el tema, el favicon, la barra superior y el pie."""
    head = ('<link rel="icon" type="image/png" href="assets/favicon.png">\n'
            f'<meta name="description" content="Sistema de gestión de rutas de entrega con Dijkstra y Floyd-Warshall">\n'
            f"<style>\n{THEME.read_text(encoding='utf-8')}\n</style>\n</head>")
    html = html.replace("</head>", head, 1)
    body_start = html.index("<body")
    body_tag_end = html.index(">", body_start) + 1
    html = html[:body_tag_end] + NAVBAR + html[body_tag_end:]
    return html.replace("</body>", VIDEO_PANEL + FOOTER + "</body>", 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--execute", action="store_true", help="ejecutar el notebook antes de exportar")
    args = parser.parse_args()

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(decorate(export_html(load_notebook(args.execute))), encoding="utf-8")
    (OUTPUT.parent / "assets").mkdir(exist_ok=True)
    for name in ASSETS:  # las imágenes que usa el notebook, junto a la página
        shutil.copy2(ROOT / "assets" / name, OUTPUT.parent / "assets" / name)
    (OUTPUT.parent / ".nojekyll").touch()
    if not VIDEO_CONFIG.exists():  # nunca sobrescribir el enlace que ya se haya puesto
        VIDEO_CONFIG.write_text(json.dumps({"url": ""}, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Página generada: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
