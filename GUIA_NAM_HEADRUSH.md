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
4. El motor escanea de forma recursiva los archivos `.nam` en las rutas soportadas (`/media/az01-internal/Evil/usb_mnt/NAM`, `/media/az01-internal/Evil/NAM`, `/media/az01-internal/NAM`, `/NAM` y carpeta de IRs) usando un hilo de baja prioridad (`SCHED_IDLE` y `nice(19)`) para no afectar al hilo de audio.
5. Conecta el USB a la toma trasera de la Gigboard antes de encender o antes de entrar al rig.

---

## 6. Amplificadores Custom Circuit-Modeled (IDs 53–62)

Además de los dos bloques NAM, el firmware expande la lista interna de amplificadores de **53 a 63 modelos** sin eliminar ninguno de los originales, incorporando 10 amplificadores modelados a nivel de circuito (con sobremuestreo 2x a 96 kHz en modelos seleccionados y gráficos 290×119 integrados en pantalla):

| DSP ID | Hex | Modelo | Descripción técnica |
| :---: | :---: | :--- | :--- |
| **53** | `0x35` | **Mesa Triple Crown Ch2** | Canal crunch/drive (`MesaTripleCrownDSP`, 96 kHz oversampled) |
| **54** | `0x36` | **Mesa Lone Star** | Limpios cálidos 3D y overdrive clásico (`MesaLoneStarDSP`) |
| **55** | `0x37` | **Mesa Triple Crown Lead** | Canal Lead de alta ganancia (`MesaTripleCrownDSP` canal 3) |
| **56** | `0x38` | **Dumble Steel String Singer** | Limpio de alto headroom 100W–150W (`DumbleSSSDSP`) |
| **57** | `0x39` | **Dumble Overdrive Special** | Canal Overdrive tipo #102/#124 (`DumbleODSDSP`) |
| **58** | `0x3a` | **Elmwood Bonneville 50** | Crunch británico/sueco EL34 de 50W (`ElmwoodBonnevilleDSP`) |
| **59** | `0x3b` | **IRENE** | Clean Reference Engine (híbrido Dumble SSS + Mesa Lone Star con compresión óptica suave) |
| **60** | `0x3c` | **JON** | Modern Progressive Overdrive Engine de 3 voces (`JonOverdriveDSP`) |
| **61** | `0x3d` | **5150 Original 1992 Rhythm** | Canal Rhythm (`Peavey5150DSP`, layout UI `0x29`: Pre Gain, Resonance, Post, Presence) |
| **62** | `0x3e` | **5150 Original LEAD** | Canal Lead (`Peavey5150DSP`, layout UI `0x2b`) |

En el primer arranque sobre almacenamiento interno (`/media/az01-internal/Evil/usb_mnt/Blocks/AMP`) también se crean automáticamente los 3 bloques preconfigurados de Mesa TC-100 (`MESA TC-100 CH1 CLEAN.block`, `CH2 LO-GAIN.block`, `CH3 HI-GAIN.block`), también disponibles en `presets/AMP/`.

### Fichas Técnicas Individuales

#### ID 53 — Mesa Triple Crown Ch2 (`MesaTripleCrownDSP`, `channel = 2`)
- **Descripción:** Canal 2 (Lo-Gain) del cabezal Mesa/Boogie TC-100. Voz británica EL34 con mordedura media-alta enfocada, crunch dinámico y pegada orgánica en graves.
- **Cadena DSP:** `in_hpf` (72 Hz OFF / 110 Hz Bright ON) → `tight_peak` (2000 Hz, `Q = 0.95`, +1.5 / +3.2 dB) → Triodo V1 (`asym = 0.10`, `g1 = (0.75 + 6.80 * gain) * (1.25 si Bright)`) → `inter1_hpf` (75 / 105 Hz) → Triodo V2 (`asym = 0.16`, `g2 = 1.15 + 2.70 * gain`) → `inter2_hpf` (78 Hz) → `asym_tanh` (`asym = 0.08`) → Etapa EL34 Push-Pull (`sag = 0.36`, `pre_comp = 0.24`) → Post (`sub_tight_hpf` 48 Hz, `depth_thump` 96 Hz +1.5 dB, `kerrang_peak` 1650 Hz +1.8 dB, `def_peak` 2900 Hz +1.4 dB) → Limitador (`2.0:1 @ 0.50`) → `GuitarToneStack4`.
- **Tone Stack:** Bass 122 Hz (±12 dB) · Mid 720 Hz (`Q = 0.72`, +0.8 dB bias, ±12 dB) · Treble 1650 Hz (±12 dB) · Presence 4150 Hz (±11 dB).
- **Telemetría (50%):** Ganancia 1 kHz +16.62 dB · RMS Nominal 0.2312 · THD 22.32% (80% Gain: 28.05%) · H2: -19.80 dBc · H3: -14.89 dBc · RMS 12 kHz 0.1631.

