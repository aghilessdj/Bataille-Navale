'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from model.model_pg import get_parties_en_cours, get_adversaires_virtuels, insert_joueur_virtuel
from controleurs.includes import add_activity

add_activity(SESSION['HISTORIQUE'], "Consultation des parties")

if SESSION.get('JOUEUR_COURANT'):
    # On récupère l'ID du joueur connecté
    id_joueur = SESSION['JOUEUR_COURANT']['idj']
    # On récupère ses parties via le modèle
    conn = SESSION['CONNEXION']
    REQUEST_VARS['acces_refuse'] = False

    if POST and 'bouton_creer_bot' in POST:
        pseudo_bot = POST['pseudo_bot'][0]
        niveau_bot = POST['niveau_bot'][0]

        nouvel_id = insert_joueur_virtuel(conn, pseudo_bot, niveau_bot, id_joueur)
        if nouvel_id:
            REQUEST_VARS['message'] = f"Nouvelle IA '{pseudo_bot}' crée avec succès."
            REQUEST_VARS['message_class'] = "alert-succes"
        else:
            REQUEST_VARS['message'] = f"Echec lors de la création de l'IA"
            REQUEST_VARS['message_class'] = "alert-error"

    REQUEST_VARS['mes_parties'] = get_parties_en_cours(conn, id_joueur)
    print(SESSION.get('mes_parties'))
    REQUEST_VARS['bots_disponibles'] = get_adversaires_virtuels(conn)

else:
    REQUEST_VARS['acces_refuse'] = True
    REQUEST_VARS['message'] = "Accès refusé. Veuillez vous identifier."
    REQUEST_VARS['message_class'] = "alert-error"