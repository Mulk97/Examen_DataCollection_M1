import streamlit as st
import pandas as pd
import sqlite3
from requests import get
from bs4 import BeautifulSoup as bs
from sqlalchemy import text # Import indispensable pour SQLAlchemy
import streamlit as st
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="AnimauxCoin App", layout="wide")

# Connexion SQL via Streamlit
conn = st.connection('sqlite', type='sql')


# --- MENU LATÉRAL ---
menu = ["🏠 Accueil", "🌐 Scraping Direct With BeautifulSoup", "📁 Import Web Scraper", "📊 Dashboard", "📝 Évaluation"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- SECTION 1 : ACCUEIL ---
if choice == "🏠 Accueil":
    st.title("Bienvenue sur AnimauxCoin App")
    st.write("Cette application permet de gérer et visualiser les données du marché animalier.")

# --- SECTION 2 : SCRAPING (Plusieurs pages) ---
elif choice == "🌐 Scraping Direct With BeautifulSoup":
    st.title("Scraper de nouvelles données")


    # Liste de vos 4 choix
    liste_animaux = ["Chien", "Mouton", "Poules Lapins et Pigeons", "Autres animaux"]
    
    animal_choisi = st.selectbox(
        "Quel type de catégorie souhaitez-vous scraper ?",
        options=liste_animaux,
        index=0  # Par défaut, le premier de la liste (Chien)
    )
    

    
    st.write(f"🔎 Préparation du scraping pour les : **{animal_choisi}**")
    
    # --- Utilisation dans votre base SQL ---
    # On enlève l'émoji pour faire la requête SQL proprement
    nom_pur = animal_choisi.lower() 
  
    # if st.button("Lancer la recherche"):
        # Exemple de requête filtrée sur votre choix
        # st.info(f"Connexion à la base pour chercher des {nom_pur}...")
        

# =============================================================================
    if animal_choisi == "Chien":
        pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=10, value=1)
        
        if st.button("Lancer le Scraping"):
            st.info(f"Début du scraping pour {animal_choisi}...")
            
            # 1. S'assurer que la table existe
            with conn.session as s:
                s.execute(text("CREATE TABLE IF NOT EXISTS Chien (nom TEXT, prix TEXT, adresse TEXT, image_lien TEXT)"))
                s.commit()
    
            for index_page in range(1, pages + 1):
                st.write(f"Scraping de la page {index_page}...")
                url1 = f'https://sn.coinafrique.com/categorie/chiens?page={index_page}'
                res = get(url1)
                soup = bs(res.content, 'html.parser')
                containers = soup.find_all('div','col s6 m4 l3')
                
                for container in containers:
                    try:
                        nom = container.find('p','ad__card-description').a.text.strip()
                        prix = container.find('p','ad__card-price').a.text.strip()
                        adresse = container.find('p','ad__card-location').span.text.strip()
                        image_lien = container.find('img','ad__card-img')['src']
            
                        # 2. Utiliser la syntaxe text() et les paramètres nommés (plus robuste)
                        with conn.session as s:
                            s.execute(
                                text("INSERT INTO Chien (nom, prix, adresse, image_lien) VALUES (:n, :p, :a, :i)"),
                                {"n": nom, "p": prix, "a": adresse, "i": image_lien}
                            )
                            s.commit()
                    except Exception as e:
                        # On affiche l'erreur si l'extraction d'une ligne échoue
                        st.warning(f"Erreur sur une ligne : {e}")
    
            st.success("✅ Scraping terminé et données enregistrées !")
    
            # 3. AFFICHAGE IMMÉDIAT
            st.subheader("📋 Contenu actuel de la table Chien")
            df_chien = conn.query("SELECT * FROM Chien")
            
            if not df_chien.empty:
                st.dataframe(
                    df_chien, 
                    column_config={"image_lien": st.column_config.ImageColumn("Photo")},
                    use_container_width=True
                )
            else:
                st.error("La table est vide malgré le scraping. Vérifiez les balises HTML.")


