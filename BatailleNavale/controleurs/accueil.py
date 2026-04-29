'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from model.model_pg import get_parties_finies_3mois, get_victoires_par_niveau, get_moyenne_tours_parties, get_pts_cumules_2026, get_cartes_tirees_type, get_etoile_mort_recentes
from controleurs.includes import add_activity

# On enregistre le passage sur l'accueil dans l'historique
add_activity(SESSION['HISTORIQUE'], "Consultation de la page d'accueil")


if SESSION.get('JOUEUR_COURANT'):
    id_joueur = SESSION['JOUEUR_COURANT']['idj']
    conn = SESSION['CONNEXION']

    REQUEST_VARS['stat_parties_3m'] = get_parties_finies_3mois(conn, id_joueur)
    REQUEST_VARS['stat_victoires'] = get_victoires_par_niveau(conn, id_joueur)
    REQUEST_VARS['stat_moyenne_tours'] = get_moyenne_tours_parties(conn, id_joueur)
    REQUEST_VARS['stat_points_2026'] = get_pts_cumules_2026(conn, id_joueur)
    REQUEST_VARS['stat_cartes'] = get_cartes_tirees_type(conn, id_joueur)
    REQUEST_VARS['stat_etoile_mort'] = get_etoile_mort_recentes(conn)
    REQUEST_VARS['acces_refuse'] = False

else:
    REQUEST_VARS['acces_refuse'] = True
    REQUEST_VARS['message'] = "Accès refusé. Veuillez vous identifier."
    REQUEST_VARS['message_class'] = "alert-error"