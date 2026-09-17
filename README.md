# Regresión Cuantílica: De la media a toda la distribución

**Autor:** Julián David Hernández Grisales

## 📖 Descripción del Proyecto

Este proyecto explora la **Regresión Cuantílica** como una alternativa robusta y flexible a la regresión lineal clásica (Mínimos Cuadrados Ordinarios - MCO). Mientras que la regresión clásica se centra únicamente en modelar la **media condicional** \(E(Y|X)\), la regresión cuantílica permite modelar diferentes puntos (cuantiles) de la distribución condicional de la variable respuesta \(Y\), ofreciendo una visión más completa de la relación entre las variables.

A través de este repositorio, se aborda desde la motivación histórica (Koenker & Bassett, 1978) y los fundamentos matemáticos (función de pérdida *pinball*), hasta la implementación práctica y la interpretación de resultados en diferentes áreas como economía, salud y marketing.

## 📂 Estructura del Proyecto

```text
regresion_cuantilica/
├── .venv/                     # Entorno virtual de Python
├── aplicaciones/              # Scripts de aplicaciones prácticas
│   └── aplicacion_1.py
├── data/                      # Datos del proyecto
│   ├── raw/                   # Datos crudos (advertising.csv, india.csv, natality.csv, etc.)
│   └── processed/             # Datos procesados y listos para modelar
├── documentacion/             # Documentación teórica y papers
│   ├── cuantilica_Q.pdf
│   ├── Documentación_Q.pdf
│   └── Quantile regression...pdf
├── imagenes/                  # Recursos gráficos para el notebook y presentaciones
├── notebooks/                 # Jupyter Notebooks
│   ├── modelo_R.ipynb         # Implementación en R
│   └── regresion_cuantilica.ipynb # Cuaderno principal (teoría y ejemplos)
├── README.md                  # Este archivo
└── requirements.txt           # Dependencias del proyecto (Python)