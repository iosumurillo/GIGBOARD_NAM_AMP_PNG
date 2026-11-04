# HeadRush Gigboard — Neural Amp Modeler (NAM) Mod

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Platform: HeadRush](https://img.shields.io/badge/Platform-Gigboard%20%7C%20MX5%20%7C%20Pedalboard-orange.svg)](#)
[![NAM Core](https://img.shields.io/badge/Engine-Neural%20Amp%20Modeler-green.svg)](https://github.com/sdatkinson/NeuralAmpModelerCore)
[![Release: v2.7 Extended](https://img.shields.io/badge/Release-v2.7%20Extended-success.svg)](https://github.com/iosumurillo/GIGBOARD_NAM_AMP_PNG/releases/tag/v2.7-nam-extended)

Modificación avanzada de firmware para **HeadRush Gigboard** (con compatibilidad para MX5 y Pedalboard) con **Firmware 2.7**, que integra de forma nativa la inferencia de redes neuronales [Neural Amp Modeler (NAM)](https://github.com/sdatkinson/NeuralAmpModelerCore) directamente en el motor de audio en tiempo real (`/usr/Evil/Evil`).

### Descargas Oficiales de Producción (Releases)

Para instalar el mod en tu pedalera sin necesidad de compilar código fuente:

| Archivo | Descripción | Descarga Directa |
| :--- | :--- | :--- |
| **Firmware Updater (NAM A2 extended mod)** | Flasheador automático para HeadRush Gigboard con soporte Dual NAM + Amp + Tone Stack | [Descargar .exe](https://github.com/iosumurillo/GIGBOARD_NAM_AMP_PNG/releases/download/v2.7-nam-extended/HeadRush.gigboard.Firmware.Updater.NAM.A2.extended.mod.exe) |
| **HeadRush NAM Block Manager** | Gestor de perfiles `.nam`, ordenación USB y generador de `.block` para Windows 10/11 | [Descargar .exe](https://github.com/iosumurillo/GIGBOARD_NAM_AMP_PNG/releases/download/v2.7-nam-extended/HeadRush_NAM_Block_Manager.exe) |

> **Página de la Release**: [v2.7 Extended Edition](https://github.com/iosumurillo/GIGBOARD_NAM_AMP_PNG/releases/tag/v2.7-nam-extended)  
> **Guía técnica y manual de usuario detallado**: [GUIA_NAM_HEADRUSH.md](GUIA_NAM_HEADRUSH.md)

---

## Demostración en Hardware Real (HeadRush Gigboard)

<p align="center">
  <img src="docs/images/gigboard_hardware_rig.jpg" alt="HeadRush Gigboard ejecutando NAM Mod" width="800" />
</p>

<p align="center">
  <img src="docs/images/gigboard_screen_chain.jpg" alt="Cadena de señal en pantalla táctil con doble bloque NAM (Pedal + Amp)" width="48%" />
  <img src="docs/images/gigboard_preset_picker.jpg" alt="Navegador de presets y bloques de amplificador" width="48%" />
</p>

### Gráficos Integrados en el Motor QML/RCC de HeadRush

| Bloque Pedal: Anxiety OD (NAM) | Bloque Amplificador: 82 LEAD 800 (NAM) |
| :---: | :---: |
| <img src="docs/images/nam_a2_pedal.jpg" alt="Pedal NAM A2 Vertical" width="260" /> | <img src="docs/images/nam_a2_amp_head.jpg" alt="Cabezal NAM A2 Horizontal" width="500" /> |
| *Diseño vertical para pedal de sobremarcha en la cadena* | *Cabezal apaisado con control de EQ activo de 3 bandas y Presence* |

---

## Características Principales

- **Doble Bloque NAM en Cadena**:
  - **Pedal Anxiety OD (NAM)** (y Anxiety OD V2): Inferencia transparente como pedal de saturación/overdrive con controles de Input Trim, Level y selector de modelo.
  - **Amplificador 82 LEAD 800 (NAM)**: Cabezal completo con inferencia NAM y **Tone Stack Activo** de 3 bandas (Bass a 100 Hz, Mid a 750 Hz, Treble a 3.5 kHz, Presence a 6 kHz) y filtro **Tight Cut HPF** a 150 Hz conmutable.
- **Inferencia de Ultra Baja Latencia**:
  - Motor compilado con soporte vectorial ARM Cortex-A9 NEON (`-mfpu=neon-vfpv4 -mfloat-abi=hard`).
  - Hilo de audio en tiempo real protegido contra caídas de buffer (*underruns*).
- **Transición Suave Duck & Switch**:
  - Rampa matemática de coseno elevado (*raised-cosine*) de 100 ms al cambiar de perfil, eliminando ruidos, clicks o zumbidos digitales.
- **Precarga en Segundo Plano**:
  - El análisis y lectura de perfiles `.nam` desde la unidad USB se realiza en un hilo de baja prioridad para no bloquear la interfaz gráfica ni el audio.
- **Gráficos Integrados en Pantalla Táctil**:
  - Gráficos integrados en los recursos QML/RCC de HeadRush: pedal vertical para Anxiety OD y cabezal horizontal apaisado para 82 LEAD 800.
- **HeadRush NAM Block Manager GUI**:
  - Herramienta de escritorio moderna incluida en `release/` para detectar pendrives USB, ordenar modelos alfabéticamente, calibrar trims y generar automáticamente bloques `.block` de presets listos para usar.
- **100+ Bloques Presets Incluidos**:
  - En la carpeta `presets/Blocks_Para_Tu_Gigboard` encontrarás bloques ya generados para carga instantánea.

---

## Estructura del Repositorio

```text
Gigboard_NAM/
├── docs/                 # Documentación e imágenes
│   ├── images/           # Fotografías en hardware real y recursos gráficos
│   └── RECOVERY.md       # Procedimiento de recuperación a firmware oficial
├── presets/              # Bloques listos para transferir a la memoria de la pedalera
│   └── Blocks_Para_Tu_Gigboard/
│       ├── ANXIETY OD/       # Presets 000 a 100 para pedal
│       └── ANXIETY OD V2/    # Presets 000 a 100 para segunda instancia
├── release/              # Ejecutables listos para producción
│   ├── HeadRush gigboard Firmware Updater (NAM A2 extended mod).exe
│   └── HeadRush_NAM_Block_Manager.exe
├── GUIA_NAM_HEADRUSH.md  # Manual técnico y guía completa de usuario
├── LICENSE               # Licencia GPLv3
└── README.md             # Esta documentación
```

---

## Mapeo de Controles

### Bloque Pedal: Anxiety OD (NAM)

| Control | Rango | Función Técnica |
| :--- | :--- | :--- |
| **Tone** | 0% – 100% | **Input Trim**: 50% = Ganancia Unitaria (0.0 dB). 0% = Mute, 100% = +12 dB. |
| **Drive** | 0% – 100% | **Selector de Modelo NAM**: Selecciona el archivo `.nam` correspondiente del pendrive USB (`0%` = Archivo 0, `100%` = Archivo 100). |
| **Level** | 0% – 100% | **Output Trim**: 50% = Salida Unitaria (0.0 dB). 0% = Mute, 100% = +12 dB. |
| **On/Off**| Bypass | Paso en seco directo (*dry passthrough*). |

---

### Bloque Amplificador: 82 LEAD 800 (NAM)

| Página | Control | Rango | Función Técnica |
| :--- | :--- | :--- | :--- |
| **Pág 1** | **Gain** | 0% – 100% | Ganancia de entrada previa a la red neuronal (50% = 0 dB). |
| **Pág 1** | **Presence** | 0% – 100% | Filtro High-Shelf activo en 6 kHz ($\pm 10\text{ dB}$, 50% = plano). |
| **Pág 1** | **Master** | 0% – 100% | Nivel de salida general post-inferencia y EQ (50% = 0 dB). |
| **Pág 2** | **Bass** | 0% – 100% | Filtro Low-Shelf centrado en 100 Hz ($\pm 12\text{ dB}$, 50% = plano). |
| **Pág 2** | **Mid** | 0% – 100% | Filtro Peaking en 750 Hz, $Q=1.0$ ($\pm 12\text{ dB}$, 50% = plano). |
| **Pág 2** | **Treble** | 0% – 100% | Filtro High-Shelf en 3.5 kHz ($\pm 12\text{ dB}$, 50% = plano). |
| **Pág 3** | **Depth** | 0% – 100% | **Selector de Modelo NAM**: Mapeo 1:1 exacto alfabético de perfiles USB. |
| **Pág 3** | **Bright** | OFF / ON | **Filtro Tight HPF (150 Hz)**: Elimina graves fangosos antes de la distorsión. |

---

## Inicio Rápido

### 1. Flashear la Pedalera
1. Conecta tu HeadRush Gigboard a la PC mediante cable USB.
2. En la pedalera, entra en **Global Settings -> Firmware Update**.
3. Ejecuta `HeadRush gigboard Firmware Updater (NAM A2 extended mod).exe` desde la carpeta `release/` o descárgalo directamente desde Releases.
4. Sigue los pasos en pantalla hasta que la pedalera complete el flasheo y reinicie.

### 2. Cargar Modelos en el Pendrive USB
1. En la pedalera, activa el modo **USB Transfer**.
2. Ejecuta `HeadRush_NAM_Block_Manager.exe` desde la carpeta `release/`.
3. Selecciona los modelos que deseas transferir. La herramienta organizará los nombres con prefijos numéricos ordenados alfabéticamente y generará los bloques de preset en las carpetas `Blocks/ANXIETY OD` y `Blocks/ANXIETY OD V2`.

### 3. Presets Listos para Copiar
Si prefieres no usar el gestor automático, puedes copiar directamente el contenido de la carpeta `presets/Blocks_Para_Tu_Gigboard` dentro de la carpeta `Blocks` del almacenamiento USB de tu HeadRush.

---

## Recuperación y Seguridad

El mod preserva la estructura de actualización oficial de HeadRush. Para restaurar el firmware original de fábrica en cualquier momento:
1. Pon la Gigboard en modo actualización de firmware.
2. Ejecuta el actualizador oficial de HeadRush Firmware 2.7.
3. Para más detalles, consulta [docs/RECOVERY.md](docs/RECOVERY.md).

---

## Licencia

- El código del mod y los hooks de integración están bajo la licencia [GPL v3](LICENSE).
- NeuralAmpModelerCore está bajo la licencia [MIT](https://github.com/sdatkinson/NeuralAmpModelerCore/blob/main/LICENSE).
- Las marcas HeadRush, Gigboard, MX5 y Pedalboard son marcas registradas de inMusic Brands, Inc. Este proyecto es una modificación comunitaria independiente y de código abierto sin afiliación con inMusic Brands.
