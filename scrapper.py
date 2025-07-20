#Importation des librairies
from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd
import streamlit as st

def villas():
    """
    Récupère les données de la catégorie villas sur Coin Afrique.
    Utilise un widget Streamlit pour demander le nombre de pages à parcourir.
    Retourne:
    pd.DataFrame: DataFrame contenant les données extraites.
    """
    x = st.number_input("Saisir le nombre de pages à parcourir et appuyer sur entrer", min_value=1, value=1, step=1)
    data = []
    for p in range(1, x+1):  
        url = f'https://sn.coinafrique.com/categorie/villas?page={p}'
        code_html = get(url)
        soup = bs(code_html.content, 'html.parser')
        containers = soup.find_all('div', class_ = 'col s6 m4 l3')
        for container in containers:
            try:
                url_container =  'https://sn.coinafrique.com' + container.a['href']
                hc_container = get(url_container)
                soup_container = bs(hc_container.content, 'html.parser')
                type_annonce  = soup_container.find('h1',class_ ='title title-ad hide-on-large-and-down').text.strip()  
                nombre_piece = soup_container.find('span', class_ = 'qt').text.strip()
                prix = soup_container.find('p', class_ = 'price').text.strip()
                adresse = soup_container.find('span', attrs={'data-address': True}).text.strip()
                image_lien = soup_container.img['src']
            except Exception:
                continue    
            type_annonce=type_annonce.split()[0]
            prix = ''.join([c for c in prix if c.isdigit()])
            if not prix:
                prix = 'non disponible'
            data.append({
                'type annonce (vente ou location)': type_annonce,
                'nombre  pièces': nombre_piece,
                'prix (FCFA)': prix,
                'adresse': adresse,
                'image_lien': image_lien
                })     
    df = pd.DataFrame(data)
    return df


def terrains():
    """
    Récupère les données de la catégorie terrains sur Coin Afrique.
    Utilise un widget Streamlit pour demander le nombre de pages à parcourir.
    Retourne:
    pd.DataFrame: DataFrame contenant les données extraites.
    """
    x = st.number_input("Saisir le nombre de pages à parcourir et appuyer sur entrer", min_value=1, value=1, step=1)
    data = []
    for p in range(1, x+1):  
        url = f'https://sn.coinafrique.com/categorie/terrains?page={p}'
        code_html = get(url)
        soup = bs(code_html.content, 'html.parser')
        containers = soup.find_all('div', class_ = 'col s6 m4 l3')
        for container in containers:
            try:
                url_container =  'https://sn.coinafrique.com' + container.a['href']
                hc_container = get(url_container)
                soup_container = bs(hc_container.content, 'html.parser')
                superficie  = soup_container.find('span', class_ = 'qt').text.strip()  
                prix = soup_container.find('p', class_ = 'price').text.strip()
                adresse = soup_container.find('span', attrs={'data-address': True}).text.strip()
                image_lien = soup_container.img['src']            
            except Exception:
                continue    
            superficie = superficie.replace('m2', '').replace(' ', '')
            if not superficie:
                superficie = 'non disponible'
            prix = ''.join([c for c in prix if c.isdigit()])
            if not prix:
                prix = 'non disponible'
            data.append({
                'superficie (m2)': superficie,
                'prix (FCFA)': prix,
                'adresse': adresse,
                'image_lien': image_lien
                })     
    df = pd.DataFrame(data)
    return df


def appartements():
    """
    Récupère les données de la catégorie appartements sur Coin Afrique.
    Utilise un widget Streamlit pour demander le nombre de pages à parcourir.
    Retourne:
    pd.DataFrame: DataFrame contenant les données extraites.
    """
    x = st.number_input("Saisir le nombre de pages à parcourir et appuyer sur entrer", min_value=1, value=1, step=1)
    data = []
    for p in range(1, x+1):  
        url = f'https://sn.coinafrique.com/categorie/villas?appartements={p}'
        code_html = get(url)
        soup = bs(code_html.content, 'html.parser')
        containers = soup.find_all('div', class_ = 'col s6 m4 l3')
        for container in containers:
            try:
                url_container =  'https://sn.coinafrique.com' + container.a['href']
                hc_container = get(url_container)
                soup_container = bs(hc_container.content, 'html.parser')
                type_annonce  = soup_container.find('h1',class_ ='title title-ad hide-on-large-and-down').text.strip()  
                nombre_piece = soup_container.find('span', class_ = 'qt').text.strip()
                prix = soup_container.find('p', class_ = 'price').text.strip()
                adresse = soup_container.find('span', attrs={'data-address': True}).text.strip()
                image_lien = soup_container.img['src']
            except Exception:
                continue    
            prix = ''.join([c for c in prix if c.isdigit()])
            if not prix:
                prix = 'non disponible'
            data.append({
                'nombre  pièces': nombre_piece,
                'prix (FCFA)': prix,
                'adresse': adresse,
                'image_lien': image_lien
                })     
    df = pd.DataFrame(data)
    return df