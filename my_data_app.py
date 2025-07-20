import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import subprocess
import time
import scrapper as scr
from ydata-profiling import ProfileReport

# Header section
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: black;'>Viwossin DEGBOE DATA APP</h1>
        <p>
            Cette application est conçue dans le cadre de l'examen de Data Collection, Master 1 IA - G2.<br>
            Elle scrappe des données du site <a href='https://sn.coinafrique.com' target='_blank'>Coin Afrique</a> concernant les:<br>
            <b><a href='https://sn.coinafrique.com/categorie/villas' target='_blank'>Villas</a></b>, 
            <b><a href='https://sn.coinafrique.com/categorie/appartements' target='_blank'>Appartements</a></b> et 
            <b><a href='https://sn.coinafrique.com/categorie/terrains' target='_blank'>Terrains</a></b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


menu = st.sidebar.radio("Menu", ["Scrapper avec pages", "Télécharger des données", "Dashboard", "Votre avis compte"])
st.markdown("""
    <style>
    .css-1v0mbdj .e1fqkh3o3 { justify-content: center; }
    </style>
""", unsafe_allow_html=True)

if menu == "Scrapper avec pages":
    st.markdown("""
        <div style='text-align: center;'>
        <h2 style='color: black;'>Scrapping de plusieurs pages avec BeautifullSoup.</h2>
        </div>
        """,unsafe_allow_html=True)
    
    if st.button("Lancer le scrapping des Villas"):
        villas_df = scr.villas()
        if villas_df is not None and not villas_df.empty:
            st.subheader("Résultats des Villas")
            st.dataframe(villas_df)
        else:
            st.info("Aucune donnée de villas n'a été trouvée.")

    if st.button("Lancer le scrapping des Appartements"):
        appartements_df = scr.appartements()
        if appartements_df is not None and not appartements_df.empty:
            st.subheader("Résultats des Appartements")
            st.dataframe(appartements_df)
        else:
            st.info("Aucune donnée d'appartements n'a été trouvée.")

    if st.button("Lancer le scrapping des Terrains"):
        Terrains_df = scr.terrains()
        if Terrains_df is not None and not Terrains_df.empty:
            st.subheader("Résultats des Terrains")
            st.dataframe(Terrains_df)
        else:
            st.info("Aucune donnée de terrains n'a été trouvée.")

elif menu == "Télécharger des données":
    
    st.markdown("""
    <div style='text-align: center;'>
    <h2 style='color: black;'>Téléchargement de données scrappées avec Web Scrapper.</h2>
    </div>
    """,unsafe_allow_html=True) 

    # Fonction de loading des données
    def load_(dataframe, title, key):
        st.markdown("""
        <style>
        div.stButton {text-align:center}
        </style>""", unsafe_allow_html=True)

        if st.button(title, key):
            st.subheader('Display data dimension')
            st.write('DDimension des données: ' + str(dataframe.shape[0]) + ' lignes et ' + str(dataframe.shape[1]) + ' colonnes.')
            st.dataframe(dataframe)

    # définir quelques styles liés aux box
    st.markdown('''<style> .stButton>button {
        font-size: 12px;
        height: 3em;
        width: 25em;
    }</style>''', unsafe_allow_html=True)

    # Charger les données 
    load_(pd.read_csv('data/Villas.csv'), 'Données de villas', '1')
    load_(pd.read_csv('data/Appartements.csv'), "Données d'appartements", '2')
    load_(pd.read_csv('data/Terrains.csv'), 'Données de terrains', '3')

elif menu == "Dashboard":
    st.markdown("""
    <style>
    .css-1v0mbdj .e1fqkh3o3 { justify-content: center; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Dashboard</h2>", unsafe_allow_html=True)
    
    
        # Définition des datasets
    def load_data(type_bien):
        if type_bien == "Villas":
            return pd.read_csv('data/Villas.csv')
        elif type_bien == "Terrains":
            return pd.read_csv('data/Terrains.csv')
        elif type_bien == "Appartements":
            return pd.read_csv('data/Appartements.csv')
    # Onglets Streamlit
    tabs = st.tabs(["Villas", "Terrains", "Appartements"])

    # Pour chaque onglet, charge les données, génère et affiche le rapport
    for i, tab_name in enumerate(["Villas", "Terrains", "Appartements"]):
        with tabs[i]:
            st.header(f"Dashboard - {tab_name}")
            df = load_data(tab_name)

            with st.spinner("Génération du rapport..."):
                profile = ProfileReport(df, explorative=True, minimal=True)
                profile_html = profile.to_html()

            components.html(profile_html, height=1000, scrolling=True)



elif menu == "Votre avis compte":
    st.markdown("<h2 style='text-align: center; color: black;'>Votre avis compte</h2>", unsafe_allow_html=True)
    st.write("Nous apprécions vos retours. Veuillez remplir le formulaire ci-dessous :")
    
    st.components.v1.html(
    '<iframe src="https://ee-eu.kobotoolbox.org/q1WMnNot" width="100%" height="1500" frameborder="0"></iframe>'
    ,height=1000, scrolling=True
)









 


