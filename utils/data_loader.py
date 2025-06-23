import sqlite3
import pandas as pd
import os

def load_data(db_path=r"C:\Users\User\Desktop\lectures\superLeauge_derby_analytics\data\derby_games.db"):
    try:
        print(f"Connecting to database at: {os.path.abspath(db_path)}")
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM match_stats", conn)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()
    return df

def preprocess_data(df):
    df['xG Difference'] = df['xG_home'] - df['xG_away']
    df['Score Difference'] = df['home_score'] - df['away_score']
    df['xG Prediction Error'] = abs(df['xG Difference'] - df['Score Difference'])
    df['match_date'] = pd.to_datetime(df['match_date'])
    df['total_goals'] = df['home_score'] + df['away_score']
    df['total_xG'] = df['xG_home'] + df['xG_away']
    df['match_week'] = df['match_date'].dt.to_period('W').apply(lambda r: r.start_time)
    return df
