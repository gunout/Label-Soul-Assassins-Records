# dashboard_soul_assassins.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE STRATÉGIQUE - SOUL ASSASSINS",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème Soul Assassins (noir, violet, occult)
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #000000 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #8A2BE2 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #8A2BE2;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(138, 43, 226, 0.5);
        background: linear-gradient(90deg, #000000, #1a001a, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Impact', 'Haettenschweiler', sans-serif;
        letter-spacing: 2px;
    }
    
    .academic-card {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.1);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.3);
        border-color: #8A2BE2;
    }
    
    .muggs-card { 
        border-left: 5px solid #8A2BE2; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    .cypress-card { 
        border-left: 5px solid #FF4500; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .gza-card { 
        border-left: 5px solid #4169E1; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    .roc-card { 
        border-left: 5px solid #FFD700; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .illbill-card { 
        border-left: 5px solid #DC143C; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .planetasia-card { 
        border-left: 5px solid #00FF7F; 
        background: linear-gradient(135deg, #0a1a0a 0%, #1a2d1a 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #8A2BE2 !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(138, 43, 226, 0.5);
        font-family: 'Impact', 'Haettenschweiler', sans-serif;
        letter-spacing: 1px;
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #8A2BE2;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(138, 43, 226, 0.2);
        font-family: 'Impact', 'Haettenschweiler', sans-serif;
        letter-spacing: 1px;
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #8A2BE2;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'Courier New', monospace;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #0a0a0a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1a1a;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
        font-family: 'Courier New', monospace;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d2d2d;
        border-color: #8A2BE2;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #8A2BE2 !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #8A2BE2;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%);
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.3);
        font-family: 'Courier New', monospace;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #9B30FF 0%, #8A2BE2 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(138, 43, 226, 0.5);
    }
    
    .stDataFrame {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #8A2BE2;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(10, 10, 10, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Soul Assassins Badge */
    .soulassassins-badge {
        display: inline-block;
        background: #000000;
        color: #8A2BE2;
        padding: 5px 15px;
        border-radius: 20px;
        border: 2px solid #8A2BE2;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0 5px 10px 0;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
    }
    
    /* Occult Symbol */
    .occult-symbol {
        font-size: 1.5rem;
        margin: 0 5px;
        color: #8A2BE2;
    }
    
    /* Dark Theme Elements */
    .dark-glow {
        position: relative;
    }
    
    .dark-glow::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #8A2BE2, #4B0082, #8A2BE2);
        z-index: -1;
        border-radius: 12px;
        opacity: 0.3;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Matrix/Code effect */
    .code-text {
        font-family: 'Courier New', monospace;
        background: rgba(138, 43, 226, 0.1);
        padding: 5px 10px;
        border-radius: 5px;
        border-left: 3px solid #8A2BE2;
    }
</style>
""", unsafe_allow_html=True)

class SoulAssassinsAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour Soul Assassins
        self.color_palette = {
            'DJ MUGGS': '#8A2BE2',        # Violet bleuâtre
            'CYPRESS HILL': '#FF4500',    # Orange rougeâtre
            'GZA': '#4169E1',             # Bleu royal
            'ROC MARCIANO': '#FFD700',    # Or
            'ILL BILL': '#DC143C',        # Crimson
            'PLANET ASIA': '#00FF7F',     # Vert printemps
            'FLEE LORD': '#9370DB',       # Violet moyen
            'Période 90s': '#8A2BE2',
            'Période 2000s': '#FF4500',
            'Période 2010s': '#00FF7F'
        }
        
        # Couleurs pour les types de données
        self.data_colors = {
            'Ventes': '#8A2BE2',
            'Albums': '#FF4500',
            'Artistes': '#4169E1',
            'Productions': '#FFD700',
            'Underground': '#00FF7F'
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur Soul Assassins"""
        
        # Données principales sur le collectif/label
        self.label_data = {
            'fondation': 1997,
            'fondateur': 'DJ Muggs',
            'statut': 'Collectif/Label underground',
            'siege': 'Los Angeles, Californie, USA',
            'specialisation': 'Hip-hop underground, rap occult, boom bap',
            'philosophie': "Dark, spiritual, esoteric hip-hop",
            'distribution': 'Indépendante, collaborations limitées'
        }

        # Données des artistes principaux
        self.artists_data = {
            'DJ MUGGS': {
                'debut': 1997,
                'genre': 'Boom bap, rap occult, hip-hop expérimental',
                'albums_soulassassins': 15,
                'ventes_totales': 800000,
                'succes_principal': 'Soul Assassins: Chapter 1 (1997)',
                'statut': 'Fondateur et producteur principal',
                'impact': 'Pionnier du rap occult et esotérique',
                'annees_activite': '1997-présent',
                'albums_principaux': ['Soul Assassins: Chapter 1', 'Soul Assassins: Chapter 2', 'Dia del Asesinato'],
                'chiffre_affaires_estime': 5000000,
                'public_cible': 'Underground, fans rap technique',
                'tournees': 'Limitée, événements spécialisés'
            },
            'CYPRESS HILL': {
                'debut': 1997,
                'genre': 'Hip-hop, rap rock, stoner rap',
                'albums_soulassassins': 3,
                'ventes_totales': 18000000,
                'succes_principal': 'Black Sunday (1993) - avant SA',
                'statut': 'Groupe légendaire associé',
                'impact': 'Croisement hip-hop/rock/metal',
                'annees_activite': '1997-2004',
                'albums_principaux': ['IV', 'Stoned Raiders'],
                'chiffre_affaires_estime': 40000000,
                'public_cible': 'Alternative, metal, hip-hop',
                'tournees': 'Internationales'
            },
            'GZA': {
                'debut': 1999,
                'genre': 'Hip-hop, rap technique, spiritual',
                'albums_soulassassins': 1,
                'ventes_totales': 2000000,
                'succes_principal': 'Beneath the Surface (1999)',
                'statut': 'Membre Wu-Tang Clan',
                'impact': 'Rap intellectuel et technique',
                'annees_activite': '1999-2000',
                'albums_principaux': ['Beneath the Surface'],
                'chiffre_affaires_estime': 10000000,
                'public_cible': 'Puristes Wu-Tang, underground',
                'tournees': 'Nationales'
            },
            'ROC MARCIANO': {
                'debut': 2010,
                'genre': 'Boom bap, mafioso rap, underground',
                'albums_soulassassins': 2,
                'ventes_totales': 300000,
                'succes_principal': 'Marcberg (2010)',
                'statut': 'Figure majeure underground moderne',
                'impact': 'Renaissance boom bap 2010s',
                'annees_activite': '2010-présent',
                'albums_principaux': ['Marcberg', 'Reloaded'],
                'chiffre_affaires_estime': 2000000,
                'public_cible': 'Underground New York, boom bap',
                'tournees': 'Limitée'
            },
            'ILL BILL': {
                'debut': 2004,
                'genre': 'Hardcore rap, horrorcore, underground',
                'albums_soulassassins': 3,
                'ventes_totales': 400000,
                'succes_principal': 'What\'s Wrong with Bill? (2004)',
                'statut': 'Membre Non Phixion, underground',
                'impact': 'Hardcore rap politique',
                'annees_activite': '2004-2012',
                'albums_principaux': ['What\'s Wrong with Bill?', 'The Hour of Reprisal'],
                'chiffre_affaires_estime': 2500000,
                'public_cible': 'Hardcore, politique, underground',
                'tournees': 'Nationales underground'
            },
            'PLANET ASIA': {
                'debut': 2001,
                'genre': 'Underground hip-hop, West Coast',
                'albums_soulassassins': 2,
                'ventes_totales': 250000,
                'succes_principal': 'The Pain (2004)',
                'statut': 'Lyricist West Coast underground',
                'impact': 'Maintenance qualité West Coast',
                'annees_activite': '2001-2008',
                'albums_principaux': ['The Pain', 'The Medicine'],
                'chiffre_affaires_estime': 1500000,
                'public_cible': 'West Coast underground',
                'tournees': 'Régionales'
            },
            'FLEE LORD': {
                'debut': 2020,
                'genre': 'Boom bap, rap New York moderne',
                'albums_soulassassins': 2,
                'ventes_totales': 100000,
                'succes_principal': 'Pray for the Evil 2 (2021)',
                'statut': 'Nouvelle génération',
                'impact': 'Continuité tradition boom bap',
                'annees_activite': '2020-présent',
                'albums_principaux': ['Pray for the Evil 2', 'In the Name of Prodigy'],
                'chiffre_affaires_estime': 800000,
                'public_cible': 'Jeune underground, nostalgique',
                'tournees': 'Émergentes'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1997, 'evenement': 'Fondation par DJ Muggs après Cypress Hill', 'type': 'Structure', 'importance': 10},
            {'annee': 1997, 'evenement': 'Sortie de Soul Assassins: Chapter 1', 'type': 'Album', 'importance': 9},
            {'annee': 1998, 'evenement': 'Tournée mondiale avec Cypress Hill', 'type': 'Tournée', 'importance': 8},
            {'annee': 1999, 'evenement': 'Collaboration avec GZA (Wu-Tang)', 'type': 'Collaboration', 'importance': 9},
            {'annee': 2000, 'evenement': 'Soul Assassins: Chapter 2', 'type': 'Album', 'importance': 8},
            {'annee': 2004, 'evenement': 'Signature d\'Ill Bill', 'type': 'Artiste', 'importance': 7},
            {'annee': 2006, 'evenement': 'Pause du collectif', 'type': 'Structure', 'importance': 6},
            {'annee': 2010, 'evenement': 'Retour avec Roc Marciano', 'type': 'Artiste', 'importance': 8},
            {'annee': 2013, 'evenement': 'Dia del Asesinato (album)', 'type': 'Album', 'importance': 7},
            {'annee': 2018, 'evenement': 'Soul Assassins: Intermission', 'type': 'Album', 'importance': 6},
            {'annee': 2020, 'evenement': 'Signature de Flee Lord', 'type': 'Artiste', 'importance': 7},
            {'annee': 2021, 'evenement': 'Collab avec MF DOOM posthume', 'type': 'Collaboration', 'importance': 8},
            {'annee': 2023, 'evenement': '25 ans d\'anniversaire', 'type': 'Événement', 'importance': 6}
        ]

        # Données financières et commerciales (underground focus)
        self.financial_data = {
            'DJ MUGGS': {
                'ventes_albums': 800000,
                'chiffre_affaires': 5000000,
                'rentabilite': 60,
                'cout_production_moyen': 50000,
                'budget_marketing_moyen': 100000,
                'roi': 150,
                'influence_underground': 10
            },
            'CYPRESS HILL': {
                'ventes_albums': 18000000,
                'chiffre_affaires': 40000000,
                'rentabilite': 75,
                'cout_production_moyen': 300000,
                'budget_marketing_moyen': 1000000,
                'roi': 300,
                'influence_underground': 8
            },
            'GZA': {
                'ventes_albums': 2000000,
                'chiffre_affaires': 10000000,
                'rentabilite': 70,
                'cout_production_moyen': 150000,
                'budget_marketing_moyen': 300000,
                'roi': 200,
                'influence_underground': 9
            },
            'ROC MARCIANO': {
                'ventes_albums': 300000,
                'chiffre_affaires': 2000000,
                'rentabilite': 65,
                'cout_production_moyen': 30000,
                'budget_marketing_moyen': 50000,
                'roi': 180,
                'influence_underground': 10
            },
            'ILL BILL': {
                'ventes_albums': 400000,
                'chiffre_affaires': 2500000,
                'rentabilite': 62,
                'cout_production_moyen': 40000,
                'budget_marketing_moyen': 80000,
                'roi': 160,
                'influence_underground': 9
            },
            'PLANET ASIA': {
                'ventes_albums': 250000,
                'chiffre_affaires': 1500000,
                'rentabilite': 58,
                'cout_production_moyen': 25000,
                'budget_marketing_moyen': 60000,
                'roi': 140,
                'influence_underground': 8
            },
            'FLEE LORD': {
                'ventes_albums': 100000,
                'chiffre_affaires': 800000,
                'rentabilite': 55,
                'cout_production_moyen': 20000,
                'budget_marketing_moyen': 30000,
                'roi': 120,
                'influence_underground': 7
            }
        }

        # Données de stratégie marketing (underground focus)
        self.marketing_data = {
            'DJ MUGGS': {
                'strategie': 'Cult following, exclusivité, mystique',
                'cibles': 'Collecteurs, underground, connaisseurs',
                'canaux': ['Vinyle limité', 'Événements privés', 'Réseaux underground'],
                'budget_ratio': 15,
                'succes': 'Cult',
                'innovations': 'Marketing occulte et mystique'
            },
            'CYPRESS HILL': {
                'strategie': 'Cross-genre, festival, alternative',
                'cibles': 'Metalheads, stoners, alternative',
                'canaux': ['Festivals', 'Radio college', 'Magazines alternatifs'],
                'budget_ratio': 25,
                'succes': 'Mainstream alternatif',
                'innovations': 'Croisement hip-hop/metal'
            },
            'GZA': {
                'strategie': 'Intellectuel, Wu-Tang affiliate, puriste',
                'cibles': 'Fans Wu-Tang, puristes, intellectuels',
                'canaux': ['Mixtapes underground', 'Conférences', 'Presse niche'],
                'budget_ratio': 18,
                'succes': 'Critique',
                'innovations': 'Marketing intellectuel'
            },
            'ROC MARCIANO': {
                'strategie': 'Street credibility, limited releases',
                'cibles': 'Underground NY, boom bap revival',
                'canaux': ['Bandcamp', 'Vinyle exclusif', 'Réseaux sociaux niche'],
                'budget_ratio': 12,
                'succes': 'Underground star',
                'innovations': 'Marketing digital underground'
            },
            'ILL BILL': {
                'strategie': 'Hardcore, politique, confrontational',
                'cibles': 'Hardcore rap, politique, underground',
                'canaux': ['Webzines', 'Concerts intimistes', 'Features'],
                'budget_ratio': 14,
                'succes': 'Niche',
                'innovations': 'Marketing politique underground'
            },
            'PLANET ASIA': {
                'strategie': 'West Coast underground, lyricism',
                'cibles': 'West Coast puristes, underground',
                'canaux': ['Radio locale', 'Features', 'Mixtapes'],
                'budget_ratio': 13,
                'succes': 'Regional',
                'innovations': 'Marketing régional underground'
            },
            'FLEE LORD': {
                'strategie': 'Nouvelle génération, digital native',
                'cibles': 'Jeunes underground, nostalgiques',
                'canaux': ['Instagram', 'YouTube', 'Streaming niche'],
                'budget_ratio': 16,
                'succes': 'Émergent',
                'innovations': 'Marketing social media underground'
            }
        }

        # Données de production
        self.production_data = {
            'DJ MUGGS': {
                'albums_produits': 15,
                'duree_contrat': 26,
                'rythme_sorties': '1-2 ans',
                'qualite_production': 9,
                'autonomie_artistique': 10,
                'support_label': 8,
                'style_production': 'Boom bap dark, samples occultes'
            },
            'CYPRESS HILL': {
                'albums_produits': 3,
                'duree_contrat': 7,
                'rythme_sorties': '3-4 ans',
                'qualite_production': 8,
                'autonomie_artistique': 9,
                'support_label': 9,
                'style_production': 'Hip-hop/rock fusion'
            },
            'GZA': {
                'albums_produits': 1,
                'duree_contrat': 1,
                'rythme_sorties': '1 an',
                'qualite_production': 9,
                'autonomie_artistique': 9,
                'support_label': 7,
                'style_production': 'Rap technique intellectuel'
            },
            'ROC MARCIANO': {
                'albums_produits': 2,
                'duree_contrat': 13,
                'rythme_sorties': '6-7 ans',
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 8,
                'style_production': 'Boom bap moderne, mafioso'
            },
            'ILL BILL': {
                'albums_produits': 3,
                'duree_contrat': 8,
                'rythme_sorties': '4 ans',
                'qualite_production': 8,
                'autonomie_artistique': 8,
                'support_label': 7,
                'style_production': 'Hardcore, samples cinématiques'
            },
            'PLANET ASIA': {
                'albums_produits': 2,
                'duree_contrat': 7,
                'rythme_sorties': '3.5 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 7,
                'style_production': 'West Coast underground'
            },
            'FLEE LORD': {
                'albums_produits': 2,
                'duree_contrat': 3,
                'rythme_sorties': '1.5 ans',
                'qualite_production': 7,
                'autonomie_artistique': 8,
                'support_label': 8,
                'style_production': 'Boom bap nostalgique'
            }
        }

        # Données de gestion et management
        self.management_data = {
            'structure': {
                'type': 'Collectif artistique / Label boutique',
                'effectif': 8,
                'departements': ['Production', 'A&R limité', 'Digital'],
                'processus_decision': 'DJ Muggs + artistes principaux',
                'culture_entreprise': 'Familial, underground, artistique'
            },
            'ressources_humaines': {
                'turnover': 'Faible',
                'expertise': 'Production boom bap, réseau underground',
                'reseautage': 'Underground mondial',
                'formation': 'Apprentissage sur le tas'
            },
            'finances': {
                'model_economique': 'Low budget, high creativity, fan direct',
                'marge_nette': '15-20%',
                'investissement_artistes': 'Minimal, collaborations',
                'risque': 'Faible (coûts bas)'
            },
            'relations_artistes': {
                'approche': 'Collaborative, respect artistique',
                'contrats': 'Flexibles, souvent verbaux',
                'communication': 'Directe, souvent informelle',
                'loyaute': 'Forte (famille underground)'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">💀 SOUL ASSASSINS - DASHBOARD STRATÉGIQUE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem; font-family: Courier New, monospace;">Collectif/Label underground - Analyse complète 1997-2024</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventes = sum(self.financial_data[artist]['ventes_albums'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card muggs-card">
                <div style="color: {self.color_palette['DJ MUGGS']}; font-size: 1rem; font-weight: 600; text-align: center;">💿 VENTES TOTALES</div>
                <div class="metric-value" style="color: {self.color_palette['DJ MUGGS']}; text-align: center;">{total_ventes/1000:.0f}K</div>
                <div style="color: #cccccc; text-align: center;">Unités underground</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_artistes = len(self.artists_data)
            st.markdown(f"""
            <div class="academic-card cypress-card">
                <div style="color: {self.color_palette['CYPRESS HILL']}; font-size: 1rem; font-weight: 600; text-align: center;">👥 ARTISTES</div>
                <div class="metric-value" style="color: {self.color_palette['CYPRESS HILL']}; text-align: center;">{total_artistes}</div>
                <div style="color: #cccccc; text-align: center;">Collaborateurs principaux</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_albums = sum(self.artists_data[artist]['albums_soulassassins'] for artist in self.artists_data)
            st.markdown(f"""
            <div class="academic-card gza-card">
                <div style="color: {self.color_palette['GZA']}; font-size: 1rem; font-weight: 600; text-align: center;">🎵 PROJETS</div>
                <div class="metric-value" style="color: {self.color_palette['GZA']}; text-align: center;">{total_albums}</div>
                <div style="color: #cccccc; text-align: center;">Productions collectives</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            influence_totale = sum(self.financial_data[artist]['influence_underground'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card roc-card">
                <div style="color: {self.color_palette['ROC MARCIANO']}; font-size: 1rem; font-weight: 600; text-align: center;">🌟 INFLUENCE</div>
                <div class="metric-value" style="color: {self.color_palette['ROC MARCIANO']}; text-align: center;">{influence_totale}/70</div>
                <div style="color: #cccccc; text-align: center;">Score underground</div>
            </div>
            """, unsafe_allow_html=True)

    def create_artist_analysis(self):
        """Analyse complète des artistes"""
        st.markdown('<h3 class="section-title">💀 PORTFOLIO ARTISTIQUE OCCULTE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Impact Commercial vs Underground</div>', unsafe_allow_html=True)
            self.create_influence_commercial_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 ROI Underground</div>', unsafe_allow_html=True)
            self.create_underground_roi_chart()
        
        # Analyse détaillée par artiste
        st.markdown('<div class="subsection-title">🔮 Profils Artistiques</div>', unsafe_allow_html=True)
        self.create_detailed_artist_analysis()

    def create_influence_commercial_chart(self):
        """Graphique influence vs ventes"""
        artists = list(self.artists_data.keys())
        influence = [self.financial_data[artist]['influence_underground'] for artist in artists]
        ventes_normalisees = [min(10, self.financial_data[artist]['ventes_albums'] / 200000) for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[influence[i]],
                y=[ventes_normalisees[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=12, weight='bold'),
                name=artist,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Influence Underground vs Ventes Commerciales',
            xaxis_title='Influence Underground (1-10)',
            yaxis_title='Ventes Normalisées (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#8A2BE2',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_underground_roi_chart(self):
        """Graphique ROI underground"""
        artists = list(self.financial_data.keys())
        roi = [self.financial_data[artist]['roi'] for artist in artists]
        influence = [self.financial_data[artist]['influence_underground'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=artists,
            y=roi,
            mode='lines+markers',
            line=dict(color='#8A2BE2', width=3),
            marker=dict(
                size=12,
                color=[self.color_palette[artist] for artist in artists]
            ),
            name='ROI (%)'
        ))
        
        fig.add_trace(go.Scatter(
            x=artists,
            y=[i * 20 for i in influence],  # Multiplier pour échelle similaire
            mode='lines+markers',
            line=dict(color='#FF4500', width=3, dash='dash'),
            marker=dict(
                size=12,
                color=[self.color_palette[artist] for artist in artists]
            ),
            name='Influence (x20)'
        ))
        
        fig.update_layout(
            title='ROI vs Influence Underground',
            xaxis_title='Artistes',
            yaxis_title='Valeurs',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#8A2BE2',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(tickfont=dict(size=10), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_artist_analysis(self):
        """Analyse détaillée par artiste"""
        artists = list(self.artists_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.artists_data[artist]['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques clés
                    st.metric("Projets Soul Assassins", self.artists_data[artist]['albums_soulassassins'])
                    st.metric("Ventes totales", f"{self.financial_data[artist]['ventes_albums']:,}")
                    st.metric("Influence underground", f"{self.financial_data[artist]['influence_underground']}/10")
                    
                    # Style production
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Style:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.production_data[artist]['style_production']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques commerciales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Économie Underground:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Rentabilité: {self.financial_data[artist]['rentabilite']}%</li>
                            <li>ROI: {self.financial_data[artist]['roi']}%</li>
                            <li>Coût production: ${self.financial_data[artist]['cout_production_moyen']:,}</li>
                            <li>Budget marketing: ${self.financial_data[artist]['budget_marketing_moyen']:,}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Influence', 'Qualité', 'ROI', 'Innovation']
                    valeurs = [
                        self.financial_data[artist]['influence_underground'] * 10,
                        self.production_data[artist]['qualite_production'] * 10,
                        min(100, self.financial_data[artist]['roi'] / 2),
                        100 if self.marketing_data[artist]['innovations'] in ['Marketing occulte', 'Croisement hip-hop/metal'] else
                        80 if self.marketing_data[artist]['innovations'] in ['Marketing intellectuel', 'Marketing digital'] else
                        70
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=artist
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14),
                        showlegend=False,
                        height=300,
                        title=f"Profil Underground - {artist}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_production_analysis(self):
        """Analyse de la production"""
        st.markdown('<h3 class="section-title">🎛️ ANALYSE DE LA PRODUCTION OCCULTE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">⏳ Rythme de Production</div>', unsafe_allow_html=True)
            self.create_production_pace_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">⚗️ Qualité vs Autonomie</div>', unsafe_allow_html=True)
            self.create_quality_autonomy_chart()
        
        # Analyse des styles
        st.markdown('<div class="subsection-title">🎨 Palette Sonore</div>', unsafe_allow_html=True)
        self.create_production_styles_analysis()

    def create_production_pace_chart(self):
        """Graphique rythme de production"""
        artists = list(self.production_data.keys())
        rythme = [float(self.production_data[artist]['rythme_sorties'].split()[0]) for artist in artists]
        albums = [self.production_data[artist]['albums_produits'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[rythme[i]],
                y=[albums[i]],
                mode='markers+text',
                marker=dict(
                    size=60, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Rythme de Production vs Nombre d\'Albums',
            xaxis_title='Rythme (années entre albums)',
            yaxis_title="Nombre d'albums produits",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_autonomy_chart(self):
        """Graphique qualité vs autonomie"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        autonomie = [self.production_data[artist]['autonomie_artistique'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=autonomie,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Autonomie Artistique',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Autonomie Artistique (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_production_styles_analysis(self):
        """Analyse des styles de production"""
        styles = {}
        for artist, data in self.production_data.items():
            style = data['style_production']
            if style not in styles:
                styles[style] = []
            styles[style].append(artist)
        
        # Afficher les styles
        col1, col2 = st.columns(2)
        
        with col1:
            for i, (style, artists_list) in enumerate(list(styles.items())[:len(styles)//2]):
                couleur = self.color_palette[artists_list[0]] if artists_list else '#8A2BE2'
                st.markdown(f"""
                <div class="academic-card">
                    <div style="border-left: 5px solid {couleur}; padding-left: 10px;">
                        <h4 style="color: {couleur}; font-weight: bold;">{style.upper()}</h4>
                        <p style="color: #cccccc; margin: 5px 0;">Artistes:</p>
                        <div style="color: #ffffff; font-weight: 500;">
                            {', '.join(artists_list)}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            for i, (style, artists_list) in enumerate(list(styles.items())[len(styles)//2:]):
                couleur = self.color_palette[artists_list[0]] if artists_list else '#8A2BE2'
                st.markdown(f"""
                <div class="academic-card">
                    <div style="border-left: 5px solid {couleur}; padding-left: 10px;">
                        <h4 style="color: {couleur}; font-weight: bold;">{style.upper()}</h4>
                        <p style="color: #cccccc; margin: 5px 0;">Artistes:</p>
                        <div style="color: #ffffff; font-weight: 500;">
                            {', '.join(artists_list)}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    def create_marketing_analysis(self):
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🔮 STRATÉGIES MARKETING OCCULTES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📈 Budgets vs Succès Underground</div>', unsafe_allow_html=True)
            self.create_underground_marketing_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux Underground</div>', unsafe_allow_html=True)
            self.create_underground_channels_analysis()
        
        # Analyse des innovations
        st.markdown('<div class="subsection-title">✨ Innovations Marketing</div>', unsafe_allow_html=True)
        self.create_marketing_innovations_analysis()

    def create_underground_marketing_chart(self):
        """Graphique marketing underground"""
        artists = list(self.marketing_data.keys())
        budget_ratios = [self.marketing_data[artist]['budget_ratio'] for artist in artists]
        succes = [10 if self.marketing_data[artist]['succes'] == 'Cult' else 
                 8 if self.marketing_data[artist]['succes'] == 'Mainstream alternatif' else
                 7 if self.marketing_data[artist]['succes'] == 'Critique' else
                 6 if self.marketing_data[artist]['succes'] == 'Underground star' else
                 5 for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[budget_ratios[i]],
                y=[succes[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Budget Marketing vs Succès Underground',
            xaxis_title='Ratio Budget Marketing (%)',
            yaxis_title='Succès Underground (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[10, 30], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[4, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_underground_channels_analysis(self):
        """Analyse des canaux marketing underground"""
        # Compter les canaux les plus utilisés
        canaux_count = {}
        for artist_data in self.marketing_data.values():
            for canal in artist_data['canaux']:
                canaux_count[canal] = canaux_count.get(canal, 0) + 1
        
        canaux = list(canaux_count.keys())
        counts = list(canaux_count.values())
        
        fig = go.Figure(go.Bar(
            x=counts,
            y=canaux,
            orientation='h',
            marker_color='#9370DB',
            text=counts,
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Canaux Marketing Underground',
            xaxis_title="Nombre d'artistes utilisant le canal",
            yaxis_title='Canaux',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_innovations_analysis(self):
        """Analyse des innovations marketing"""
        innovations = {}
        for artist, data in self.marketing_data.items():
            innovation = data['innovations']
            if innovation not in innovations:
                innovations[innovation] = []
            innovations[innovation].append(artist)
        
        # Afficher les innovations avec des badges
        cols = st.columns(3)
        innovation_items = list(innovations.items())
        
        for i, (innovation, artists_list) in enumerate(innovation_items):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="academic-card dark-glow">
                    <div style="text-align: center;">
                        <span class="occult-symbol">🔮</span>
                        <h4 style="color: #8A2BE2; font-weight: bold; margin: 10px 0;">{innovation.split()[0].upper()}</h4>
                        <div style="color: #cccccc; font-size: 0.9rem; margin: 5px 0;">
                            {innovation}
                        </div>
                        <div style="margin-top: 10px;">
                            {''.join([f'<span class="soulassassins-badge" style="font-size: 0.8rem; margin: 2px;">{a}</span>' for a in artists_list])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    def create_management_analysis(self):
        """Analyse de la gestion et management"""
        st.markdown('<h3 class="section-title">🏛️ STRUCTURE OCCULTE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">⚖️ Économie Underground</div>', unsafe_allow_html=True)
            self.create_underground_economics()
        
        with col2:
            st.markdown('<div class="subsection-title">🌀 Culture du Collectif</div>', unsafe_allow_html=True)
            self.create_collective_culture()
        
        # Analyse SWOT underground
        st.markdown('<div class="subsection-title">🔍 Analyse SWOT Underground</div>', unsafe_allow_html=True)
        self.create_swot_analysis()

    def create_underground_economics(self):
        """Modèle économique underground"""
        # Créer un graphique circulaire
        labels = ['Production', 'Marketing', 'Distribution', 'Artistes', 'Marge']
        valeurs = [30, 15, 20, 25, 10]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=valeurs,
            hole=.3,
            marker=dict(colors=['#8A2BE2', '#FF4500', '#4169E1', '#FFD700', '#00FF7F']),
            textinfo='label+percent',
            textfont=dict(color='white', size=14)
        )])
        
        fig.update_layout(
            title='Répartition des Coûts - Modèle Underground',
            paper_bgcolor='#1a1a1a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_collective_culture(self):
        """Culture du collectif"""
        # Afficher les valeurs du collectif
        valeurs = [
            ("👁️‍🗨️", "Artistic Freedom", "Liberté créative absolue"),
            ("🤝", "Collaboration", "Échanges artistiques mutuels"),
            ("🔮", "Mystique", "Image occulte et mystérieuse"),
            ("💎", "Qualité", "Focus sur la substance"),
            ("👥", "Communauté", "Famille underground")
        ]
        
        for emoji, titre, description in valeurs:
            st.markdown(f"""
            <div class="academic-card" style="margin-bottom: 10px;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2rem; margin-right: 15px; color: #8A2BE2;">{emoji}</span>
                    <div>
                        <div style="font-weight: bold; color: #8A2BE2; font-size: 1.1rem;">{titre}</div>
                        <div style="color: #cccccc; font-size: 0.9rem;">{description}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    def create_swot_analysis(self):
        """Analyse SWOT"""
        # Créer un graphique radar pour l'analyse SWOT
        categories = ['Forces', 'Faiblesses', 'Opportunités', 'Menaces']
        valeurs = [9, 3, 7, 4]  # Scores sur 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs + [valeurs[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#8A2BE2', width=3),
            marker=dict(size=8, color='#8A2BE2'),
            name='Analyse SWOT'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            showlegend=False,
            height=400,
            title="Analyse SWOT - Collectif Underground"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de l'analyse SWOT
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="academic-card muggs-card">
                <h4 style="color: #8A2BE2; text-align: center; font-weight: bold;">FORCES</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>DJ Muggs - producteur légendaire</li>
                    <li>Réseau underground solide</li>
                    <li>Image mystique unique</li>
                    <li>Liberté artistique totale</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card cypress-card">
                <h4 style="color: #FF4500; text-align: center; font-weight: bold;">FAIBLESSES</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Budget limité</li>
                    <li>Exposition limitée</li>
                    <li>Dépendance à Muggs</li>
                    <li>Rythme irrégulier</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="academic-card gza-card">
                <h4 style="color: #4169E1; text-align: center; font-weight: bold;">OPPORTUNITÉS</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Renaissance boom bap</li>
                    <li>Vinyle/merch premium</li>
                    <li>Streaming niche</li>
                    <li>Nouvelle génération</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="academic-card roc-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">MENACES</h4>
                <ul style="color: #ffffff; font-weight: 500; font-size: 0.9rem;">
                    <li>Mainstreamisation underground</li>
                    <li>Concurrence digitale</li>
                    <li>Vieillissement public</li>
                    <li>Économie incertaine</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def create_timeline_analysis(self):
        """Analyse chronologique"""
        st.markdown('<h3 class="section-title">📜 CHRONOLOGIE OCCULTE</h3>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour la timeline
        df_timeline = pd.DataFrame(self.timeline_data)
        
        fig = go.Figure()
        
        # Ajouter les événements par type
        for event_type in df_timeline['type'].unique():
            df_type = df_timeline[df_timeline['type'] == event_type]
            fig.add_trace(go.Scatter(
                x=df_type['annee'],
                y=df_type['importance'],
                mode='markers+text',
                marker=dict(
                    size=df_type['importance'] * 8,
                    color=self.data_colors.get(event_type, '#ffffff'),
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=df_type['evenement'],
                textposition="top center",
                textfont=dict(color='white', size=10),
                name=event_type,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Chronologie - Périodes Clés du Collectif',
            xaxis_title='Année',
            yaxis_title='Importance (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#8A2BE2',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(range=[1996, 2024], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_conclusions(self):
        """Conclusions et recommandations"""
        st.markdown('<h3 class="section-title">📜 SAGESSE OCCULTE</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card muggs-card">
                <h4 style="color: #8A2BE2; text-align: center; font-weight: bold;">⚡ LEÇONS OCCULTES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>La qualité prime sur la quantité</li>
                    <li>L'authenticité crée des cultes</li>
                    <li>Le mystère attire les connaisseurs</li>
                    <li>Les réseaux underground sont durables</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card cypress-card">
                <h4 style="color: #FF4500; text-align: center; font-weight: bold;">💎 VALEURS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Intégrité artistique</li>
                    <li>Liberté créative</li>
                    <li>Respect de la tradition</li>
                    <li>Innovation dans les limites</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card gza-card">
                <h4 style="color: #4169E1; text-align: center; font-weight: bold;">🔮 RECOMMANDATIONS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Développer les éditions collector</li>
                    <li>Créer une plateforme numérique dédiée</li>
                    <li>Organiser des événements occultes</li>
                    <li>Documenter l'héritage via NFTs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card roc-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">🌌 PERSPECTIVES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Archives digitalisées premium</li>
                    <li>Académie production underground</li>
                    <li>Collaborations intergénérationnelles</li>
                    <li>Expansion mondiale niche</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def run(self):
        """Fonction principale pour exécuter le dashboard"""
        self.display_header()
        
        # Créer les onglets principaux
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "💀 Artistes", 
            "🎛️ Production", 
            "🔮 Marketing", 
            "🏛️ Structure", 
            "📜 Chronologie", 
            "📜 Sagesse"
        ])
        
        with tab1:
            self.create_artist_analysis()
        
        with tab2:
            self.create_production_analysis()
        
        with tab3:
            self.create_marketing_analysis()
        
        with tab4:
            self.create_management_analysis()
        
        with tab5:
            self.create_timeline_analysis()
        
        with tab6:
            self.create_conclusions()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); border-radius: 10px; border: 1px solid #444444;">
            <p style="color: #8A2BE2; font-weight: bold; font-size: 1.2rem; font-family: Impact, sans-serif; letter-spacing: 1px;">SOUL ASSASSINS - Dashboard Stratégique</p>
            <p style="color: #cccccc; margin-top: 0.5rem; font-family: Courier New, monospace;">Analyse complète 1997-2024 | Collectif/Label underground</p>
            <div style="margin-top: 1rem;">
                <span class="soulassassins-badge">DJ MUGGS</span>
                <span class="soulassassins-badge">CYPRESS HILL</span>
                <span class="soulassassins-badge">GZA</span>
                <span class="soulassassins-badge">OCCULT HIP-HOP</span>
            </div>
            <p style="color: #999999; margin-top: 1rem; font-size: 0.9rem;">© 2024 - Tous droits réservés | Philosophie: Underground Éternel</p>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée principal
if __name__ == "__main__":
    analyzer = SoulAssassinsAnalyzer()
    analyzer.run()
