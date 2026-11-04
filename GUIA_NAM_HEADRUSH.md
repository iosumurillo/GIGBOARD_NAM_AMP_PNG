# Guía Completa de Uso: NAM (Neural Amp Modeler) en HeadRush Gigboard v2.7

Este documento detalla el funcionamiento, la arquitectura interna y la guía de uso de los dos bloques secuestrados para ejecutar inferencia de redes neuronales **Neural Amp Modeler (NAM)** en tu HeadRush Gigboard con firmware 2.7:
1. **Pedal Anxiety OD (NAM)** (y Anxiety OD V2)
2. **Amplificador 82 LEAD 800 (NAM)**

---

## 1. ¿Qué tiene de especial esta implementación?

A diferencia de soluciones externas o modificaciones genéricas, este mod está integrado directamente en el núcleo del motor de audio de HeadRush (`/usr/Evil/Evil`):
- **Motor NAM Nativo de Baja Latencia:** Ejecuta inferencia optimizada para la CPU ARM Cortex-A9 con aceleración vectorial NEON y punto flotante duro (`neon-vfpv4`).
- **Soporte de Modelos NAM A2 (Slimmable):** Calibra automáticamente en segundo plano la resolución del modelo para adaptarse al presupuesto de CPU de la pedalera, evitando caídas de buffer (*underruns*) o sobrecalentamiento.
- **Transición Silenciosa (Duck & Switch):** Al girar el potenciómetro selector de modelo, el sistema aplica una rampa matemática de coseno elevado (*raised-cosine*) de 100 ms que atenúa el perfil anterior y levanta el nuevo suavemente, eliminando clics, zumbidos o ruidos digitales.
- **Precarga en Segundo Plano:** El análisis de los archivos `.nam` del USB se realiza en un hilo de baja prioridad; el hilo de audio en tiempo real nunca se bloquea ni se congela la pantalla táctil.
- **Gráficos Integrados en Pantalla Diferenciados:**
  - El pedal **Anxiety OD** muestra la versión vertical del pedal NAM A2.
  - El amplificador **82 LEAD 800 (NAM)** muestra el cabezal horizontal apaisado del amplificador NAM A2.
  - Se corrigió la resolución de nombres en QML para que el renombramiento del bloque `82 LEAD 800 (NAM)` resuelva de forma nativa la imagen del cabezal en el motor de recursos de Qt.

---

## 2. Bloque de Pedal: Anxiety OD (NAM)

El bloque **Anxiety OD** actúa como un cargador directo y minimalista de perfiles NAM con ganancia de entrada y salida transparente.

```
       [Entrada Audio]
              │
              ▼
   ┌──────────────────────┐
   │ Tone Knob (0x548)    │ ──► Ganancia de Entrada (Input Trim)
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Drive Knob (0x534)   │ ──► Selector de Perfil (.nam del USB)
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Level Knob (0x520)   │ ──► Ganancia de Salida (Output Trim)
   └──────────────────────┘
              │
              ▼
       [Salida Audio]
```

### Controles de Anxiety OD
| Control UI | Offset Interno | Rango UI | Función Técnica en NAM Mod |
| :--- | :--- | :--- | :--- |
| **Drive** | `this_ + 0x534` | 0% .. 100% | **Selector de Modelo NAM**: Divide el recorrido del potenciómetro proporcionalmente entre todos los archivos `.nam` presentes en la carpeta `/NAM` del pendrive USB. |
| **Tone** | `this_ + 0x548` | 0% .. 100% | **Input Trim (Ganancia de Entrada)**:<br>• **0%**: Silencio total.<br>• **50%**: Ganancia unitaria exacta (0.0 dB / 1.0x).<br>• **100%**: Realce de +12 dB. |
| **Level** | `this_ + 0x520` | 0% .. 100% | **Output Trim (Volumen Maestro)**:<br>• **0%**: Silencio total.<br>• **50%**: Nivel unitario exacto (0.0 dB / 1.0x).<br>• **100%**: Realce de +12 dB. |
| **Interruptor On/Off** | `this_ + 0x26b` | 0 / 1 | **Bypass Analógico/Seco**: Cuando el pedal se apaga en la pantalla o por pedalera, el audio pasa en seco (*dry passthrough*) de forma inmediata. |

> [!TIP]
> **Recomendación de Uso:** Sitúa **Tone** y **Level** al **50%**. En esta posición la señal no sufre ninguna alteración de ganancia, reproduciendo el perfil NAM tal y como fue capturado originalmente.

---

## 3. Bloque de Amplificador: 82 LEAD 800 (NAM)

El bloque **82 LEAD 800 (NAM)** ofrece una sección completa de ecualización activa de 3 bandas, presencia, filtro para control de graves y selector de modelo independiente.

```
       [Entrada Audio]
              │
              ▼
   ┌──────────────────────┐
   │ Bright Switch (9518) │ ──► Filtro Paso Altos (HPF 150 Hz - Tight Cut)
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Gain Knob (9500)     │ ──► Ganancia de Entrada (Input Trim)
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Depth Knob (9538)    │ ──► Inferencia NAM (.nam seleccionado)
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Bass (9524, 100 Hz)  │
   │ Mid  (9528, 750 Hz)  │ ──► Tone Stack Activo Post-NAM
   │ Treble (952c, 3.5k)  │
   │ Presence (9510, 6k)  │
   └──────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Master Knob (9508)   │ ──► Volumen de Salida Maestro
   └──────────────────────┘
              │
              ▼
       [Salida Audio]
```

