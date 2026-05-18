# IPL Win Predictor

A simple machine-learning web app and notebook to predict the winner of Indian Premier League (IPL) matches.

**Project structure**
- `app.py` — main application (Flask/WSGI entrypoint)
- `IPL Win Predictor.ipynb` — exploratory notebook and model development
- `requirements.txt` — Python dependencies
- `Procfile` / `runtime.txt` — deployment configuration (Heroku)

**Features**
- Predict match outcomes using historical IPL data
- Lightweight Flask app for serving predictions
- Jupyter notebook for experiments and model improvements
-
**Data**
- Kaggle IPL dataset: https://www.kaggle.com/datasets/ramjidoolla/ipl-data-set

**Prerequisites**
- Python 3.8+ (see `runtime.txt`)
- pip

**Install**

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

**Run locally**

```bash
python app.py
```

Open the notebook to explore the data and model: `IPL Win Predictor.ipynb`.

**Deployment**

This repo includes `Procfile` and `runtime.txt` for easy deployment to platforms like Heroku. Ensure `requirements.txt` lists all runtime packages.

**Usage**
- Start the web app and visit the local URL (printed by `app.py`) to interact with the predictor.
- Use the notebook to retrain or evaluate models; export updated artifacts to the app's expected model path.

**Contributing**
- Feel free to open issues or PRs. Add tests and update the notebook or `app.py` as needed.


