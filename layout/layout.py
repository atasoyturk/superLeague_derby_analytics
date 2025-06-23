from dash import html, dcc

def create_layout(fig, fig2, fig3, fig4, correlation, p_value, df, xg_fazla_kaybeden_result, xg_az_kazanan_result, team_colors):
    return html.Div([
        html.H1("The Importance of xG Parameter in Derbies in Trendyol Super League", style={'textAlign': 'center'}),
        dcc.Graph(id='scatter-plot', figure=fig),
        html.Div([
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P(f"Pearson Correlation: {correlation:.6f}", style={'color': 'red'}),
            html.P(f"P-value: {p_value:.6f}", style={'color': 'red'}),
            html.P(f"Average xG Prediction Error: {df['xG Prediction Error'].mean():.6f}", style={'color': 'red'}),
            html.P(
                "My goal is to analyze the performance of teams in derby matches using xG (expected goals) statistics. "
                "I will also identify teams that have performed better or worse than expected based on their xG statistics. "
                "My hypothesis is that there is no significant league-wide relationship between match scores and xG values. "
                "I use the pearson correlation coefficient to measure the strength of the linear relationship between xG and score. "
                "My pearson correlation shows that there is a weak positive correlation between xG and score, "
                "which means that it is not a good predictor of the actual score. "
                "Another insteresting point is that the P-value is too high, which means that my hypothesis cannot be rejected."
            )
        ], style={'width': '80%', 'margin': 'auto'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='trend-graph', figure=fig2),
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P(
                "This graph shows the total goals and total xGs in derby matches over time. "
                "It helps to visualize the trend of goals and xGs in derby matches. "
                "In most of matches, there is a noticeable difference between total goals and total xGs. "
                "This reinforces the idea that while xG is a valuable metric for assessing the quality of scoring opportunities,"
                "it does not always accurately predict the final outcome of a match—particularly in high-intensity games such as derbies, where emotions, pressure, and unpredictability play a larger role."
            )
        ], style={'width': '80%', 'margin': 'auto'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='xg-performance-graph', figure=fig3),
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P(
                "This chart shows the average difference between actual goals and expected goals (xG) for each team. "
                "Positive values indicate teams scoring more than expected (overperforming), while negative values indicate teams scoring less than expected (underperforming)."
                "As it seen, the teams are shows various performance through the league season in matches played betwwen themselves."
                "This supports the hypothesis that xG is not always a reliable predictor of the actual score for a single team at the same time."
            )
        ], style={'width': '80%', 'margin': 'auto', 'marginBottom': '40px'}),
        html.Hr(),
        html.Div([
            dcc.Graph(id='xg-heatmap', figure=fig4),
            html.H3("Statistical Analysis", style={'textAlign': 'left'}),
            html.P(
                "This heatmap visualizes the weekly average xG Delta for each team. "
                "The xG Delta is the difference between the expected goals (xG) and the actual score. "
                "Lighter colors represent smaller deltas (i.e., xG is closer to the actual result), "
                "while darker tones highlight weeks where xG and actual scores differ significantly. "
                "Weekly analyses, such as the xG Delta Heatmap, show that in some periods the differences between the xG and the score diminish and partial agreement is achieved."
                "This suggests that xG provides closer estimates in some weeks, but is not a reliable metric for score prediction in general."
            )
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
