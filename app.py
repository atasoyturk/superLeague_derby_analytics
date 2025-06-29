from dash import Dash
import os
from utils.data_loader import load_data, preprocess_data
from utils.stats import (
    calculate_correlation,
    calculate_xg_fazla_kaybeden,
    calculate_xg_az_kazanan,
    calculate_team_xg_performance
)
from utils.plotting import (
    create_scatter_plot,
    create_bar_plot,
    create_performance_bar_plot,
    create_heatmap
)
from layout.layout import create_layout

def create_team_colors():
    return {
        'Besiktas': 'black',
        'Fenerbahce': 'navy',
        'Galatasaray': 'red',
        'Trabzonspor': 'maroon'
    }

app = Dash(__name__)
server = app.server  # gunicorn için gerekli

# Veriyi yükle ve ön işle
df = load_data()
if df is None:
    print("Could not load data from the database.")
    # Burada hata işleme yapabilirsin, basitçe pass de
    pass

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

# Layout ataması modül seviyesinde kesin yapılmalı
app.layout = create_layout(
    fig, fig2, fig3, fig4,
    correlation, p_value, df,
    xg_fazla_kaybeden_result, xg_az_kazanan_result, team_colors
)

# __main__ altında çalıştırma, gunicorn kullanırken gerek yok
# if __name__ == '__main__':
#     app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=False)
