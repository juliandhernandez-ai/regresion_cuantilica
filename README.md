# Regresión cuantilica

Proyecto para explorar modelos de regresión cuantilica con Python y R.

## Estructura del proyecto

- `apps/`: aplicaciones y scripts funcionales del proyecto.
- `data/`: datos crudos y procesados.
- `docs/`: documentación, material académico, imágenes y archivos LaTeX/PDF.
- `notebooks/`: notebooks de exploración y análisis.
- `src/`: código reutilizable del proyecto organizado por módulos.
- `results/`: salidas, figuras y reportes generados.
- `tests/`: pruebas unitarias e integración.
- `requirements.txt`: dependencias del entorno Python.

## Organización sugerida

```text
regresion_cuantilica/
├── apps/
│   ├── scripts/
│   ├── streamlit/
│   └── pages/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── latex/
│   ├── references/
│   └── images/
├── notebooks/
│   ├── exploratory/
│   └── reports/
├── src/
│   ├── preprocessing/
│   ├── modeling/
│   ├── evaluation/
│   └── visualization/
├── results/
│   ├── figures/
│   ├── models/
│   └── reports/
├── tests/
│   ├── unit/
│   └── integration/
├── README.md
├── requirements.txt
└── .gitignore
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar notebooks de análisis, se recomienda mantenerlos en `notebooks/exploratory/` y los scripts funcionales en `apps/scripts/`.

Para ejecutar `notebooks/exploratory/modelo_R.ipynb`, instala R y el paquete `IRkernel` para que VS Code pueda seleccionar el kernel R.