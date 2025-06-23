import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_scatter_plot(df, team_colors):
    fig = px.scatter(
        df, 
        x='xG Difference', 
        y='Score Difference', 
        color='home_team',
        color_discrete_map=team_colors, 
        hover_data={'home_team': True, 'away_team': True, 'xG Difference': True, 'Score Difference': True},
        labels={'xG Difference': 'xG Difference (Home - Away)',
                'Score Difference': 'Score Difference (Home - Away)',
                'home_team': 'Home Team',
                'away_team': 'Away Team'},
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
