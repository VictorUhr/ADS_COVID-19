# ADS_COVID-19

This repository contains the final deliverables for an Applied Data Science project focused on COVID-19 data analysis. The work includes data preparation, exploratory analysis, and presentation of results through notebooks and Python scripts.

## Project overview

The project uses public COVID-19 datasets to explore patterns in infections and vaccination-related information. The workflow is organized around reproducible data processing steps and analysis notebooks.

## Deliverables

- Delivery 3: [Notebook walkthrough](https://github.com/VictorUhr/ADS_COVID-19/blob/main/notebooks/0.%20Source%20code_Walkthrough_Delivery3.ipynb)
- Delivery 4: [Notebook walkthrough](https://github.com/VictorUhr/ADS_COVID-19/blob/main/notebooks/0.%20Source%20code_Walkthrough_Delivery4.ipynb)
- Source code: [Project source folder](https://github.com/VictorUhr/ADS_COVID-19/tree/main/src)

## Repository structure

```text
├── LICENSE
├── Makefile
├── README.md
├── data/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── docs/
├── notebooks/
├── reports/
├── requirements.txt
├── setup.py
├── src/
└── tox.ini
```

## Getting started

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Open the notebooks in the `notebooks/` directory or run the scripts in `src/`.

## Notes

This project follows the structure of the Cookiecutter Data Science template and is intended to support reproducible analysis and documentation.

---

<small>Project based on the <a href="https://drivendata.github.io/cookiecutter-data-science/" target="_blank">Cookiecutter Data Science project template</a>.</small>
