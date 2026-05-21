# Reportes Automáticos Nubyx

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/UI_Toolkit-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/CLI_Engine-Rich-orange?style=for-the-badge" alt="Rich Engine">
  <img src="https://img.shields.io/badge/Render_Engine-ReportLab-red?style=for-the-badge" alt="ReportLab Engine">
  <img src="https://img.shields.io/badge/Environment-Fedora%20Linux-3C6EB4?style=for-the-badge&logo=fedora&logoColor=white" alt="Fedora OS">
</p>

---

## 📋 Descripción del Sistema

Sistema automatizado de nivel industrial desarrollado para la captura interactiva de datos de hardware en control de calidad técnico. El software resuelve de forma directa la persistencia estructurada de registros mediante una base de datos distribuida en formato plano (CSV) y cuenta con un **motor automatizado de renderizado de informes homologados en formato PDF pixel-perfect**, asegurando un alineamiento exacto con las grillas impresas corporativas.

El sistema expone dos interfaces totalmente funcionales y autocontenidas que comparten el mismo núcleo lógico:

1. **Interactive CLI Engine (`main.py`)**: Diseñado con un enfoque ágil y optimizado para teclado mediante cuadros visuales interactivos y formateo enriquecido a través de la terminal.
2. **Desktop GUI Application (`gui.py`)**: Desarrollado bajo la arquitectura clásica de Qt utilizando layouts dinámicos y un sistema predictivo de autocompletado inteligente de registros históricos.

---

## 🛠️ Arquitectura y Stack Tecnológico

El proyecto está diseñado bajo un principio de desacoplamiento modular estricto:

- **Core Engine (`generador_pdf.py`)**: Abstrae toda la lógica de construcción de tablas, asignación dinámica de altura de celdas para prevenir el solapamiento de strings complejos y estilización cromática.
- **Persistencia Integrada (CSV)**: Implementa una lógica de lectura/escritura atómica que mapea, actualiza u organiza de forma dinámica las diferentes etapas del protocolo técnica de un equipo basándose exclusivamente en su clave primaria única (`serie`).

### Componentes Utilizados

- **Python 3.14**: Últimas directivas de tipado, concatenación atómica de diccionarios `**kwargs` y manejo nativo de flujos I/O.
- **PyQt6 (Qt6 Toolkit)**: Sistema robusto de componentes gráficos y delegación de eventos en tiempo real.
- **ReportLab**: Renderizado de primitivas gráficas vectoriales a bajo nivel para empaquetado PDF compacto.
- **Rich**: Formateo avanzado de flujo ANSI en consola y renderizado de layouts en terminal de alta fidelidad.

---

## ⚙️ Configuración del Entorno Local

El despliegue está completamente automatizado y no requiere de llaves de escritura ni de autenticaciones externas para entornos de prueba.

### 1. Clonar el Repositorio

```bash
git clone [https://github.com/MarcosBernardC/reportes_automaticos_nubyx.git](https://github.com/MarcosBernardC/reportes_automaticos_nubyx.git)
cd reportes_automaticos_nubyx
```

### 2. Creación y Activación del Entorno Virtual Isolado

Para garantizar que el software corra sin conflictos de dependencias con paquetes globales del sistema, inicializa un entorno de pruebas (`venv`):

- **En entornos Fish Shell:**

  Fragmento de código

  ```
  python -m venv test_env
  source test_env/bin/activate.fish
  ```

- **En entornos Bash / Zsh estándar:**

  Bash

  ```
  python -m venv test_env
  source test_env/bin/activate
  ```

### 3. Instalación de Dependencias del Sistema

Actualiza el gestor e instala el set completo de bibliotecas empaquetadas en un solo comando:

Bash

```
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Modos de Ejecución

Una vez completado el proceso de instalación, puedes arrancar el núcleo del software bajo cualquiera de sus dos modalidades disponibles:

### Modo Terminal Interactiva (TUI / CLI)

Ideal para entornos remotos de infraestructura o ingenieros que priorizan la velocidad operativa del teclado:

Bash

```
python main.py
```

### Modo Aplicación de Escritorio (GUI)

Interfaz gráfica intuitiva basada en Qt con layouts auto-ajustables y soporte de autocompletado predictivo:

Bash

```
python gui.py
```

## 📈 Historial de Cambios e Infraestructura (Git Standards)

El desarrollo del proyecto se rige bajo especificaciones estrictas de calidad de software:

- **Commits Atómicos**: Los cambios de dependencias, las correcciones y las actualizaciones de metadatos se registran de manera independiente e inequívoca.
- **Conventional Commits**: Historial de control de versiones legible por máquinas y humanos (`feat:`, `fix:`, `docs:`, `chore:`).
- **Integración en Ecosistema**: Automatizado mediante orquestadores de metadatos locales para la actualización síncrona inmediata en portafolios técnicos en producción.
