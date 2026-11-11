"""Genera la página publicada (docs/index.html) a partir del notebook ya ejecutado.

Uso (desde la raíz del repo):
    python scripts/build_site.py              # exporta las salidas guardadas
    python scripts/build_site.py --execute    # ejecuta el notebook antes de exportar

- Tema oscuro de JupyterLab + `site/theme.css` (fondo neón, código estilo editor).
- Oculta el código de las celdas con la etiqueta `presentation` (estilos y GUI).
- Agrega una barra superior con enlaces a la app, el notebook y el repositorio.
"""
from __future__ import annotations

import argparse
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
ASSETS = ("logo.png", "favicon.png")

REPO = "https://github.com/CamilaQuimbaya/logiexpress"
BINDER = "https://mybinder.org/v2/gh/CamilaQuimbaya/logiexpress/HEAD"
APP_URL = f"{BINDER}?urlpath=voila%2Frender%2FLogiExpress.ipynb%3Fvoila-theme%3Ddark"
NOTEBOOK_URL = f"{BINDER}?labpath=LogiExpress.ipynb"


NAVBAR = f"""
<nav class="lx-nav">
  <a class="lx-brand" href="#"><img src="assets/favicon.png" alt=""><b>Logi<em>Express</em></b></a>
  <div class="lx-links">
    <a class="primary" href="{APP_URL}" target="_blank" rel="noopener">🚀 App interactiva</a>
    <a href="{NOTEBOOK_URL}" target="_blank" rel="noopener">💻 Notebook</a>
    <a href="{REPO}" target="_blank" rel="noopener">GitHub</a>
  </div>
</nav>
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
    return html.replace("</body>", FOOTER + "</body>", 1)


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
    print(f"✅ Página generada: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