#### ID 54 — Mesa Lone Star (`MesaLoneStarDSP`)
- **Descripción:** Canal 1 Clean del Mesa/Boogie Lone Star (100W/50W 6L6GC). Combina gran headroom texano, brillo tridimensional en púa y un selector de rectificador en el switch Bright (`0x9518`): Silicon (OFF) para respuesta rápida y firme, o 5U4GB Tube Sag (ON) para compresión elástica de fuente valvular.
- **Cadena DSP:** `in_hpf` (50 Hz) → Triodo V1A (`g = 0.78 + 2.45 * gain`) con inyector cuadrático `2f0` DC-blocked (`-0.12 * (d1_sq - dc_est)`) alineado constructivamente con `asym_tanh` → `ts_mid_body` (380 Hz +2.0 dB) → `sparkle_bell` (2.8 kHz +2.4 dB) → Triodo V1B con auto-compresión (`1 / (1 + 0.12 * env)`, `top35` empuja en el último 35% del Gain) → Power 6L6GC Class AB (`sag = 0.10` Silicon / `0.36` 5U4GB) → `sub_tight_hpf` (52 Hz) → `depth_thump` (84 Hz +1.6 dB) → `air_shelf` (5.8 kHz +1.8 dB) → `GuitarToneStack4`.
- **Tone Stack:** Bass 115 Hz (±12 dB) · Mid 520 Hz (`Q = 0.72`, ±11 dB) · Treble 1650 Hz (±12 dB) · Presence 4200 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +7.01 dB · RMS Nominal 0.2279 · THD 4.36% (80% Gain: 9.84%) · H2: -28.09 dBc · H3: -34.68 dBc · Span dinámico 23.9 dB (0.02 → 0.45).

#### ID 55 — Mesa Triple Crown Lead (`MesaTripleCrownDSP`, `channel = 3`)
- **Descripción:** Canal 3 (Hi-Gain Tight Lead) del TC-100. Diseñado para riffs articulados y solos definidos, con un HPF de entrada dinámicamente acoplado al control Bass (bajar Bass aprieta automáticamente el subgrave antes de la saturación).
- **Cadena DSP:** `in_hpf` dinámico (`118 Hz OFF / 142 Hz ON + (0.5 - bass) * 28 Hz`, rango 90..168 Hz) → `tight_peak` (1150 Hz, `Q = 1.20`, +2.0 / +3.2 dB) → Triodo V1 (`g1 = (1.10 + 11.5 * gain) * bright_mul`, `asym = 0.12`) → `inter1_hpf` (95 / 125 Hz) → `asym_tanh` (`1.65 + 1.85 * gain`, `asym = 0.14`) → `inter2_hpf` (95 Hz) → Triodo V2 (`1.50 + 3.30 * gain`, `asym = 0.34`) → `asym_tanh` (`1.75`, `asym = -0.06`) → Power EL34 rígido (`sag = 0.18`, atk 4.5 ms) → `kerrang_peak` (1620 Hz +3.0 dB) → `def_peak` (3000 Hz +1.6 dB) → Limitador (`3.2:1 @ 0.48`) + `tanh(0.9y) / 0.9` → `GuitarToneStack4`.
- **Tone Stack:** Bass 122 Hz (±12 dB) · Mid 560 Hz (`Q = 0.72`, scoop base -2.6 dB, ±12 dB) · Treble 1650 Hz (±12 dB) · Presence 4150 Hz (±11 dB).
- **Telemetría (50%):** Ganancia 1 kHz +20.52 dB · RMS Nominal 0.2531 · THD 26.75% (80% Gain: 28.91%) · H3: -12.82 dBc · RMS 12 kHz 0.2748.