# ======================================================


    elif animal_choisi == "Mouton":
        pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=10, value=1)
        
        if st.button("Lancer le Scraping"):
            st.info(f"Début du scraping pour {animal_choisi}...")
            
            # 1. S'assurer que la table existe
            with conn.session as s:
                s.execute(text("CREATE TABLE IF NOT EXISTS Mouton (nom TEXT, prix TEXT, adresse TEXT, image_lien TEXT)"))
                s.commit()
    
            for index_page in range(1, pages + 1):
                st.write(f"Scraping de la page {index_page}...")
                url2 = f'https://sn.coinafrique.com/categorie/moutons?page={index_page}'
                res = get(url2)
                soup = bs(res.content, 'html.parser')
                containers = soup.find_all('div','col s6 m4 l3')
                
                for container in containers:
                    try:
                        nom = container.find('p','ad__card-description').a.text.strip()
                        prix = container.find('p','ad__card-price').a.text.strip()
                        adresse = container.find('p','ad__card-location').span.text.strip()
                        image_lien = container.find('img','ad__card-img')['src']
            
                        # 2. Utiliser la syntaxe text() et les paramètres nommés (plus robuste)
                        with conn.session as s:
                            s.execute(
                                text("INSERT INTO Mouton (nom, prix, adresse, image_lien) VALUES (:n, :p, :a, :i)"),
                                {"n": nom, "p": prix, "a": adresse, "i": image_lien}
                            )
                            s.commit()
                    except Exception as e:
                        # On affiche l'erreur si l'extraction d'une ligne échoue
                        st.warning(f"Erreur sur une ligne : {e}")
    
            st.success("✅ Scraping terminé et données enregistrées !")
        
            # 3. AFFICHAGE IMMÉDIAT
            st.subheader("📋 Contenu actuel de la table Mouton")
            df_mouton = conn.query("SELECT * FROM Mouton")
            
            if not df_mouton.empty:
                st.dataframe(
                    df_mouton, 
                    column_config={"image_lien": st.column_config.ImageColumn("Photo")},
                    use_container_width=True
                )
            else:
                st.error("La table est vide malgré le scraping. Vérifiez les balises HTML.")

