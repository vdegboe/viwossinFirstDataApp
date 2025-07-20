import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Charger les données
df = pd.read_csv('data/Appartements.csv')

# Nettoyage des données
# Extraire la ville de la colonne 'adresse'
df['ville'] = df['adresse'].str.split(',').str[0].str.strip()

# Nettoyer la colonne 'superficie (m2)'
df['superficie (m2)'] = df['superficie (m2)'].str.replace(' m2', '', regex=False)
df['superficie (m2)'] = pd.to_numeric(df['superficie (m2)'], errors='coerce')

# Nettoyer la colonne 'nombre pièces'
df['nombre pièces'] = pd.to_numeric(df['nombre pièces'], errors='coerce')

# Supprimer les lignes avec des valeurs manquantes dans 'superficie (m2)' ou 'nombre pièces'
df_clean = df.dropna(subset=['superficie (m2)', 'nombre pièces'])

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Layout du dashboard
app.layout = html.Div([
    html.H1('Dashboard Interactif des Appartements au Sénégal', style={'textAlign': 'center', 'margin': '20px'}),
    
    # Filtre pour la ville
    html.Div([
        html.Label('Sélectionner une ville :'),
        dcc.Dropdown(
            id='ville-filter',
            options=[{'label': ville, 'value': ville} for ville in sorted(df_clean['ville'].unique())],
            value=None,
            placeholder='Toutes les villes',
            style={'width': '50%', 'margin': '10px auto'}
        ),
    ], style={'textAlign': 'center'}),
    
    # Graphique de dispersion
    html.Div([
        dcc.Graph(id='scatter-plot')
    ], style={'margin': '20px'}),
    
    # Histogramme
    html.Div([
        dcc.Graph(id='histogram')
    ], style={'margin': '20px'}),
    
    # Table des données
    html.Div([
        html.H3('Détails des Appartements', style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='table',
            columns=[
                {'name': 'ID', 'id': 'web-scraper-order'},
                {'name': 'Titre', 'id': 'container'},
                {'name': 'Ville', 'id': 'ville'},
                {'name': 'Superficie (m²)', 'id': 'superficie (m2)'},
                {'name': 'Nombre de Pièces', 'id': 'nombre pièces'},
                {'name': 'Nombre de Salles de Bain', 'id': 'nombre salle bain'},
                {'name': 'Adresse', 'id': 'adresse'},
                {'name': 'Lien', 'id': 'container-href', 'type': 'text', 'presentation': 'markdown'}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            page_size=10
        )
    ], style={'margin': '20px'})
])

# Callback pour mettre à jour les graphiques et la table
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('histogram', 'figure'),
     Output('table', 'data')],
    [Input('ville-filter', 'value')]
)
def update_dashboard(selected_ville):
    # Filtrer les données selon la ville sélectionnée
    filtered_df = df_clean if selected_ville is None else df_clean[df_clean['ville'] == selected_ville]
    
    # Graphique de dispersion : Superficie vs Nombre de pièces
    scatter_fig = px.scatter(
        filtered_df,
        x='superficie (m2)',
        y='nombre pièces',
        color='ville',
        hover_data=['container', 'adresse'],
        title='Superficie vs Nombre de Pièces des Appartements',
        labels={'superficie (m2)': 'Superficie (m²)', 'nombre pièces': 'Nombre de Pièces'}
    )
    scatter_fig.update_layout(title_x=0.5)
    
    # Histogramme : Distribution du nombre de pièces
    hist_fig = px.histogram(
        filtered_df,
        x='nombre pièces',
        nbins=20,
        title='Distribution du Nombre de Pièces',
        labels={'nombre pièces': 'Nombre de Pièces'}
    )
    hist_fig.update_layout(title_x=0.5)
    
    # Données pour la table
    table_data = filtered_df[['web-scraper-order', 'container', 'ville', 'superficie (m2)', 
                             'nombre pièces', 'nombre salle bain', 'adresse', 'container-href']].to_dict('records')
    # Formatter les liens pour la table
    for row in table_data:
        row['container-href'] = f"[Lien]({row['container-href']})"
    
    return scatter_fig, hist_fig, table_data

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)