#### ID 56 — Dumble Steel String (`DumbleSSSDSP`)
- **Descripción:** Inspirado en el Steel String Singer #002 (100W–150W 6L6GC/6550). Arquitectura ultra-limpia con extensión profunda de graves (35 Hz HPF), scoop de medios en 400 Hz y timbre cristalino tipo piano para absorber pedales delante o tocar limpios con enorme dinámica.
- **Cadena DSP:** `in_hpf` (35 Hz) → Previo lineal simétrico `tanh(pre_gain * sig * 0.5) / 0.5` (`0.50 + 1.85 * gain`) → `mid_scoop` (400 Hz, -4.2 dB) → `chime_peak` (2200 Hz, +3.0 dB) → `bright_shelf` (3800 Hz, +3.5 dB si Bright ON) → Power Stage rígido (`sag = 0.05`, rel 58 ms) + compresión de inversor de fase (`pi_comp = 0.16`) → `depth_thump` (90 Hz +1.6 dB) → `air_peak` (4800 Hz +1.5 dB) → `GuitarToneStack4`.
- **Tone Stack:** Bass 122 Hz (±12 dB) · Mid 500 Hz (`Q = 0.72`, ±11 dB) · Treble 1700 Hz (±12 dB) · Presence 4200 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +7.70 dB · RMS Nominal 0.2212 · THD 0.27% (80% Gain: 0.51%, el más lineal) · Span dinámico 26.4 dB (0.02 → 0.45) · RMS @ 0.70 = 0.6538.

