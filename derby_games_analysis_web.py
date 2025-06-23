import sqlite3
import pandas as pd
import os
from scipy.stats import pearsonr
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go

def load_data(db_path=r'C:\Users\User\Desktop\lectures\ceng\SQL\derby_games.db'):
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

def calculate_correlation(df):
    correlation, p_value = pearsonr(df['xG Difference'], df['Score Difference'])
    return correlation, p_value

def create_team_colors():
    return {
        'Besiktas': 'black',
        'Fenerbahce': 'navy',
        'Galatasaray': 'red',
        'Trabzonspor': 'maroon'
    }

def create_scatter_plot(df, team_colors):
    fig = px.scatter(
        df, 
        x='xG Difference', 
        y='Score Difference', 
        color='home_team',
        color_discrete_map=team_colors, 
        hover_data={
            'home_team': True,
            'away_team': True,
            'xG Difference': True,
            'Score Difference': True
        },
        labels={
            'xG Difference': 'xG Difference (Home - Away)',
            'Score Difference': 'Score Difference (Home - Away)',
            'home_team': 'Home Team',
            'away_team': 'Away Team'
        },
        title='Trendyol Super League Derby Games (2024-2025)<br>xG Difference vs Score Difference',
        template='plotly_white'
    )
    fig.update_traces(
        hovertemplate='<b>Home Team: %{customdata[0]}<br>'
                      'Away Team: %{customdata[1]}<br>'
                      'xG Difference: %{x}<br>'
                      'Score Difference: %{y}<extra></extra>',
        selector=dict(type='scatter', mode='markers')
    )
    outliers = df[df['xG Prediction Error'] > 2]
    fig.add_scatter(
        x=outliers['xG Difference'],
        y=outliers['Score Difference'],
        mode='markers+text',
        marker=dict(size=10, color='yellow', line=dict(color='black', width=2)),
        textposition='top center',
        name='Outliers (Error > 2)',
        showlegend=True
    )
    return fig

def create_bar_plot(df):
    daily_stats = df.groupby('match_date').agg({'total_goals': 'sum', 'total_xG': 'sum'}).reset_index()
    fig = px.bar(
        daily_stats, 
        x='match_date', 
        y=['total_goals', 'total_xG'],
        barmode='group',
        labels={'match_date': 'Match Date'},
        title='Trendyol Super League Derby Games (2024-2025)<br>Total xG vs Total Goals',
        template='plotly_white'
    )
    fig.for_each_trace(lambda t: t.update(name='Total Goals' if t.name == 'total_goals' else 'Total xG'))
    fig.update_traces(
        hovertemplate='<b>Match Date: %{x|%d %b %Y}</b><br>%{data.name}: %{y}<extra></extra>',
        selector=dict(type='bar')
    )
    return fig

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

def create_performance_bar_plot(team_performance, team_colors):
    fig = px.bar(
        team_performance, 
        x='team', 
        y='performance',
        color='team',
        color_discrete_map=team_colors,
        title='Trendyol Super League Derby Games (2024-2025)<br>Average Goal - xG Performance',
        labels={'performance': 'Average Goal - xG'},
        template='plotly_white'
    )
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Average Goal - xG: %{y:.2f}<extra></extra>')
    return fig

def create_heatmap(df):
    df['xG Delta'] = abs(df['xG Difference'] - df['Score Difference'])
    home_df = df[['match_week', 'home_team', 'xG Delta']].rename(columns={'home_team': 'team'})
    away_df = df[['match_week', 'away_team', 'xG Delta']].rename(columns={'away_team': 'team'})
    heatmap_df = pd.concat([home_df, away_df])
    heatmap_grouped = heatmap_df.groupby(['match_week', 'team']).mean().reset_index()
    heatmap_pivot = heatmap_grouped.pivot(index='team', columns='match_week', values='xG Delta').fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns.strftime('%d %b'),
        y=heatmap_pivot.index,
        colorscale='RdBu_r',
        colorbar=dict(title='xG Delta'),
        zmin=0,
        zmax=heatmap_pivot.values.max()
    ))
    fig.update_layout(
        title='Trendyol Super League Derby Games (2024-2025)<br>Weekly Average xG Delta',
        xaxis_title='Match Week',
        yaxis_title='Team',
        template='plotly_white'
    )
    return fig

