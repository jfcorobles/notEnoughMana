# 🧙‍♂️ Not Enough Mana - Companion App & Print & Play (Español)

> Contador elegante, ligero y 100% offline de **Puntos de Vida (HP)** y **Reserva de Maná (MP)**, junto con el **mazo completo de 154 cartas traducidas al español** en formato **Print & Play (PDF)** para el juego de cartas y fiesta **Not Enough Mana**.

Diseñado para funcionar sin backend ni dependencias externas, listo para desplegarse directamente en **GitHub Pages** e instalarse en teléfonos móviles (**Android** e **iOS**) o computadoras como una Progressive Web App (PWA). Incluye además una suite completa de herramientas para la traducción y generación de cartas imprimibles a 300 DPI.

---

## ✨ Características

- ❤️ **Puntos de Vida (HP):**
  - Comienza en **10 HP** (máximo).
  - Barra de salud segmentada con **10 pips de neón** dinámicos.
  - Alerta de latido rápido (*heartbeat pulse*) en vida crítica (≤ 3 HP).
  - Pantalla de derrota (*Game Over*) al llegar a 0 HP con opción de revivir.
  - Botones táctiles de `-1 HP` y `+1 HP`.

- 💧 **Reserva de Maná (MP):**
  - Comienza en **0 MP** y acumula maná ilimitado.
  - Estado contextual dinámico (*Pozo Vacío*, *Poción Cargada*, *Torrente de Maná*, *Sobrecarga Arcana*).
  - Botón principal de **Poción / Shot** (+3 MP) con etiqueta `REGLA BASE` y efecto resplandor.
  - Botones secundarios de `-1 Maná` y `+1 Maná`.

- 🔊 **Efectos de Sonido Procedurales (0 KB):**
  - Generados en tiempo real mediante **Web Audio API** (sin necesidad de descargar archivos `.mp3`).
  - Sonido de burbujas/sorbo para pociones, golpes de daño, campanas de curación, silbidos arcanos y campanada fúnebre.
  - Conmutador para silenciar/activar el audio con un toque.

- 📱 **Herramientas de Mesa:**
  - **Wake Lock (Pantalla siempre encendida):** Evita que el móvil bloquee la pantalla en mitad de la partida.
  - **Deshacer (Undo):** Revierte toques accidentales fácilmente.
  - **Vibración háptica:** Respuesta táctil al interactuar con los botones.
  - **Persistencia en `localStorage`:** No pierdes tus puntos si refrescas la página o sales de la aplicación.
  - **Modal de Reglas Rápidas:** Recordatorio inmediato de las mecánicas base del juego.

---

## ⌨️ Atajos de Teclado (PC)

Si juegas desde una laptop o PC de escritorio, puedes utilizar los siguientes atajos:

| Tecla | Acción |
| :--- | :--- |
| `1` o `Q` | **-1 HP** (Restar vida) |
| `2` o `W` | **+1 HP** (Sumar vida) |
| `Espacio` o `P` | **+3 Maná** (Beber Poción / Shot) |
| `A` | **-1 Maná** (Gastar maná) |
| `S` | **+1 Maná** (Añadir maná) |
| `Ctrl + Z` | **Deshacer** última acción |

---

## 📲 Instalación como PWA (Móvil)

### En Android (Google Chrome)
1. Abre la URL de la aplicación.
2. Toca el menú de opciones (tres puntos verticales) en la esquina superior derecha.
3. Selecciona **"Instalar aplicación"** o **"Agregar a la pantalla principal"**.

### En iOS (Safari)
1. Abre la URL en Safari.
2. Toca el botón de **Compartir** (icono con flecha hacia arriba).
3. Selecciona **"Agregar al inicio"** (*Add to Home Screen*).

La aplicación funcionará a pantalla completa y sin necesidad de conexión a internet gracias a su **Service Worker**.

---

## 🚀 Despliegue en GitHub Pages

Dado que la aplicación consta de archivos estáticos puros (`index.html`, `style.css`, `app.js`, `sw.js`, `manifest.webmanifest` y `favicon.svg`), el despliegue es inmediato:

1. Crea un nuevo repositorio en GitHub.
2. Inicializa git y sube los archivos:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Not Enough Mana PWA"
   git branch -M main
   git remote add origin https://github.com/jfcorobles/notEnoughMana.git
   git push -u origin main
   ```
3. En GitHub, dirígete a:
   **Settings** > **Pages**.
4. En la sección **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `main` (o `master`) / `/ (root)`
5. Haz clic en **Save**. En un par de minutos estará disponible en:
   ```
   https://jfcorobles.github.io/notEnoughMana/
   ```

---

## 💻 Ejecución Local

Puedes probar la aplicación localmente con cualquier servidor HTTP estático:

### Con Python:
```bash
python -m http.server 8080
```
Luego abre en tu navegador `http://localhost:8080`.

### Con Node.js / npx:
```bash
npx serve .
```

---

## 🃏 Cartas en Español & Print & Play (`translate_cards/`)