### Controles Detallados por Página

#### Página 1: Ganancia y Dinámica Primaria
* **Gain (Knob 1, `0x9500`):**
  * Control de saturación previa a la red neuronal.
  * Curva logarítmica/lineal calibrada: en **50%** es ganancia neutra (0 dB / 1.0x). Al 0% apaga la señal y al 100% aplica hasta +12 dB de empuje para capturas con baja señal de entrada.
* **Presence (Knob 2, `0x9510`):**
  * Filtro High-Shelf activo en **6000 Hz** con un margen de $\pm 10\text{ dB}$.
  * En **50%**, el filtro se desactiva digitalmente por completo (0 dB).
  * Ideal para abrir el brillo superior o suavizar perfiles demasiado chillones.
* **Master (Knob 3, `0x9508`):**
  * Nivel de salida general tras la inferencia y ecualización.
  * Mismo comportamiento que el Level de Anxiety OD: **50% = 0 dB**.

#### Página 2: Tone Stack (Ecualizador de 3 Bandas)
* **Bass (Knob 1, `0x9524`):**
  * Filtro Low-Shelf centrado en **100 Hz** con margen de $\pm 12\text{ dB}$.
  * Al 50% no colorea la señal (0 dB). Permite engrosar la pegada o limpiar graves retumbantes.
* **Mid (Knob 2, `0x9528`):**
  * Filtro Peaking tipo campana centrado en **750 Hz** ($Q = 1.0$) con $\pm 12\text{ dB}$.
  * Al 50% es plano (0 dB). 750 Hz es la frecuencia clásica británica que define el cuerpo de la guitarra en la mezcla.
* **Treble (Knob 3, `0x952c`):**
  * Filtro High-Shelf centrado en **3500 Hz** con margen de $\pm 12\text{ dB}$.
  * Al 50% es plano (0 dB). Controla la mordedura y ataque de púa.

#### Página 3: Herramientas Avanzadas y Selector de Modelo
* **Depth (Knob 1, `0x9538`):**
  * **Selector de Modelo NAM (Mapeo 1:1 idéntico a Anxiety OD)**:
  * Cada valor entero del potenciómetro (`0%` a `100%`) corresponde exactamente al archivo en esa posición alfabética:
    * `0%` $\to$ Archivo 0
    * `9%` $\to$ Archivo 9
    * `50%` $\to$ Archivo 50
  * Si el valor es mayor que la cantidad de modelos presentes en el pendrive, el sistema silencia la salida (sin inventar ni saltar a otros modelos).
  * Límite máximo: 101 perfiles (`0%` a `100%`).
* **Bright (Switch, `0x9518`):**
  * **Filtro Tight Cut (HPF 150 Hz)**:
    * **OFF**: Respuesta plana total sin filtrado.
    * **ON**: Activa un filtro paso altos de 2º orden a **150 Hz** ($Q = 0.707$) previo al modelo.
    * Elimina subgraves "barrosos" antes de la distorsión, aportando definición y precisión en riffs rápidos o afinaciones graves.

#### Conmutador de Bypass del Bloque
* **Offset `0x95a5`:**
  * Detecta el estado On/Off del bloque en la pantalla táctil de HeadRush.
  * Cuando está en **Off**, el bloque se desconecta de la ruta de audio inmediatamente y pasa la señal limpia en seco, mientras continúa la precarga en segundo plano para una reconexión instantánea.

---

## 4. Comparativa: ¿Cuándo usar cada bloque?

| Característica | Anxiety OD (NAM) | 82 LEAD 800 (NAM) |
| :--- | :--- | :--- |
| **Rol habitual** | Pedal de Overdrive / Boost o Perfiles Completos | Cabezal de Amplificador Principal |
| **Controles de Tono** | 1 control de tono plano | Ecualizador completo de 4 bandas (Bass, Mid, Treble, Presence) |
| **Filtro Paso Altos (Tight)** | No disponible | Conmutable vía switch **Bright** (corte en 150 Hz) |
| **Posición sugerida en Rig** | Al principio de la cadena (Slot de pedal pre-amp) | En el slot de Amplificador (antes de Cab/IR) |
| **Transparencia en 50%** | Idéntico a la captura (.nam) | Idéntico a la captura (.nam) con filtros en bypass automático |
| **Selector de Archivo** | Potenciómetro *Drive* | Potenciómetro *Depth* (Página 3) |

---

## 5. Organización de Archivos en el USB

1. Conecta tu pendrive USB formateado en FAT32 o exFAT a tu ordenador.
2. Crea una carpeta llamada exactamente **`NAM`** en la raíz:
   ```text
   D:\ (USB)
   └── NAM\
       ├── 01_Marshall_JCM800.nam
       ├── 02_Fender_Twin_Clean.nam
       ├── 03_Mesa_Boogie_DualRect.nam
       └── 04_Friedman_BE100.nam
   ```
3. Los perfiles se indexan en estricto orden alfabético. Nombrarlos con prefijos numéricos (`01_`, `02_`, etc.) te facilitará saber exactamente qué modelo corresponde a cada tramo del potenciómetro selector.
4. Conecta el USB a la toma trasera de la Gigboard antes de encender o antes de entrar al rig.

