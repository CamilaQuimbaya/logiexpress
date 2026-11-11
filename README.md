# 🚚 LogiExpress — Sistema de Gestión de Rutas de Entrega

Proyecto final de **Estructuras de Datos y Algoritmos de Grafos**: un sistema que calcula las rutas
de entrega más eficientes de una red vial (localidades de Bogotá) con **Dijkstra** y
**Floyd-Warshall**, implementados desde cero en Python siguiendo **arquitectura limpia**.

| | Enlace | Qué es |
|---|---|---|
| 🌐 | **[Ver el proyecto](https://camilaquimbaya.github.io/logiexpress/)** | Página estática con explicaciones, resultados y gráficos (abre al instante) |
| 🚀 | **[Abrir la app interactiva](https://mybinder.org/v2/gh/CamilaQuimbaya/logiexpress/HEAD?urlpath=voila%2Frender%2FLogiExpress.ipynb)** | La interfaz gráfica sin código (Voilà en Binder) |
| 💻 | **[Abrir el notebook](https://mybinder.org/v2/gh/CamilaQuimbaya/logiexpress/HEAD?labpath=LogiExpress.ipynb)** | Jupyter en la nube para ver y ejecutar el código |

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CamilaQuimbaya/logiexpress/HEAD?urlpath=voila%2Frender%2FLogiExpress.ipynb)

> ⏳ Binder es gratuito: la primera vez puede tardar unos minutos en arrancar y la sesión se borra
> al cerrarla.

## ✨ Funcionalidades

- **Ruta más corta** entre dos puntos, por tiempo o por distancia, con **recomendación** automática.
- **Todas las rutas desde un origen** (árbol de caminos más cortos de Dijkstra).
- **Rutas entre todos los pares** (matriz de Floyd-Warshall con mapa de calor).
- **🚧 Tráfico y cierres de vías:** reporta trancones o cierres y compara la ruta antes vs. después.
- **📦 Reparto con varias paradas** (problema del viajante): vecino más cercano, 2-opt y fuerza
  bruta sobre la matriz de Floyd-Warshall.
- **🎬 Algoritmos paso a paso:** animaciones de Dijkstra y Floyd-Warshall para entender cada decisión.
- **Dos interfaces** sobre el mismo núcleo: GUI con pestañas (ipywidgets) y menú de consola.
- **24 pruebas automáticas**, incluida la validación cruzada Dijkstra = Floyd-Warshall en todos los pares.

## 🏛️ Arquitectura

```
5 · Presentación     HtmlRenderer · NetworkPlotter · RoutePlannerGUI · ConsoleApp
4 · Datos            build_network · red de Bogotá
3 · Aplicación       RouteService (casos de uso)
2 · Algoritmos       Dijkstra · Floyd-Warshall · DeliveryRoutePlanner
1 · Dominio          Location · Route · RoadNetwork · RoadConditions · PathResult
```

Cada capa solo depende de las capas internas. Principios aplicados: SRP, abierto/cerrado,
inversión de dependencias, patrones Strategy y Observer, entidades inmutables y validación en el
dominio. Todo el código está en un solo archivo, **[`LogiExpress.ipynb`](LogiExpress.ipynb)**, como
pide el enunciado.

## 💻 Ejecutarlo en local

```bash
git clone https://github.com/CamilaQuimbaya/logiexpress.git
cd logiexpress
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook LogiExpress.ipynb # o, como app sin código: voila LogiExpress.ipynb
```

Luego **Run → Run All Cells** y ve a la **sección 8** (GUI) o a la **sección 9** (consola).
Requiere Python 3.10 o superior.

## 🗺️ Cambiar los datos

La red está en el diccionario `BOGOTA_NETWORK` (sección 4). Para usar otra ciudad solo hay que
editar ese diccionario; el resto del código no cambia. Para una vía de un solo sentido se agrega
`"two_way": False`.
