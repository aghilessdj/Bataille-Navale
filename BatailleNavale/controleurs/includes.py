'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

"""
Ficher includes chargé avant chaque requête (ex, fonctions utilisées par différents controleurs)
"""
import random
from model.model_pg import get_placements_joueur_partie, update_etat_bateau, get_tirs_joueur_partie, inserer_tir, get_partie_by_id, modifier_stats_tour, get_bateau_touches, deplacer_et_reparer_bateau, couler_plus_petits_bateaux

def add_activity(session_histo, activity):
    """
    Ajoute l'activité activity dans l'historique de session avec la date courante (comme clé)
    """
    from datetime import datetime
    session_histo.append({
        'date': datetime.now(),
        'description': activity
    })

def generer_flotte_virtuelle(types_bateaux):
    """
    Génère les palcementes aléatoires pour les bateaux du joueur virtuel
    """
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    cases_occupees = set()
    placements = []

    for bateau in types_bateaux:
        taille = bateau['taille_bat']
        place = False 

        while not place:
            sens = random.choice(['H', 'V'])
            x_start = random.randint(1, 10)
            y_idx_start = random.randint(0, 9)

            cases_potentielles = set()
            valide = True 

            for i in range(taille):
                if sens == 'H':
                    x_courant = x_start + i
                    y_courant = y_idx_start 
                else:
                    x_courant = x_start 
                    y_courant = y_idx_start + i

                if x_courant > 10 or y_courant > 9:
                    valide = False 
                    break

                coord = f"{lettres[y_courant]}{x_courant}"

                if coord in cases_occupees:
                    valide = False
                    break

                cases_potentielles.add(coord)

            if valide:
                cases_occupees.update(cases_potentielles)
                placements.append({
                    'type_bat': bateau['type_bat'],
                    'xy': f"{lettres[y_idx_start]}{x_start}",
                    'sens': sens,
                    'nom_bat': f"{bateau['type_bat']} IA"
                })
                place = True 
    return placements

def preparer_composition_flotte(catalogue_db):
    """
    Construit la liste exhaustive des navires à déployer pour une partie standard.
    Associe la composition canonique aux tailles issues du référentiel de la base de données.
    """
    tailles = {navire['type_bat']: navire['taille_bat'] for navire in catalogue_db}
    
    noms_requis = [
        'porte-avion', 
        'croiseur', 
        'contre-torpilleur', 
        'contre-torpilleur', 
        'torpilleur'
    ]
    
    composition = []
    for nom in noms_requis:
        if nom in tailles:
            composition.append({'type_bat': nom, 'taille_bat': tailles[nom]})
        else:
            logger.error(f"Navire {nom} introuvable dans le catalogue SQL.")
            
    return composition

def calculer_occupation_bateau(xy_db, sens, taille):
    """
    Détermine l'ensemble des coordonnées alphanumériques couvertes pas un bateau
    """
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    if ';' in xy_db:
        x_str, y_str = xy_db.split(';')
        x_depart = int(x_str)
        idx_y = lettres.index(y_str.upper())
    else:
        y_str = xy_db[0].upper()
        x_depart = int(xy_db[1:])
        idx_y = lettres.index(y_str)

    coordonnees_occupees = []

    for i in range(taille):
        if sens == 'H':
            coordonnees_occupees.append(f"{lettres[idx_y]}{x_depart + i}")
        else:
            if idx_y + i < len(lettres):
                coordonnees_occupees.append(f"{lettres[idx_y + i]}{x_depart}")

    return coordonnees_occupees

