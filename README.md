# ⚽️  Trendyol Super League Analysis of Derby Games (2024–2025)

An in-depth statistical and visual analysis of Turkish **Süper Lig** derbies, focusing on **Expected Goals (xG)** vs actual match outcomes. This project aims to understand how well xG captures match dynamics and to highlight teams that under- or over-performed relative to their xG in the biggest clashes of the Turkish football calendar.

---

## 🎯 Purpose
Derby matches are special. They have more emotion, pressure, and unpredictability compared to regular league matches. This project analyzes:
- The correlation between **xG** and actual match results.
- Teams that have been:
    - **Better than expected** (winning despite lower xG).
    - **More dominant than results imply** (losing despite higher xG).
- Weekly variations in **xG delta** across the league.

**Research Question:**  
_"Is xG a robust predictor of match results in high-intensity derbies, or do emotions and external factors dominate?"_

---

## 🗂️ Project Architecture
The project is structured into the following components:
superLeague_derby_analytics/

├─ app.py  # Main Dash application

├─ utils/

│ └─ data_loader.py # Database connections and preprocessing

│ └─ plotting.py # Plot creation for visual analytics

│ └─ stats.py # Statistical analyses

├─ layout/

│ └─ layout.py # Dash layout design

├─ requirements.txt # Dependencies

├─ .gitignore # Exclusions

├─ README.md # Project Documentation

---


## ⚡️ Technologies & Libraries
- 🐍 **Python** (Data analysis, statistics, plotting)
- 📊 **Pandas** (Data processing)
- 📈 **Plotly/Dash** (Dynamic plotting and interactive dashboards)
- 📉 **SciPy** (Statistical testing, e.g., Pearson correlation)
- 💾 **SQLite** (Data storage)

---

## 🛠️ Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/atasoyturk/superLeague_derby_analytics.git
cd superLeague_derby_analytics
```


### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```


### 3️⃣ Run the App
```bash
python app.py
```

## 📊 Key Insights
**1. xG vs Final Score Correlation:**

The correlation is weaker than expected for derbies, implying that traditional xG metrics may not reliably predict outcomes for high-intensity matches.

**2. Over and Underperforming Teams:**

-Teams that lost despite higher xG

-Teams that won despite lower xG

**3. xG Delta Heatmap:**

Shows weekly fluctuations in the reliability of xG across the season.

## 📈 Roadmap

- 🔥 Incorporate more advanced statistical techniques (e.g., Bayesian inference).

- ⚡️ Add ML prediction pipelines.

- 🌍 Extend coverage beyond the Turkish Süper Lig.




