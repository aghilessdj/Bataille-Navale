'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from model.model_pg import get_joueurs_by_pseudo, insert_joueur_humain, get_joueur_by_id
from controleurs.includes import add_activity

add_activity(SESSION['HISTORIQUE'], "consultation de la page de connexion")
REQUEST_VARS['connexion_reussie'] = False

# Traitement du bouton de déconnexion
if POST and 'bouton_deconnexion' in POST:
    SESSION['JOUEUR_COURANT'] = None
    REQUEST_VARS['message'] = f"Deconnéxion réussie."
    REQUEST_VARS['message_class'] = "alert-succes"

# Traitement de le recherche de pseudo
elif POST and 'bouton_recherche' in POST:
    pseudo_recherche = POST['pseudo_recherche'][0]
    joueurs = get_joueurs_by_pseudo(SESSION['CONNEXION'], pseudo_recherche)

    if joueurs:
        REQUEST_VARS['joueurs_trouves'] = joueurs 
    else:
        REQUEST_VARS['message'] = f"Aucun joueur contenant '{pseudo_recherche}' n'a été trouvé."
        REQUEST_VARS['message_class'] = "alert-error"

# Traitement de la sélection d'un joueur parmi les résultas
elif POST and 'bouton_choix' in POST:
    id_joueur = POST['id_joueur'][0]
    joueur = get_joueur_by_id(SESSION['CONNEXION'], id_joueur)

    if joueur:
        SESSION['JOUEUR_COURANT'] = joueur 
        REQUEST_VARS['connexion_reussie'] = True

# Traitement du formulaire d'inscription
elif POST and 'bouton_inscription' in POST:  # incription
    pseudo = POST['pseudo_inscr'][0]
    nom = POST['nom_inscr'][0]
    prenom = POST['prenom_inscr'][0]
    date_naiss = POST['date_naiss_inscr'][0]

    nouvel_id = insert_joueur_humain(SESSION['CONNEXION'], pseudo, nom, prenom, date_naiss)

    if nouvel_id and nouvel_id > 0:
        REQUEST_VARS['message'] = f"Inscription réussie."
        REQUEST_VARS['message_class'] = "alert-succes"

        joueur = get_joueur_by_id(SESSION['CONNEXION'], nouvel_id)
        if joueur:
            SESSION['JOUEUR_COURANT'] = joueur 
            REQUEST_VARS['connexion_reussie'] = True
    else: 
        REQUEST_VARS['message'] = f"Erreur lors de l'inscription."
        REQUEST_VARS['message_class'] = "alert-error"