#### ID 57 — Dumble ODS (`DumbleODSDSP`)
- **Descripción:** Dumble Overdrive Special (#102/#124, canal Overdrive) con voicing Skyliner. Con Bright=OFF entrega un overdrive cremoso y vocal; al activar Bright=ON entra en acción la entrada FET real (+12.5 dB / 4.2x) con mordedura JFET en 2.2 kHz que empuja la cascada OD1/OD2 a saturación densa y bloom armónico.
- **Cadena DSP:** `in_hpf` (65 Hz) → `[Opcional Bright=ON: ganancia 4.2x + 2f0 JFET + tanh(0.16s + 0.03)]` → Etapa Clean (`0.75 + 1.55 * gain`, `asym = 0.08`) → `skyliner_mid` (580 Hz +2.0 dB) → `bright_shelf` (2.2 kHz +3.8 dB ON) → `inter_hpf` (75 Hz) → Triodo OD1 (`0.75 + 4.50 * gain`, `asym = 0.22`, bloom 30/210 ms) → `gnarly_growl` (1550 Hz +1.8 dB) → Inyección `0.09 * tanh(4.2 * sig)` → Triodo OD2 (`0.80 + 2.90 * gain`, `asym = 0.28`) → Power Stage (`sag = 0.24`, `pre_comp = 0.22`, `bias = 0.075`) → `sub_tight_hpf` (50 Hz) → `depth_thump` (102 Hz +1.4 dB) → `def_peak` (4800 Hz +1.8 dB) → `GuitarToneStack4`.
- **Tone Stack:** Bass 122 Hz (±12 dB) · Mid 620 Hz (`Q = 0.72`, ±11 dB) · Treble 1680 Hz (±12 dB) · Presence 4150 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +14.13 dB (+5.65 dB con FET ON) · RMS Nominal 0.2294 · THD 25.66% (80% Gain: 34.25%) · H2: -19.44 dBc · H3: -13.47 dBc.

#### ID 58 — Elmwood Bonneville 50 (`ElmwoodBonnevilleDSP`)
- **Descripción:** Amplificador boutique sueco de 50W EL34 (híbrido Plexi-AC30 crudo). Destaca por incorporar el motor `ProgramSustain` con hasta +20 dB de recuperación controlada por puerta anti-ruido (-63 a -52 dBFS) y una cascada de 5 triodos con asimetrías alternadas para un grano británico orgánico y canto infinito en solos.
- **Cadena DSP:** `ProgramSustain` (atk 10 ms, rel 150 ms, `max_up 10.5x`, `min_down 0.30x`) → `pre_hpf` (75/95 Hz) → `pre_clarity` (2.2 kHz +2.0 dB) → `bright_chime` (2.6 kHz +3.2 dB ON) → 4 Triodos en cascada (V1 +0.18 → `inter_hpf` 75 Hz → V2 -0.14 → V3 +0.15 → V4 -0.10) → Cathode Follower (+0.06) → Power 50W EL34 (`sag = 0.16`, `bias = 0.035`) → `post_wood_body` (880 Hz +1.8 dB) → `post_kerrang` (2150 Hz +1.8 dB) → `GuitarToneStack4`.
- **Tone Stack:** Bass 85 Hz (±12 dB) · Mid 820 Hz (`Q = 0.72`, ±11 dB) · Treble 1680 Hz (±12 dB) · Presence 3650 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +20.83 dB · RMS Nominal 0.2334 · THD 43.21% (80% Gain: 45.78%) · RMS sostenido `0.2186..0.2324` en todo el rango `0.01..0.70` · RMS 12 kHz 0.2057.

#### ID 59 — IRENE (`IreneCleanDSP`)
- **Descripción:** Clean Reference Engine — diseño original híbrido que fusiona la velocidad y headroom del Dumble SSS con la calidez 3D del Lone Star. Usa un compresor óptico paralelo (`tick_optical`, 55% mezcla paralela) con ataque lento de 35 ms para dejar pasar intacto el ataque de la púa, ecualización de mezcla lista para grabación y un generador puro de 2º armónico par (`2f0`) tipo triodo de 400V con aire abierto hasta 18 kHz.
- **Cadena DSP:** `pre_hpf` (68 Hz) → `ProgramSustain::tick_optical` (atk 35 ms, rel 220 ms, 1.75:1, +5/-4.5 dB, mix 55%) → Esculpido de estudio (105 Hz low-shelf +1.0 dB → 320 Hz dip -2.0 dB → 1050 Hz vocal +2.0 dB → 2.8 kHz chime +3.2 dB → 5.2 kHz air-shelf +2.6 / +5.4 dB Bright ON) → Generador 400V `2f0` (`k2 = 0.11 + 0.12 * gain`, DC-blocked) + `tanh(0.18s) / 0.18` → Power 100W 6L6GC/KT66 (`sag = 0.12`, `bias = 0.015`) → `GuitarToneStack4`.
- **Tone Stack:** Bass 118 Hz (±12 dB) · Mid 820 Hz (`Q = 0.72`, ±11 dB) · Treble 1800 Hz (±12 dB) · Presence 4400 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +11.97 dB · RMS Nominal 0.2202 · THD 2.20% (80% Gain: 3.78%) · H2: -33.20 dBc vs H3: -53.98 dBc (+20.8 dB halo par) · Span dinámico 21.8 dB (0.02 → 0.45) con pico de ataque 0.860.

#### ID 60 — JON (`JonOverdriveDSP`)
- **Descripción:** Modern Progressive Overdrive Engine — arquitectura original de 3 voces progresivas controladas por el propio recorrido de Gain: desde Clean/Blues cálido en valores bajos, pasando por Liquid Lead en rango medio, hasta Surgical Tight Metal al subir Gain por encima del 36%, donde realiza un crossfade continuo (`blend_45`) hacia una doble etapa de recorte de grano fino inspirada en Soldano/Triple Crown.
- **Cadena DSP:** `pre_hpf` adaptativo (68 → 137 Hz + trim inverso con Bass) → `pre_dip` adaptativo en 320 Hz (0 → -3.8 dB) → `pre_focus` deslizante (520 Hz +1.2 dB → 1400 Hz +2.4 dB) → `bright_boost` (2.3 kHz +3.2 dB ON) → S1 lineal → S2/S3 triodos bloom (30/190 ms) → `inter_hpf` (115 Hz) → Crossfade `blend_45` hacia `[S4 (2/65 ms, asym = 0.05) → S5 (tanh 0.90) → CF (asym = 0.04)]` → Power Stage (`sag = 0.12`, `bias = 0.02`) → `nfb_punch` (78 Hz +1.0 dB) → `post_clean_dip` (340 Hz -2.2 dB) → `post_soldano_edge` (1450 Hz +2.2 dB) → `GuitarToneStack4 (* blend_trim)`.
- **Tone Stack:** Bass 122 Hz (±12 dB) · Mid 640 Hz (`Q = 0.72`, ±12 dB) · Treble 1700 Hz (±12 dB) · Presence 4200 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +17.71 dB · RMS Nominal 0.2366 · THD 17.02% (80% Gain: 25.90%) · H2: -24.32 dBc · H3: -16.36 dBc · RMS 12 kHz 0.1859.

#### ID 61 — 5150 Original 1992 Rhythm (`Pv5150DSP`, `is_lead = false`)
- **Descripción:** Canal Rhythm del Peavey 5150 "Block Letter" de 1992 (topología V1A → V1B → V6A + etapa 4x6L6GC). Usa el layout nativo `0x29` con controles Pre Gain, Resonance, Post, High/Mid/Low, Presence y switch Bright (que emula el condensador treble-bleed de 4700 pF sobre el potenciómetro Pre Gain, atenuándose al subir la ganancia).
- **Cadena DSP:** `pre_hpf` (56..80 Hz) → `pre_mid_push` (820 Hz +1.0 dB) → `bright_shelf` (`2.35 kHz`, `+4.4 dB * (1 - 0.65 * pre_gain)` ON) → Triodo V1A (`asym = 0.06`) → `inter_hpf` (72 Hz) → V1B (`asym = 0.14`) → V6A (`asym = 0.18`) → `inter_fizz` (-1.2 dB @ 5.4 kHz) → Power 4x6L6GC (`sag = 0.11`, `bias = 0.045`, Post > 70% añade saturación de potencia) → `nfb_resonance` (72 Hz, `Q = 1.05`, 0 → +8.6 dB, +4.3 dB al 50%) → `GuitarToneStack4`.
- **Tone Stack:** Low 116 Hz (±12 dB) · Mid 680 Hz (`Q = 0.72`, ±12 dB) · High 1860 Hz (±12 dB) · Presence 3950 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +9.19 dB · RMS Nominal 0.2429 · Resonance @ 72 Hz: +4.30 dB (50%) / +8.60 dB (100%) · Bright @ 3.5 kHz: +2.81 dB · THD 17.04% (80% Gain: 28.24%).

#### ID 62 — 5150 Original LEAD (`Pv5150DSP`, `is_lead = true`)
- **Descripción:** Canal LEAD del Peavey 5150 "Block Letter" 1992 (layout `0x2b`). Cascada completa de 5 etapas incluyendo la icónica etapa V2B con cátodo frío de 39k (`asym = 0.42f`), que genera su saturación agresiva y densidad armónica característica sin muro pasa-bajos (conservando apertura hasta ~15 kHz). El switch Bright no tiene efecto en el canal LEAD, tal como en el amplificador original.
- **Cadena DSP:** `pre_hpf` (82..114 Hz) → `pre_mid_push` (1050 Hz +2.4 dB) → V1A (`asym = 0.08`) → `inter_hpf` (112 Hz) → V2A (`asym = 0.12`) → V2B 39k Cold Clipper (`asym = 0.42`) → `inter_fizz` (-3.2 dB @ 5.4 kHz) → V6A (`asym = 0.16`) → `tanh(0.92s) / 0.92` → Power 4x6L6GC (`sag = 0.11`, `bias = 0.045`) → `nfb_resonance` (72 Hz, `Q = 1.12`, 0 → +9.4 dB, +4.7 dB al 50%) → `GuitarToneStack4`.
- **Tone Stack:** Low 112 Hz (±12 dB) · Mid 650 Hz (`Q = 0.76`, ±12 dB) · High 1820 Hz (±12 dB) · Presence 4150 Hz (±10 dB).
- **Telemetría (50%):** Ganancia 1 kHz +18.84 dB · RMS Nominal 0.2490 · Resonance @ 72 Hz: +4.69 dB (50%) / +9.39 dB (100%) · Presence @ 4.2 kHz (0% → 100%): +9.80 dB · THD 35.45% (80% Gain: 36.37%) · RMS 10 kHz 0.1793.

---

## 7. Modo Ingeniería (Dev Mode) y Medidor de CPU DSP

- **Pantallas ocultas desbloqueadas:** `RedirCtrl EnableDevAccess` queda activado por defecto y `GlobalSettings.qml` habilita el acceso a los menús de ingeniería (`dev menu`, `ampTweak` y `fftDisplay`).
- **Soporte táctil en Dev Mode:** Los componentes `DevComboWithText.qml`, `NotifyKnobWithTexts.qml` y `NotifyButtonWithText.qml` están parcheados para responder directamente a la pantalla táctil.
- **Medidor de CPU DSP siempre visible:** `ShowCPUTime` se activa por defecto al arranque junto con el overlay `EngineInfo.qml` para monitorizar en tiempo real la carga de CPU de cada modelo NAM o amplificador custom.

