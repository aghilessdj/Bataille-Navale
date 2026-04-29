'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from controleurs.includes import add_activity
from model.model_pg import get_classement

add_activity(SESSION['HISTORIQUE'], "Consultation du classement")

if SESSION.get('JOUEUR_COURANT'):
    id_joueur = SESSION['JOUEUR_COURANT']['idj']
    conn = SESSION['CONNEXION']

    REQUEST_VARS['classement'] = get_classement(conn)
    print(REQUEST_VARS['classement'])
    REQUEST_VARS['acces_refuse'] = False

else:
    REQUEST_VARS['acces_refuse'] = True
    REQUEST_VARS['message'] = "Accès refusé. Veuillez vous identifier."
    REQUEST_VARS['message_class'] = "alert-error"
