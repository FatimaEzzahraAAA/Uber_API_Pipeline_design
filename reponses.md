# Exercice — Design Uber API
## cadrer, modeliser et etendre une API multi-face

### CADRAGE · PARTIE A : Périmètre & deux faces du produit

1. Uber regroupe plusieurs services (VTC, Eats, Pool). Pourquoi est-il important de clarifier le périmètre avant de dessiner un schéma ? Justifie en une phrase

    Uber Eats gère de la logistique de nourriture (restaurants, coursiers) et Pool gère du multi-tenant (plusieurs passagers). Si on mélange tout, le schéma devient illisible et impossible à scaler.

3. Le produit a deux faces : passager et conducteur. Liste au moins 3 actions côté passager et 3 côté conducteur.

    Passager : 
    - Demander une course 
    - voir la position du chauffeur sur la carte 
    - payer la course
    - noter la course

    Conducteur : 
    - Accepter/Refuser/annuler la course
    - mettre à jour son statut (En ligne/Hors ligne/occupé)
    - terminer la course.
    - commenter en cas d'annulation 

4. Pourquoi est-il pertinent de prévoir deux API distinctes (passager / conducteur) plutôt qu'une seule API générique ?

    Pour des raisons de Sécurité et de Rate Limiting. 
    L'API Passager subit des pics massifs (ex: vendredi soir 20h) et nécessite un rate limiting agressif. 
    L'API Conducteur gère des flux GPS constants (haute fréquence). 
    Séparer les deux permet de scaler indépendamment les serveurs.

### MODÉLISATION · PARTIE B : L'entité Ride

5. Propose la liste des champs de l'entité Ride (identifiant, driver_info , passenger_info
, statut, point de départ, destination, etc.).

    - id (UUID) 
    - passenger_id 
    - driver_id 
    - status 
    - pickup (lat/lng) 
    - dropoff (lat/lng) 
    - fare_estimate 
    - created_at.

6. Pour driver_info et passenger_info , s'agit-il d'un simple identifiant (référence) ou d'un
objet imbriqué complet ? Justifie ton choix.

    Dans l'API, on fait une jointure pour retourner un objet passenger_info pour faciliter l'affichage côté frontend.

7. Liste les endpoints minimum pour : demander une course, accepter une course (côté conducteur), consulter le statut d'une course, terminer une course.

    - POST /rides                 # demander une course (passager)
    - POST /rides/{id}/accept     # accepter une course (conducteur)
    - GET  /rides/{id}            # consulter le statut d'une course (passager)
    - POST /rides/{id}/complete   # terminer une course (conducteur)

8. Bonus — propose une liste ordonnée de statuts pour le cycle de vie d'une course (ex :
requested , accepted , in_progress , completed , ...).

    Statuts : REQUESTED -> ACCEPTED -> ARRIVED -> IN_PROGRESS -> COMPLETED (ou CANCELLED).

### EXTENSION · PARTIE C : Uber Pool — côté passager

9. Sur Uber Pool, plusieurs passagers indépendants partagent une même voiture, chacun avec son propre trajet (départ / destination différents). Peut-on simplement transformer passenger_info en une liste ( repeated field ) sur l'entité Ride ? Explique pourquoi cette approche pose problème.

    Cela viole le principe de responsabilité unique. Un Ride a une destination et un prix. Si on met 3 passagers, on ne sait plus à qui attribuer la destination ou le tarif. Cela crée de la Data Skew
   

11. Quelles informations supplémentaires l'entité PoolRide doit-elle porter (ordre de dépose,driver_info , etc.) ?

    - driver_id
    - rides (tableau)
    - dropoff_order (l'ordre de dépose optimisé)
    - vehicle_capacity

12. Bonus — pourquoi vaut-il mieux réutiliser Ride comme brique plutôt que de dupliquer sa logique dans PoolRide ? Explique en une phrase.

    Pour éviter la duplication de code et de logique métier. Ride est notre "brique de base", On utilise le même cycle de statut et les mêmes endpoints pour une course Pool que pour une course simple.

### EXTENSION · PARTIE D : Uber Pool — côté conducteur

13. Sur Uber Pool, un conducteur peut accepter une nouvelle course même s'il en effectue déjà une, jusqu'à la capacité de son véhicule. Quel nouveau statut conducteur proposerais-tu pour représenter cet état (« en course mais disponible pour un ramassage supplémentaire ») ?

    ON_TRIP_AVAILABLE_FOR_POOL. Cela signifie que le conducteur est en course (IN_PROGRESS), mais que capacity_remaining > 0

14. Comment le conducteur découvre-t-il de nouvelles courses à ajouter à son PoolRide en cours ? Réutilise-t-il le même endpoint que pour une course simple ?

    Il utilise (GET /rides/available), mais le backend filtre les résultats en fonction de la distance (géolocalisation) et de la capacité restante du véhicule.

15. Bonus — à quel moment le conducteur doit-il arrêter d'accepter de nouvelles courses sur son PoolRide en cours ? Propose une règle simple.

    Le conducteur arrête d'accepter quand nombre_rides_actifs == vehicle_capacity