El repositorio incluye la baraja completa con las **154 cartas** del juego base traducidas al español, preparadas para imprimir y jugar (*Print & Play*), así como la suite de scripts en Python utilizada para la limpieza de imagen (*inpainting*), renderizado tipográfico y ensamblado de PDFs.

### 📄 Documentos PDF Listos para Imprimir

En la carpeta [`translate_cards/`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards) se encuentran los archivos PDF ya generados:

1. **[`Cartas_Espanol_Print_and_Play.pdf`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/Cartas_Espanol_Print_and_Play.pdf)** (~9.5 MB)
   - **Formato:** 18 páginas en tamaño **A4 a 300 DPI**.
   - **Distribución:** Cuadrícula de **3x3 (9 cartas por hoja)** a tamaño estándar de naipe poker (**63.5 × 88.9 mm** / **2.5 × 3.5 in**).
   - **Guías de corte:** Líneas perimetrales discretas en los márgenes exteriores para cortar con regla y cúter sin dejar marcas en las cartas.
   - **Pie de página:** Indicador de número de hoja y especificaciones técnicas de impresión.

2. **[`Cartas_Espanol_Individuales.pdf`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/Cartas_Espanol_Individuales.pdf)** (~5.0 MB)
   - **Formato:** 154 páginas a resolución nativa completa (1 carta por página).
   - Ideal para consulta digital en tablets/móviles o impresión carta por carta en papel fotográfico o impresoras de tarjetas plásticas.

---

### 📂 Estructura de la Carpeta `translate_cards/`

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| [`Cartas_Espanol_Print_and_Play.pdf`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/Cartas_Espanol_Print_and_Play.pdf) | PDF en cuadrícula 3x3 listo para impresión en hojas A4/Carta con marcas de corte. |
| [`Cartas_Espanol_Individuales.pdf`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/Cartas_Espanol_Individuales.pdf) | PDF con las 154 cartas a 1 carta por página a resolución completa. |
| [`cards_database.json`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/cards_database.json) | Base de datos JSON con títulos, subtítulos en latín y textos traducidos con tokens para iconos (`{heart}`, `{drop}`) y negritas (`**`). |
| [`translate_cards.py`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/translate_cards.py) | Script de procesamiento: *inpainting* con OpenCV y composición tipográfica con Pillow. |
| [`generate_pdf.py`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/generate_pdf.py) | Script CLI para generar los PDFs en formato Print & Play (A4 o Carta) o individual. |
| [`MedievalSharp.ttf`](file:///c:/Users/Francisco%20Robles/Documents/apps/notEnoughMana/translate_cards/MedievalSharp.ttf) | Fuente gótica/medieval utilizada para renderizar los títulos de las cartas. |
| `EN/` | Carpeta con las 154 cartas originales en inglés. |
| `ES/` | Carpeta con las 154 cartas traducidas al español en formato `.png` en alta calidad. |

---

### ⚙️ Automatización y Scripts de Generación

Si deseas regenerar los PDFs o modificar las traducciones de las cartas:

#### 1. Requisitos Previos

Instala las librerías necesarias de Python:
```bash
pip install opencv-python pillow numpy pypdf
```

#### 2. Generador de PDFs (`generate_pdf.py`)

Genera los archivos PDF a partir de las imágenes de la carpeta `ES/`:

```bash
cd translate_cards

# Generar ambos PDFs (Print & Play en A4 + Individuales)
python generate_pdf.py

# Generar Print & Play en tamaño Carta (Letter)
python generate_pdf.py --format pnp --paper Letter

# Generar solo el PDF de cartas individuales
python generate_pdf.py --format single
```

#### 3. Traducción y Renderizado de Cartas (`translate_cards.py`)

Aplica limpieza del texto original mediante *inpainting* con algoritmo Telea y dibuja los textos en español respetando tipografías e iconos incrustados:

```bash
cd translate_cards
python translate_cards.py
```

---

## 🛠️ Tecnologías

### Companion App (PWA):
- **HTML5:** Semántica, metaetiquetas PWA y viewport optimizado contra zoom accidental.
- **CSS3:** Variables CSS, gradientes oscuros con resplandor neón (*box-shadow* / *drop-shadow*), diseño adaptable móvil/desktop.
- **JavaScript (ES6+):** Lógica del contador, Web Audio API, Screen Wake Lock API, Vibration API, Web Storage API.
- **Service Worker & Web Manifest:** Soporte offline completo e instalación como app nativa.

### Suite de Cartas & Print & Play:
- **Python 3:** Automatización de flujos de imagen y documentos.
- **OpenCV & NumPy:** Máscaras de color y algoritmos de *inpainting* (Telea) para remover textos preservando el fondo.
- **Pillow (PIL):** Composición gráfica, renderizado tipográfico (*MedievalSharp*, *Cambria*, *Segoe UI*) e incrustación de glifos de vida y maná.
- **PyPDF:** Verificación e inspección de estructura de páginas PDF.
