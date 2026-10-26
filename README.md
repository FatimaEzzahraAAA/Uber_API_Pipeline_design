# 🚕 Uber Ride-Hailing Data Pipeline & Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=for-the-badge&logo=metabase&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)

Ce projet est une application complète de bout en bout (End-to-End) qui simule une plateforme de VTC (type Uber). Il couvre l'ensemble du cycle de vie de la donnée : de la conception de l'API à la visualisation des indicateurs clés (KPI) sur un Dashboard décisionnel.

## 🎯 Objectifs du Projet
*   **System Design** : Concevoir une API RESTful robuste pour gérer un système multi-faces (Passagers / Conducteurs).
*   **Data Engineering** : Mettre en place une architecture conteneurisée avec une base de données relationnelle.
*   **Data Analytics** : Créer un pipeline de données pour analyser l'activité et générer des tableaux de bord interactifs.


## 🏗️ Architecture du Pipeline

Le projet repose sur une architecture découplée garantissant la séparation des responsabilités (Separation of Concerns).

<img width="1408" height="768" alt="uber pipline" src="https://github.com/user-attachments/assets/3a25f607-c762-4e31-a2f0-021808f02fc5" />


##  ⚙️ Stack Technique

*  Backend / API : FastAPI (Python)
*  Frontend / Interface : Streamlit (Python)
*  Base de données : PostgreSQL
*  Outil BI / Dashboard : Metabase
*  Conteneurisation : Docker & Docker Compose
*  ORM : SQLAlchemy

<img width="1408" height="768" alt="uber pipeline detaillé" src="https://github.com/user-attachments/assets/efae17c0-1a63-47fb-8dd3-044680f216e4" />


##  🚀 Fonctionnalités

1. Gestion Métier (Interface Streamlit)
   
    Passagers : Enregistrement avec informations de paiement.

<img width="1852" height="608" alt="Capture d&#39;écran 2026-10-26 002508" src="https://github.com/user-attachments/assets/3a6da270-f6ef-466e-b344-10395c7e801a" />

  Chauffeurs : Enregistrement avec détails du véhicule (marque, modèle, plaque, capacité).

<img width="1842" height="791" alt="Capture d&#39;écran 2026-10-26 002525" src="https://github.com/user-attachments/assets/92751753-6583-4a2f-979d-84845fbb07f2" />

  Courses (Rides) : Création de courses en sélectionnant un passager et un chauffeur existants.
  
<img width="1812" height="731" alt="Capture d&#39;écran 2026-10-26 002541" src="https://github.com/user-attachments/assets/bc1bc22a-0c42-42c2-ab80-6eb460812b44" />

  Cycle de vie : Modification du statut des courses (REQUESTED, ACCEPTED, IN_PROGRESS, COMPLETED, CANCELLED).

<img width="1815" height="762" alt="Capture d&#39;écran 2026-10-26 002614" src="https://github.com/user-attachments/assets/c45ed431-1099-49dd-873d-f8e683cb57f9" />


3. API REST (FastAPI)
   
    Documentation interactive générée automatiquement via Swagger UI (/docs).
    Endpoints sécurisés et validés avec Pydantic.
    Gestion complète du CRUD (Create, Read, Update, Delete).

<img width="931" height="855" alt="Capture d&#39;écran 2026-10-26 002332" src="https://github.com/user-attachments/assets/2d569574-490b-471e-9ffd-2706a718a644" />


4. Dashboard Analytique (Metabase)
   
    KPIs Globaux : Chiffre d'affaires total, Nombre de courses, Taux d'annulation.
    Analyses : Évolution du CA dans le temps, Répartition des statuts de courses.
    Classements : Top 5 des chauffeurs (avec matricules et marques de véhicules).

<img width="1036" height="825" alt="image" src="https://github.com/user-attachments/assets/aad583fd-6c97-462e-8f2e-b38ab49223be" />

👤 Auteur:
Fatima-Ezzahra BOUMAIZE
🎓 Data Maroc Bootcamp — Promotion octobre-2026
📧 fatimaezzahraboumaize020@gmail.com

