'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from model.model_pg import search_in_table
from controleurs.includes import add_activity

add_activity(SESSION['HISTORIQUE'], "Utilisation de la recherche")

REQUEST_VARS['resultats'] = None

if POST and 'bouton_valider' in POST:
    table = POST['nom_table'][0]
    terme = POST['valeur'][0]
    #si else alors on regarde dans la table TypeCarte
    colonne = 'pseudo' if table == 'Joueur' else 'nom'

    resultats = search_in_table(SESSION['CONNEXION'], table, colonne, terme)
    
    if resultats:
        REQUEST_VARS['resultats'] = resultats
        REQUEST_VARS['champs'] = resultats[0].keys()
    else:
        REQUEST_VARS['message'] = f"Aucun résultat pour '{terme}'"
        REQUEST_VARS['message_class'] = "alert-warning"