def generer_etats_grilles(connexion, id_partie, id_joueur, id_adversaire):
    """
    Reconstruit l'état des deux grilles sous forme de dictionnaires
    en croisant les placements et l'historique des tirs
    """
    grille_joueur = {}
    grille_adverse = {}

    placements_joueur = get_placements_joueur_partie(connexion, id_partie, id_joueur)
    tirs_adversaire = get_tirs_joueur_partie(connexion, id_partie, id_adversaire)

    bateaux_joueurs_coords = {}
    if placements_joueur:
        for bateau in placements_joueur:
            coords = calculer_occupation_bateau(bateau['xy'], bateau['sens'], bateau['taille_bat'])
            for c in coords:
                bateaux_joueurs_coords[c] = bateau['etat']
                grille_joueur[c] = 'bateau'

                if bateau['etat'] == 'coulé':
                    grille_joueur[c] = 'coule'

    if tirs_adversaire:
        for tir in tirs_adversaire:
            coord_cible = f"{tir['lettre'].strip().upper()}{tir['chiffre']}"
            if coord_cible in bateaux_joueurs_coords:
                etat_actuel = bateaux_joueurs_coords[coord_cible]
                grille_joueur[coord_cible] = 'coule' if etat_actuel == 'coulé' else 'touche'
            else:
                grille_joueur[coord_cible] = 'rate'

    placements_adversaire = get_placements_joueur_partie(connexion, id_partie, id_adversaire)
    tirs_joueur = get_tirs_joueur_partie(connexion, id_partie, id_joueur)

    bateaux_adverses_coords = {}
    if placements_adversaire:
        for bateau in placements_adversaire:
            coords = calculer_occupation_bateau(bateau['xy'], bateau['sens'], bateau['taille_bat'])
            for c in coords:
                bateaux_adverses_coords[c] = bateau['etat']
                if bateau['etat'] == 'coulé':
                    grille_adverse[c] = 'coule'

    if tirs_joueur:
        for tir in tirs_joueur:
            coord_cible = f"{tir['lettre'].strip().upper()}{tir['chiffre']}"
            if coord_cible not in grille_adverse or grille_adverse[coord_cible] != 'coule':
                if coord_cible in bateaux_adverses_coords:
                    etat_actuel = bateaux_adverses_coords[coord_cible]
                    grille_adverse[coord_cible] = 'coule' if etat_actuel == 'coulé' else 'touche'
                else:
                    grille_adverse[coord_cible] = 'rate'

    return grille_joueur, grille_adverse


def transformer_tir_selon_carte(coord_x, coord_y, code_carte):
    """
    Transforme un point d'impact central en une liste de cibles selon la carte
    """
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    if coord_y not in lettres:
        return []

    y_idx = lettres.index(coord_y)
    cibles = []

    if code_carte == 'C_MEGA':
        # 9 cases (le point central + 8 adjacentes)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = coord_x + dx
                ny_idx = y_idx + dy
                if 1 <= nx <= 10 and 0 <= ny_idx <= 9:
                    cibles.append((nx, lettres[ny_idx]))
                    
    elif code_carte == 'C_ETOILE':
        # 25 cases
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                nx = coord_x + dx
                ny_idx = y_idx + dy
                if 1 <= nx <= 10 and 0 <= ny_idx <= 9:
                    cibles.append((nx, lettres[ny_idx]))
                    
    elif code_carte in ['C_PASSE', 'C_OUPS']:
        # Cartes pièges : le tir initial est annulé / redirigé
        return []
        
    else:
        # C_MISSILE, C_VIDE et autres comportements par défaut : 1 case
        cibles.append((coord_x, coord_y))
        
    return cibles

