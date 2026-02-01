[Home](./) | [Statistical tables](statistical-tables) | [Datasets](datasets) | [SQL & syntaxes](sql-and-syntaxes) | [Data dictionary](data-dictionary) | [Reproducibility](reproducibility)


# Reproducibility

Everything needed to regenerate the statistical tables and visuals is included in this repo.

1. Open `notebooks/analysis.ipynb` in Jupyter, or run `scripts/analysis.py`.
2. The script reads `data/healthcare_data.csv`.
3. Outputs are written to `stats/` and plots are written to `docs/assets/img/`.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate # Windows (PowerShell)

pip install -r requirements.txt
python scripts/analysis.py
```
