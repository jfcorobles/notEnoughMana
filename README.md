# 🧙‍♂️ Not Enough Mana - Companion App (PWA)

> Contador elegante, ligero y 100% offline de **Puntos de Vida (HP)** y **Reserva de Maná (MP)** para el juego de cartas y fiesta **Not Enough Mana**.

Diseñado para funcionar sin backend ni dependencias externas, listo para desplegarse directamente en **GitHub Pages** e instalarse en teléfonos móviles (**Android** e **iOS**) o computadoras como una Progressive Web App (PWA).

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

## 🛠️ Tecnologías

- **HTML5:** Semántica, metaetiquetas PWA y viewport optimizado contra zoom accidental.
- **CSS3:** Variables CSS, gradientes oscuros con resplandor neón (*box-shadow* / *drop-shadow*), diseño adaptable móvil/desktop.
- **JavaScript (ES6+):** Lógica del contador, Web Audio API, Screen Wake Lock API, Vibration API, Web Storage API.
- **Service Worker & Web Manifest:** Soporte offline completo e instalación como app nativa.