def evaluer_et_enregistrer_tir(connexion, id_partie, id_tireur, id_cible, coord_x, coord_y, num_tour, carte_utilisee):
    """
    Execution du tir (simple ou multiple selon la carte), renvoie true si au moins un impact a touché, false sinon
    """
    code_carte = carte_utilisee['code'] if carte_utilisee else 'C_MISSILE'
    id_carte = carte_utilisee['idc'] if carte_utilisee else None

    cibles = transformer_tir_selon_carte(coord_x, coord_y, code_carte)
    placements_cible = get_placements_joueur_partie(connexion, id_partie, id_cible)

    touches_tour = 0
    coules_tour = 0
    willy = False

    for cx, cy in cibles:
        # Enregistrement en base de chaque sous-tir
        inserer_tir(connexion, id_carte, id_tireur, id_partie, num_tour, cx, cy)
        coord_visee = f"{cy}{cx}"

        if placements_cible:
            for bateau in placements_cible:
                coords_bateau = calculer_occupation_bateau(bateau['xy'], bateau['sens'], bateau['taille_bat'])
                
                if coord_visee in coords_bateau:                    
                    if bateau['etat'] != 'coulé':
                        touches_tour += 1
                        
                    if bateau['etat'] == 'opérationnel':
                        update_etat_bateau(connexion, id_partie, id_cible, bateau['xy'], 'touché')
                        bateau['etat'] = 'touché'

                        if bateau['type_bat'] == 'Orque':
                            couler_plus_petits_bateaux(connexion, id_partie, id_tireur, 3)
                            willy = True

                    if verifier_et_couler_bateau(connexion, id_partie, id_tireur, id_cible, bateau):
                        coules_tour += 1
                        bateau['etat'] = 'coulé'
                        
    if touches_tour > 0 or coules_tour > 0:
        partie = get_partie_by_id(connexion, id_partie)
        type_joueur = 'humain' if partie['idj_humain'] == id_tireur else 'virtuel'
        modifier_stats_tour(connexion, id_partie, num_tour, type_joueur, touches_tour, coules_tour)

    return touches_tour, coules_tour, willy

def obtenir_cibles_potentielles_grille(grille_vue_par_bot):
    """
    Renvoie les cases non explorées par le bot
    """
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    potentielles = []
    
    for y_idx, lettre in enumerate(lettres):
        for x in range(1, 11):
            coord = f"{lettre}{x}"
            etat = grille_vue_par_bot.get(coord, 'eau')
            if etat in ['eau', 'bateau']: 
                if (x + y_idx) % 2 == 0:
                    potentielles.append(coord)
                    
    if not potentielles:
        for y_idx, lettre in enumerate(lettres):
            for x in range(1, 11):
                coord = f"{lettre}{x}"
                if grille_vue_par_bot.get(coord, 'eau') in ['eau', 'bateau']:
                    potentielles.append(coord)
                    
    return potentielles

def obtenir_voisins_non_explores(coord, grille_vue_par_bot):
    """
    Retourne les coordonnées adjacentes et non explorées
    """
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    lettre = coord[0].upper()
    x = int(coord[1:])
    y_idx = lettres.index(lettre)
    
    voisins = []
    mouvements = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for dx, dy in mouvements:
        nx = x + dx
        ny_idx = y_idx + dy
        
        if 1 <= nx <= 10 and 0 <= ny_idx <= 9:
            n_coord = f"{lettres[ny_idx]}{nx}"
            if grille_vue_par_bot.get(n_coord, 'eau') in ['eau', 'bateau']:
                voisins.append(n_coord)
                
    return voisins

def choisir_cible_ia_intermediaire(grille_vue_par_bot):
    """
    Détermine la prochaine cible du bot, si navire touché alors il va chercher à terminer le navire
    sinon il cherche les cibles potentielles
    """
    import random
    
    # 1. Rechercher des cibles touchées mais non coulées
    cases_touchees = [coord for coord, etat in grille_vue_par_bot.items() if etat == 'touche']
    
    cibles_voisines = []
    for coord in cases_touchees:
        voisins = obtenir_voisins_non_explores(coord, grille_vue_par_bot)
        cibles_voisines.extend(voisins)
        
    # Si on a des pistes chaudes, on tire au hasard parmi elles
    if cibles_voisines:
        return random.choice(cibles_voisines)
    
    # 2. Sinon, on repasse en mode chasse (grillle)
    cibles_damier = obtenir_cibles_potentielles_grille(grille_vue_par_bot)
    if cibles_damier:
        return random.choice(cibles_damier)
        
    return None