# ======================================================

    elif animal_choisi == "Poules Lapins et Pigeons":
        pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=10, value=1)
        
        if st.button("Lancer le Scraping"):
            st.info(f"Début du scraping pour {animal_choisi}...")
            
            # 1. S'assurer que la table existe
            with conn.session as s:
                s.execute(text("CREATE TABLE IF NOT EXISTS PouLaPi (details TEXT, prix TEXT, adresse TEXT, image_lien TEXT)"))
                s.commit()
    
            for index_page in range(1, pages + 1):
                st.write(f"Scraping de la page {index_page}...")
                url3 = f'https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons?page={index_page}'
                res = get(url3)
                soup = bs(res.content, 'html.parser')
                containers = soup.find_all('div','col s6 m4 l3')
                
                for container in containers:
                    try:
                        details = container.find('p','ad__card-description').a.text.strip()
                        prix = container.find('p','ad__card-price').a.text.strip()
                        adresse = container.find('p','ad__card-location').span.text.strip()
                        image_lien = container.find('img','ad__card-img')['src']
            
                        # 2. Utiliser la syntaxe text() et les paramètres nommés (plus robuste)
                        with conn.session as s:
                            s.execute(
                                text("INSERT INTO PouLaPi (details, prix, adresse, image_lien) VALUES (:d, :p, :a, :i)"),
                                {"d": details, "p": prix, "a": adresse, "i": image_lien}
                            )
                            s.commit()
                    except Exception as e:
                        # On affiche l'erreur si l'extraction d'une ligne échoue
                        st.warning(f"Erreur sur une ligne : {e}")
    
            st.success("✅ Scraping terminé et données enregistrées !")
    
            # 3. AFFICHAGE IMMÉDIAT
            st.subheader("📋 Contenu actuel de la table Poules Lapins et Pigeons")
            df_poulapi = conn.query("SELECT * FROM PouLaPi")
            
            if not df_poulapi.empty:
                st.dataframe(
                    df_poulapi, 
                    column_config={"image_lien": st.column_config.ImageColumn("Photo")},
                    use_container_width=True
                )
            else:
                st.error("La table est vide malgré le scraping. Vérifiez les balises HTML.")

    # ===========================================================================

    elif animal_choisi == "Autres animaux":
        pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=10, value=1)
        
        if st.button("Lancer le Scraping"):
            st.info(f"Début du scraping pour {animal_choisi}...")
            
            # 1. S'assurer que la table existe
            with conn.session as s:
                s.execute(text("CREATE TABLE IF NOT EXISTS AutresAnimaux (nom TEXT, prix TEXT, adresse TEXT, image_lien TEXT)"))
                s.commit()
    
            for index_page in range(1, pages + 1):
                st.write(f"Scraping de la page {index_page}...")
                url3 = f'https://sn.coinafrique.com/categorie/autres-animaux?page={index_page}'
                res = get(url3)
                soup = bs(res.content, 'html.parser')
                containers = soup.find_all('div','col s6 m4 l3')
                
                for container in containers:
                    try:
                        nom = container.find('p','ad__card-description').a.text.strip()
                        prix = container.find('p','ad__card-price').a.text.strip()
                        adresse = container.find('p','ad__card-location').span.text.strip()
                        image_lien = container.find('img','ad__card-img')['src']
            
                        # 2. Utiliser la syntaxe text() et les paramètres nommés (plus robuste)
                        with conn.session as s:
                            s.execute(
                                text("INSERT INTO AutresAnimaux (nom, prix, adresse, image_lien) VALUES (:n, :p, :a, :i)"),
                                {"n": nom, "p": prix, "a": adresse, "i": image_lien}
                            )
                            s.commit()
                    except Exception as e:
                        # On affiche l'erreur si l'extraction d'une ligne échoue
                        st.warning(f"Erreur sur une ligne : {e}")
    
            st.success("✅ Scraping terminé et données enregistrées !")
    
            # 3. AFFICHAGE IMMÉDIAT
            st.subheader("📋 Contenu actuel de la table Autres animaux")
            df_autresanimaux = conn.query("SELECT * FROM AutresAnimaux")
            
            if not df_autresanimaux.empty:
                st.dataframe(
                    df_autresanimaux, 
                    column_config={"image_lien": st.column_config.ImageColumn("Photo")},
                    use_container_width=True
                )
            else:
                st.error("La table est vide malgré le scraping. Vérifiez les balises HTML.")

# =============================================================
    

# ==============================================================================================================================
# --- SECTION 3 : TÉLÉCHARGER DONNÉES NON NETTOYÉES ---
elif choice == "📁 Import Web Scraper":
    st.title("Téléchargement des données brutes")
    
    if st.button("Chien"):
        st.info("Récupérez ici les fichiers issus de l'extension 'Web Scraper' (non nettoyés).")
        try:
            df_chien = pd.read_csv('data_web_scraper/CoinAfrique_Data_Chien.csv')
            st.write("Données locales chargées.")
            st.dataframe(df_chien)
        except FileNotFoundError:
            st.warning("Le fichier CSV n'a pas été trouvé dans le dossier.")
            
        csv = df_chien.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger le CSV Brut", csv, "Data_Chien.csv", "text/csv")
        
    elif st.button("Mouton"):
        st.info("Récupérez ici les fichiers issus de l'extension 'Web Scraper' (non nettoyés).")
        try:
            df_mouton = pd.read_csv('data_web_scraper/CoinAfrique_Data_Moutons.csv')
            st.write("Données locales chargées.")
            st.dataframe(df_mouton)
        except FileNotFoundError:
            st.warning("Le fichier CSV n'a pas été trouvé dans le dossier.")
            
        csv = df_mouton.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger le CSV Brut", csv, "Data_Moutons.csv", "text/csv")
        
    elif st.button("Poules Lapins et Pigeons"):
        st.info("Récupérez ici les fichiers issus de l'extension 'Web Scraper' (non nettoyés).")
        try:
            df_poulapi = pd.read_csv('data_web_scraper/CoinAfrique_Data_PouLaPi.csv')
            st.write("Données locales chargées.")
            st.dataframe(df_poulapi)
        except FileNotFoundError:
            st.warning("Le fichier CSV n'a pas été trouvé dans le dossier.")
            
        csv = df_poulapi.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger le CSV Brut", csv, "Data_PouLaPi.csv", "text/csv")
        
    elif st.button("Autres animaux"):
        st.info("Récupérez ici les fichiers issus de l'extension 'Web Scraper' (non nettoyés).")
        try:
            df_autresanimaux = pd.read_csv('data_web_scraper/CoinAfrique_Data_AutresAnimaux.csv')
            st.write("Données locales chargées.")
            st.dataframe(df_autresanimaux)
        except FileNotFoundError:
            st.warning("Le fichier CSV n'a pas été trouvé dans le dossier.")
            


