from scipy.stats import pearsonr
import pandas as pd

def calculate_correlation(df):
    correlation, p_value = pearsonr(df['xG Difference'], df['Score Difference'])
    return correlation, p_value

def calculate_xg_fazla_kaybeden(df):
    kaybedenler = []
    for _, row in df.iterrows():
        if row['xG_home'] > row['xG_away'] and row['home_score'] < row['away_score']:
            kaybedenler.append(row['home_team'])
        elif row['xG_away'] > row['xG_home'] and row['away_score'] < row['home_score']:
            kaybedenler.append(row['away_team'])
    if not kaybedenler:
        return {"text": "No team was found that met these criteria.", "team": None}
    series = pd.Series(kaybedenler)
    team = series.value_counts().idxmax()
    count = series.value_counts().max()
    return {"text": f"{team} ({count} matches)", "team": team}

def calculate_xg_az_kazanan(df):
    kazananlar = []
    for _, row in df.iterrows():
        if row['xG_home'] < row['xG_away'] and row['home_score'] > row['away_score']:
            kazananlar.append(row['home_team'])
        elif row['xG_away'] < row['xG_home'] and row['away_score'] > row['home_score']:
            kazananlar.append(row['away_team'])
    if not kazananlar:
        return {"text": "No team was found that met these criteria.", "team": None}
    series = pd.Series(kazananlar)
    team = series.value_counts().idxmax()
    count = series.value_counts().max()
    return {"text": f"{team} ({count} matches)", "team": team}

def calculate_team_xg_performance(df):
    perf_rows = []
    for _, row in df.iterrows():
        perf_rows.append({'team': row['home_team'], 'performance': row['home_score'] - row['xG_home']})
        perf_rows.append({'team': row['away_team'], 'performance': row['away_score'] - row['xG_away']})
    perf_df = pd.DataFrame(perf_rows)
    team_avg_perf = perf_df.groupby('team')['performance'].mean().reset_index()
    return team_avg_perf