def choisir_cible_ia_impossible(connexion, id_partie, id_cible, id_tireur):
    """
    Détermine la prochaine cible du bot (toujours une case ou un bateau n'a pas été touché)
    """
    placements = get_placements_joueur_partie(connexion, id_partie, id_cible)
    tirs = get_tirs_joueur_partie(connexion, id_partie, id_tireur)

    coords_tirees = []
    if tirs:
        for t in tirs:
            coords_tirees.append(f"{t['lettre'].strip().upper()}{t['chiffre']}")

    cibles_valides = []
    if placements:
        for bat in placements:
            if bat['etat'] != 'coulé':
                coords = calculer_occupation_bateau(bat['xy'], bat['sens'], bat['taille_bat'])
                for c in coords:
                    if c not in coords_tirees:
                        cibles_valides.append(c)

    if cibles_valides:
        return random.choice(cibles_valides)
    return None

def verifier_et_couler_bateau(connexion, id_partie, id_tireur, id_cible, bateau):
    """
    Vérifie si un bateau a été coulé et met à jour la base de données
    """
    coords_bateau = calculer_occupation_bateau(bateau['xy'], bateau['sens'], bateau['taille_bat'])
    tirs_tireur = get_tirs_joueur_partie(connexion, id_partie, id_tireur)
    
    coords_tires = []
    if tirs_tireur:
        coords_tires = [f"{tir['lettre'].strip().upper()}{tir['chiffre']}" for tir in tirs_tireur]
        
    # Si chaque case du bateau figure dans l'historique des tirs
    if all(c in coords_tires for c in coords_bateau):
        update_etat_bateau(connexion, id_partie, id_cible, bateau['xy'], 'coulé')
        return True
    return False

def verifier_fin_partie(connexion, id_partie, id_cible):
    """
    Vérifie si tous les bateaux d'un joueur sont coulés
    """
    placements = get_placements_joueur_partie(connexion, id_partie, id_cible)
    if placements:
        return all(bateau['etat'] == 'coulé' for bateau in placements)
    return False

def determiner_etape_apres_pioche(carte, id_partie, id_joueur, conn):
    ''' Détermine la prochaine action requise après que le joueur ait pioché '''
    if not carte: 
        return 'attente_tir_joueur'
    
    code = carte['code']
    if code in ['C_LEURRE', 'C_WILLY']:
        return 'attente_placement_bonus'
    elif code == 'C_VIDE':
        return 'attente_verification_vide'
    elif code == 'C_MPM':
        touches = get_bateau_touches(conn, id_partie, id_joueur)
        if touches:
            return 'attente_selection_bateau_mpm'
        return 'attente_tir_joueur'
    elif code =='C_PASSE':
        return 'attente_passe_tour'
    elif code == 'C_OUPS':
        return 'attente_oups'
    
    return 'attente_tir_joueur'


def appliquer_effet_oups(connexion, id_partie, id_joueur):
    """
    Sélectionne au hasard un bateau opérationnel du joueur pour lui appliquer un dégat
    """
    query = """
        SELECT xy
        FROM Placements
        WHERE idp = %s AND etat = 'opérationnel'
        ORDER BY RANDOM()
        LIMIT 1
    """
    placements = get_placements_joueur_partie(connexion, id_partie, id_joueur)
    tirs_subis = get_tirs_joueur_partie(connexion, id_partie, id_adversaire)

    coords_bateaux = []
    for bat in placements:
        if bat['etat'] != 'coulé':
            coords = calculer_occupation_bateau(bat['xy'], bat['sens'], bat['taille_bat'])
            for c in coords:
                coords_bateaux.append(c)

    coords_tires = []
    if tirs_subis:
        for tir in tirs_subis:
            coords_tires.append(f"{tir['lettre'].strip().upper()}{tir['chiffre']}")

    cases_intactes = [c for c in coords_bateaux if c not in coords_tires]

    if cases_intactes:
        coord_choisie = random.choice(cases_intactes)
        lettre = coord_choisie[0]
        chiffre = int(coord_choisie[1:])

        evaluer_et_enregistrer_tir(connexion, id_partie, id_adversaire, id_joueur, chiffre, lettre, num_tour, None)
        return True
    
    return False