def create_layout(fig, fig2, fig3, fig4, correlation, p_value, df, xg_fazla_kaybeden_result, xg_az_kazanan_result, team_colors):
    return html.Div([
        html.H1("The Importance of xG Parameter in Derbies in Trendyol Super League", style={'textAlign': 'center'}),
        dcc.Graph(id='scatter-plot', figure=fig),
        html.Div([
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P(f"Pearson Correlation: {correlation:.6f}", style={'color': 'red'}),
            html.P(f"P-value: {p_value:.6f}", style={'color': 'red'}),
            html.P(f"Average xG Prediction Error: {df['xG Prediction Error'].mean():.6f}", style={'color': 'red'}),
            html.P("My goal is to analyze the performance of teams in derby matches using xG (expected goals) statistics. "
                   "I will also identify teams that have performed better or worse than expected based on their xG statistics. "
                   "My hypothesis is that there is no significant league-wide relationship between match scores and xG values. "
                   "I use the pearson correlation coefficient to measure the strength of the linear relationship between xG and score. "
                   "My pearson correlation shows that there is a weak positive correlation between xG and score, "
                   "which means that it is not a good predictor of the actual score. "
                   "Another insteresting point is that the P-value is too high, which means that my hypothesis cannot be rejected.")
        ], style={'width': '80%', 'margin': 'auto'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='trend-graph', figure=fig2),
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P("This graph shows the total goals and total xGs in derby matches over time. "
                   "It helps to visualize the trend of goals and xGs in derby matches. "
                   "In most of matches, there is a noticeable difference between total goals and total xGs. "
                   "This reinforces the idea that while xG is a valuable metric for assessing the quality of scoring opportunities,"
                   "it does not always accurately predict the final outcome of a match—particularly in high-intensity games such as derbies, where emotions, pressure, and unpredictability play a larger role.")
        ], style={'width': '80%', 'margin': 'auto'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='xg-performance-graph', figure=fig3),
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P("This chart shows the average difference between actual goals and expected goals (xG) for each team. "
                   "Positive values indicate teams scoring more than expected (overperforming), while negative values indicate teams scoring less than expected (underperforming)."
                   "As it seen, the teams are shows various performance through the league season in matches played betwwen themselves."
                   "This supports the hypothesis that xG is not always a reliable predictor of the actual score for a single team at the same time.")
        ], style={'width': '80%', 'margin': 'auto', 'marginBottom': '40px'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='xg-heatmap', figure=fig4),
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P("This heatmap visualizes the weekly average xG Delta for each team. "
                   "The xG Delta is the difference between the expected goals (xG) and the actual score. "
                   "Lighter colors represent smaller deltas (i.e., xG is closer to the actual result), "
                   "while darker tones highlight weeks where xG and actual scores differ significantly. "
                   "Weekly analyses, such as the xG Delta Heatmap, show that in some periods the differences between the xG and the score diminish and partial agreement is achieved."
                   "This suggests that xG provides closer estimates in some weeks, but is not a reliable metric for score prediction in general.")
        ], style={'width': '90%', 'margin': 'auto', 'marginBottom': '40px'}),
        html.Hr(),
        html.Div([
            html.H2("Remarkable Statistics in Derbies in The Turkish Super League", style={'textAlign': 'center', 'marginTop': '40px', 'color': '#333'}),
            html.Div([
                html.P("Team with more xG than their opponent but lost the most matches", className='stat-title'),
                html.P(
                    xg_fazla_kaybeden_result["text"],
                    className=f'stat-result {xg_fazla_kaybeden_result["team"].lower() if xg_fazla_kaybeden_result["team"] else ""}',
                    style={'backgroundColor': team_colors.get(xg_fazla_kaybeden_result["team"], '#e0e0e0')}
                )
            ], className='stat-box'),
            html.Div([
                html.P("Team with less xG than their opponent but won the most matches", className='stat-title'),
                html.P(
                    xg_az_kazanan_result["text"],
                    className=f'stat-result {xg_az_kazanan_result["team"].lower() if xg_az_kazanan_result["team"] else ""}',
                    style={'backgroundColor': team_colors.get(xg_az_kazanan_result["team"], '#e0e0e0')}
                )
            ], className='stat-box')
        ], style={'width': '80%', 'margin': 'auto', 'textAlign': 'center', 'marginTop': '40px', 'marginBottom': '40px'})
    ])

def main():
    df = load_data()
    if df is None:
        print("Could not load data from the database.")
        return
    
    df = preprocess_data(df)
    team_colors = create_team_colors()
    correlation, p_value = calculate_correlation(df)
    
    fig = create_scatter_plot(df, team_colors)
    fig2 = create_bar_plot(df)
    team_performance = calculate_team_xg_performance(df)
    fig3 = create_performance_bar_plot(team_performance, team_colors)
    fig4 = create_heatmap(df)
    
    xg_fazla_kaybeden_result = calculate_xg_fazla_kaybeden(df)
    xg_az_kazanan_result = calculate_xg_az_kazanan(df)
    
    app = Dash(__name__)
    app.layout = create_layout(
        fig, fig2, fig3, fig4, 
        correlation, p_value, df, 
        xg_fazla_kaybeden_result, xg_az_kazanan_result, team_colors
    )
    
    app.run(debug=True)

if __name__ == '__main__':
    main()