# =====================================================================================================================================================
# --- SECTION 4 : DASHBOARD (Données nettoyées) ---
elif choice == "📊 Dashboard":
    st.title("Tableau de bord des données nettoyées")
    
    # Chargement des données
    df_clean = pd.read_csv('data_web_scraper/CoinAfrique_Data_Chien.csv')
    df_chien = df_clean[['nom', 'prix', 'adresse','image_lien']]
    
    if not df_chien.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Animaux", len(df_chien))
            st.bar_chart(df_chien['nom'].value_counts()) # Exemple
        with col2:
            st.write("Aperçu des données")
            st.dataframe(df_chien)
    else:
        st.warning("Aucune donnée nettoyée disponible.")


    # Chargement des données
    df_clean = pd.read_csv('data_web_scraper/CoinAfrique_Data_Moutons.csv')
    df_mouton = df_clean[['nom', 'prix', 'adresse','image_lien']]
    
    if not df_mouton.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Animaux", len(df_mouton))
            st.bar_chart(df_mouton['nom'].value_counts()) # Exemple
        with col2:
            st.write("Aperçu des données")
            st.dataframe(df_mouton)
    else:
        st.warning("Aucune donnée nettoyée disponible.")

    # Lecture des données
    df_clean = pd.read_csv('data_web_scraper/CoinAfrique_Data_AutresAnimaux.csv')
    df_autre = df_clean[['nom', 'prix', 'adresse','image_lien']]
    
    if not df_autre.empty:
        st.markdown("### 📈 Statistiques Clés")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Animaux", f"{len(df_autre)} têtes", "🐑")
        
        # Sécurisation du Prix Max
        max_prix = df_autre['prix'].max() if not df_autre['prix'].isnull().all() else "N/A"
        m2.metric("Prix Max", f"{max_prix}", "💰")
        
        # Sécurisation de la Localisation (La source de l'erreur)
        mode_adresse = df_autre['adresse'].mode()
        top_loc = mode_adresse[0] if not mode_adresse.empty else "Inconnue"
        m3.metric("Localisation Top", top_loc, "📍")

    
        st.divider()
    
        # --- LOOK 1 : Graphique Interactif (Plotly) ---
        st.subheader("📊 Répartition par Localité")
        fig = px.pie(df_autre, names='adresse', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
    
        # --- LOOK 2 : Affichage en mode "Catalogue / Galerie" ---
        st.subheader("🖼️ Galerie des Annonces")

        # On limite le choix entre 3 et le maximum disponible
        nb_a_afficher = st.slider("Nombre d'annonces à afficher", 3, len(df_autre), 6)
        
        # On ne prend que les 'n' premières lignes
        df_selection = df_autre.head(nb_a_afficher)
        
        cols = st.columns(3)
        for i, row in df_selection.iterrows():
            with cols[i % 3]:
                st.image(row['image_lien'], use_container_width=True)
                st.caption(f"💰 {row['prix']} | 📍 {row['adresse']}")
            
    else:
        st.warning("⚠️ Aucune donnée disponible pour le dashboard.")

# ======================================================================================================================================

# --- SECTION 5 : ÉVALUATION ---
elif choice == "📝 Évaluation":
    st.title("Votre avis nous intéresse")
    st.write("Merci de remplir le formulaire ci-dessous :")
    
    # Lien vers Google Forms ou Kobo
    form_url = "https://ee.kobotoolbox.org/x/vzaPiOzs"
    st.markdown(f'[👉 Cliquez ici pour ouvrir le formulaire]({form_url})')
    
    # Alternative : Intégration directe (Iframe)
    st.components.v1.iframe(form_url, height=600, scrolling=True)




