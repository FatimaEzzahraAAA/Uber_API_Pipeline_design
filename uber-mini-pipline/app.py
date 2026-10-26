import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Uber Manager Pro", page_icon="🚕", layout="wide")
st.title("🚕 Uber Manager Pro")

API_URL = "http://localhost:8000"

# Création des 4 onglets
tab_passenger, tab_driver, tab_new_ride, tab_manage_rides = st.tabs([
    "👤 Passagers", "🚙 Chauffeurs", "➕ Nouvelle Course", "📋 Gérer les Courses"
])

# ==========================================
# ONGLET 1 : PASSAGERS
# ==========================================
with tab_passenger:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Ajouter un passager")
        with st.form("form_passenger"):
            p_name = st.text_input("Nom complet")
            p_email = st.text_input("Email")
            p_phone = st.text_input("Téléphone")
            p_pay_type = st.selectbox("Type de paiement", ["card", "apple_pay", "google_pay"])
            p_pay_last4 = st.text_input("4 derniers chiffres carte", "4242")
            
            if st.form_submit_button("Enregistrer le passager"):
                payload = {"name": p_name, "email": p_email, "phone": p_phone, "payment_type": p_pay_type, "payment_last4": p_pay_last4}
                res = requests.post(f"{API_URL}/passengers", json=payload)
                if res.status_code == 201:
                    st.success("Passager ajouté !")
                    st.rerun()
                else:
                    st.error("Erreur lors de l'ajout.")
                    
    with col2:
        st.subheader("Liste des passagers")
        try:
            res = requests.get(f"{API_URL}/passengers")
            if res.status_code == 200 and res.json():
                st.dataframe(pd.DataFrame(res.json()), use_container_width=True)
            else:
                st.info("Aucun passager enregistré.")
        except:
            st.warning("API non disponible.")

# ==========================================
# ONGLET 2 : CHAUFFEURS
# ==========================================
with tab_driver:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Ajouter un chauffeur")
        with st.form("form_driver"):
            d_name = st.text_input("Nom complet")
            d_email = st.text_input("Email")
            d_phone = st.text_input("Téléphone")
            st.markdown("**Véhicule**")
            v_make = st.text_input("Marque", "Toyota")
            v_model = st.text_input("Modèle", "Prius")
            v_plate = st.text_input("Plaque d'immatriculation", "1234-A-56")
            v_capacity = st.number_input("Capacité", min_value=1, max_value=8, value=4)
            
            if st.form_submit_button("Enregistrer le chauffeur"):
                payload = {"name": d_name, "email": d_email, "phone": d_phone, "vehicle_make": v_make, "vehicle_model": v_model, "license_plate": v_plate, "capacity": v_capacity}
                res = requests.post(f"{API_URL}/drivers", json=payload)
                if res.status_code == 201:
                    st.success("Chauffeur ajouté !")
                    st.rerun()
                else:
                    st.error("Erreur lors de l'ajout.")
                    
    with col2:
        st.subheader("Liste des chauffeurs")
        try:
            res = requests.get(f"{API_URL}/drivers")
            if res.status_code == 200 and res.json():
                st.dataframe(pd.DataFrame(res.json()), use_container_width=True)
            else:
                st.info("Aucun chauffeur enregistré.")
        except:
            st.warning("API non disponible.")

# ==========================================
# ONGLET 3 : NOUVELLE COURSE (Création avec Dropdowns)
# ==========================================
with tab_new_ride:
    st.header("Commander une course")
    
    # On récupère les données pour les menus déroulants
    try:
        res_p = requests.get(f"{API_URL}/passengers").json()
        res_d = requests.get(f"{API_URL}/drivers").json()
        
        if not res_p:
            st.warning("⚠️ Veuillez d'abord créer au moins un passager.")
        else:
            with st.form("form_new_ride"):
                # Création des dictionnaires pour mapper ID -> Nom
                passagers_dict = {p["id"]: f"{p['name']} ({p['email']})" for p in res_p}
                chauffeurs_dict = {d["id"]: f"{d['name']} - {d['vehicle_make']} {d['vehicle_model']} ({d['license_plate']})" for d in res_d}
                
                # Selection
                selected_passenger_id = st.selectbox("Choisir le Passager", options=list(passagers_dict.keys()), format_func=lambda x: passagers_dict[x])
                
                # Optionnel : assigner un chauffeur direct
                options_driver = [None] + list(chauffeurs_dict.keys())
                selected_driver_id = st.selectbox("Assigner un Chauffeur (Optionnel)", options=options_driver, format_func=lambda x: "Aucun (Chercher plus tard)" if x is None else chauffeurs_dict[x])
                fare = st.number_input("Tarif estimé (en €)", min_value=0.0, value=15.0, step=0.5)


                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Départ")
                    p_lat = st.number_input("Lat", value=48.8566)
                    p_lng = st.number_input("Lng", value=2.3522)
                with col2:
                    st.subheader("Arrivée")
                    d_lat = st.number_input("Lat ", value=48.8600)
                    d_lng = st.number_input("Lng ", value=2.3600)
                    
                if st.form_submit_button("Créer la course"):
                    payload = {
                        "passenger_id": selected_passenger_id,
                        "driver_id": selected_driver_id,
                        "pickup": {"lat": p_lat, "lng": p_lng},
                        "dropoff": {"lat": d_lat, "lng": d_lng},
                        "fare_estimate": fare
                    }
                    res = requests.post(f"{API_URL}/rides", json=payload)
                    if res.status_code == 201:
                        st.success("Course créée avec succès !")
                    else:
                        st.error("Erreur de création.")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")

# ==========================================
# ONGLET 4 : GESTION DES COURSES
# ==========================================
with tab_manage_rides:
    st.header("Toutes les courses")
    if st.button("Rafraîchir"):
        st.rerun()
        
    try:
        res = requests.get(f"{API_URL}/rides")
        rides = res.json()
        if rides:
            st.dataframe(pd.DataFrame(rides), use_container_width=True)
            
            ride_ids = [r["id"] for r in rides]
            selected_ride = st.selectbox("Sélectionner une course", ride_ids)
            
            # --- NOUVELLE SECTION : MODIFIER LE STATUT ---
            st.markdown("### 🔄 Modifier le statut")
            col_status1, col_status2 = st.columns([2, 1])

            with col_status1:
                # La liste des statuts possibles
                nouveaux_statuts = ["REQUESTED", "ACCEPTED", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
                nouveau_statut = st.selectbox("Choisir le nouveau statut", nouveaux_statuts)
                
            with col_status2:
                st.write("") # Petit espace pour aligner le bouton avec la liste
                st.write("") 
                if st.button("Mettre à jour le statut"):
                    res_update = requests.patch(
                        f"{API_URL}/rides/{selected_ride}/status", 
                        json={"status": nouveau_statut}
                    )
                    if res_update.status_code == 200:
                        st.success(f"Statut mis à jour en : {nouveau_statut}")
                        st.rerun()
                    else:
                        st.error("Erreur lors de la mise à jour.")
            # ---------------------------------------------
            
            st.divider()

            # --- TES ANCIENNES ACTIONS (Accepter / Supprimer) ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Accepter la course")
                if st.button("✅ Accepter (Assigner chauffeur auto)"):
                    # ... (ton ancien code pour accepter)
                    pass
            with col2:
                st.markdown("#### Supprimer la course")
                if st.button("🗑️ Supprimer", type="primary"):
                    requests.delete(f"{API_URL}/rides/{selected_ride}")
                    st.rerun()
        else:
            st.info("Aucune course pour le moment.")
    except Exception as e:
        st.warning(f"Erreur API : {e}")