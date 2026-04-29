'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from logzero import logger

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            cursor.row_factory = dict_row
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)

def get_joueurs_by_pseudo(connexion, pseudo):
    """
    Retourne les joueurs dont le pseudo = la chaine de caractères fournie
    string pseudo : le pseudo recherché dans la table Joueur
    """
    query = sql.SQL("SELECT j.idJ, j.pseudo FROM Joueur j Where j.pseudo ILIKE {} AND j.estVirtuel = false").format(
        sql.Placeholder()
    )
    return execute_select_query(connexion, query, ["%" + pseudo + "%"])

def get_joueur_by_id(connexion, id_joueur):
    """
    Extrait les informations du joueur ayant l'id id_joueur
    """
    query = sql.SQL("SELECT * FROM Joueur j WHERE j.idj = {}").format(
        sql.Placeholder()
    )
    res = execute_select_query(connexion, query, [id_joueur])
    if res and len(res) > 0:
        return res[0]
    return None

def insert_joueur_humain(connexion, pseudo, nom, prenom, date_naissance):
    """
    Insère un nouveau joueur humain dans la base de données
    """
    query = """
        WITH nouveau_joueur AS (
            INSERT INTO Joueur (pseudo, estVirtuel)
            VALUES (%s, false)
            RETURNING idJ
        )
        INSERT INTO Humain (idJ, nom, prenom, date_naissance)
        SELECT idJ, %s, %s, %s
        FROM nouveau_joueur
        RETURNING idJ;
    """
    res = execute_select_query(connexion, query, [pseudo, nom, prenom, date_naissance])
    if res:
        return res[0]['idj']
    return None

def get_parties_finies_3mois(connexion, id_joueur):
    """
    Compte le nombre de parties terminées par le joueur d'id id_joueur
    durant les 3 derniers mois
    """
    query = """
        SELECT COUNT (DISTINCT p.idp) as total 
        FROM partie p 
        JOIN sequencetemporelle s ON p.idp = s.idp
        WHERE p.etat IN ('Gagnée', 'Perdue', 'Terminé') AND p.idj_humain = %s AND s.date_fin >= CURRENT_DATE - INTERVAL '3 months'
        """
    res = execute_select_query(connexion, query, [id_joueur])
    if res:
        return res[0]['total']
    else: 
        return 0

def get_classement(connexion):
    """
    Rencoie le classement des joueurs humains sur le nombre des parties gagnés
    """
    query = """
        SELECT j.idj, j.pseudo, COUNT(p.idj_gagnant) as Nb_victoire
        FROM joueur j 
        join partie p on j.idj=p.idj_gagnant
        GROUP BY j.idj, j.pseudo
        ORDER BY Nb_victoire DESC;
        """
    res = execute_select_query(connexion, query)
    if res:
        return res
    else: 
        return None

def get_victoires_par_niveau(connexion, id_joueur):
    """
    Compte le nombre de parties gagnées par le joueur désigné par l'id id_joueur
    et renvoie le nombre de victoire groupé à la difficulté de l'IA
    """
    query = """
        SELECT v.niveau_expertise, COUNT(p.idp) as nb_victoires
        FROM partie p
        JOIN virtuel v ON p.idj_virtuel = v.idj
        WHERE p.idj_humain = %s AND p.idj_gagnant = %s
        GROUP BY v.niveau_expertise
        ORDER BY v.niveau_expertise
        """
    return execute_select_query(connexion, query, [id_joueur, id_joueur])

def get_moyenne_tours_parties(connexion, id_joueur):
    """
    Calcule la moyenne du nombre de tours pour l'ensemble des parties
    du joueur ayant l'id id_joueur
    """
    query = """
        SELECT AVG(compte_tours.nb) as moyenne
        FROM (
            SELECT t.idp, MAX(t.numt) as nb
            FROM tour t
            JOIN partie p ON t.idp = p.idp
            WHERE p.idj_humain = %s
            GROUP BY t.idp   
        ) as compte_tours
        """
    res = execute_select_query(connexion, query, [id_joueur])
    if res and res[0]['moyenne']:
        return res[0]['moyenne']
    else:
        return 0

def get_pts_cumules_2026(connexion, id_joueur):
    """
    Somme des scores finaux des parties du joueur ayant l'id id_joueur possédant 
    au moins une séquence démarrée en 2026
    """
    query = """
        SELECT SUM(p.score_final) as total_points
        FROM partie p
        JOIN sequencetemporelle s ON p.idp = s.idp
        WHERE p.idj_humain = %s AND EXTRACT(YEAR FROM s.date_debut) = 2026
        """
    res = execute_select_query(connexion, query, [id_joueur])
    if res:
        return res[0]['total_points']
    else:
        return 0

def get_cartes_tirees_type(connexion, id_joueur):
    """
    Compte la fréquence d'apparition de chaque type de carte piochée par le joueur.
    """
    query = """
        SELECT tc.nom as type_carte, COUNT(t.idc) as nb_tirages
        FROM Tir t
        JOIN Carte c ON t.idc = c.idc
        JOIN TypeCarte tc ON c.code = tc.code
        WHERE t.idj = %s
        GROUP BY tc.nom
        ORDER BY nb_tirages desc
    """
    return execute_select_query(connexion, query, [id_joueur])

def get_etoile_mort_recentes(connexion):
    """
    Compte le nombre de cartes 'etoile de la mort' tirées lors des
    10 dernières parties globales
    """
    query = """
        WITH DixDernieres AS (
        SELECT p.idp, p.idpi
        FROM partie p
        JOIN sequencetemporelle s ON p.idp = s.idp
        ORDER BY s.date_debut DESC
        LIMIT 10
        )
        SELECT COUNT(a.idc) as total
        FROM appartient a
        JOIN DixDernieres d ON a.idpi = d.idpi
        JOIN carte c on a.idc = c.idc
        WHERE c.code = 'C_ETOILE' AND a.etat = 'utilisée'
    """
    res = execute_select_query(connexion, query)
    if res:
        return res[0]['total']
    else:
        return 0

def get_parties_joueur(connexion, id_joueur):
    """
    Récupère la liste des parties du joueur ayant id_joueur
    Affiche l'ID de la partie, l'état, le score et le pseudo de l'adversaire
    """
    query = """
        SELECT p.idP, p.etat, p.score_final, j.pseudo AS adversaire
        FROM navbat.Partie p
        JOIN navbat.Joueur j ON p.idJ_Virtuel = j.idJ
        WHERE p.idJ_Humain = %s
        ORDER BY p.idP DESC;
    """
    return execute_select_query(connexion, query, [id_joueur])

def get_parties_en_cours(connexion, id_joueur):
    """ 
    Récupère les informations des parties en cours du joueur ayant l'id id_joueur
    """
    query = """
        WITH PremiereSequence AS (
            SELECT s.idp, MIN(s.date_debut) as date_creation, MIN(to_char (heure_debut, 'HH24:MI')) as heure_creation
            FROM sequencetemporelle s
            GROUP BY s.idp
        ), 
        StatsTours AS (
            SELECT t.idp, MAX(t.numt) as max_tour,
                SUM(t.nb_coulés_hum) as nb_coulés_hum, 
                SUM(t.nb_touchés_hum) as nb_touchés_hum, 
                SUM(t.nb_coulés_virt) as nb_coulés_virt, 
                SUM(t.nb_touchés_virt) as nb_touchés_virt 
            FROM tour t
            GROUP BY t.idp
        )
        SELECT p.idp, ps.date_creation, ps.heure_creation, v.niveau_expertise as nv, 
        COALESCE(st.max_tour, 0) as nb_tours, 
        COALESCE(st.nb_coulés_hum, 0) as coules_hum, 
        COALESCE(st.nb_touchés_hum, 0) as touches_hum, 
        COALESCE(st.nb_coulés_virt, 0) as coules_virt, 
        COALESCE(st.nb_touchés_virt, 0) as touches_virt
        FROM partie p
        JOIN PremiereSequence ps ON p.idp = ps.idp
        JOIN virtuel v ON p.idj_virtuel = v.idj
        LEFT JOIN StatsTours st ON p.idp = st.idp
        LEFT JOIN tour t ON p.idp = t.idp AND t.numt = st.max_tour
        WHERE p.idj_humain = %s AND p.etat IN ('En cours', 'Suspendue')
        ORDER BY ps.date_creation DESC, ps.heure_creation DESC
    """
    return execute_select_query(connexion, query, [id_joueur])

def get_adversaires_virtuels(connexion):
    """
    Récupère la liste des joueurs virtuels
    """
    query = """
        SELECT j.idj, j.pseudo, v.niveau_expertise
        FROM joueur j
        JOIN virtuel v ON j.idj = v.idj
        WHERE j.estVirtuel = true
        ORDER BY v.niveau_expertise, j.pseudo
    """
    return execute_select_query(connexion, query)

def insert_joueur_virtuel(connexion, pseudo, niveau, id_createur):
    """
    Crée un nouveau joueur virtuel dans la base de données
    """
    query = """
        WITH nouveau_joueur AS (
            INSERT INTO joueur (pseudo, estVirtuel)
            VALUES (%s, true)
            RETURNING idj
        )
        INSERT INTO virtuel (idj, date_creation, idj_createur, niveau_expertise)
        SELECT idj, CURRENT_DATE, %s, %s
        FROM nouveau_joueur
        RETURNING idj;
    """
    res = execute_select_query(connexion, query, [pseudo, id_createur, niveau])
    if res:
        return res[0]['idj']
    return None 

def nouvelle_partie(connexion, idj_humain, idj_virt, id_distrib=1):
    """
    Création d'une nouvelle partie
    """
    query_id_pioche = "SELECT COALESCE(MAX(idpi), 0) + 1 AS next_id FROM pioche"
    query_insert_pioche = "INSERT INTO Pioche (idpi, idd) VALUES (%s, %s)"

    query_id_partie = "SELECT COALESCE(MAX(idp), 0) + 1 AS next_id FROM Partie"
    query_insert_partie = """
        INSERT INTO Partie (idp, etat, idj_virtuel, idj_humain, score_final, idpi)
        VALUES (%s, 'Créée', %s, %s, 0, %s)
    """

    query_insert_sequence = """
        INSERT INTO sequencetemporelle (idp, date_debut, heure_debut)
        VALUES (%s, CURRENT_DATE, CURRENT_TIME)
    """

    with connexion.cursor() as cursor:
        try:
            cursor.execute(query_id_pioche)
            next_id_pioche = cursor.fetchone()[0]
            cursor.execute(query_insert_pioche, [next_id_pioche, id_distrib])

            cursor.execute(query_id_partie)
            next_id_partie = cursor.fetchone()[0]
            cursor.execute(query_insert_partie, [next_id_partie, idj_virt, idj_humain, next_id_pioche])

            cursor.execute(query_insert_sequence, [next_id_partie])

            connexion.commit()
            generer_pioche_partie(connexion, next_id_pioche, id_distrib)
            return next_id_partie

        except psycopg.Error as e:
            logger.error(f"Echec critique de l'initialisation de la partie : {e}")
            connexion.rollback()
            return None

def get_catalogue_bateaux(connexion):
    """
    Récupère les types de bateaux et leur longueurs
    """
    query = "SELECT type_bat, taille_bat FROM typebateau"
    return execute_select_query(connexion, query)

def placer_bateaux(connexion, id_partie, idj, placements, pavillon='FRA'):
    """
    Place les bateaux pour un joueur donné
    """
    query = """
        INSERT INTO Placements (idp, idj, xy, sens, type_bat, nom_bat, etat, pavillon)
        VALUES (%s, %s, %s, %s, %s, %s, 'opérationnel', %s)
    """

    params_list = [
        (id_partie, idj, p['xy'], p['sens'], p['type_bat'], p['nom_bat'], pavillon)
        for p in placements
    ]

    with connexion.cursor() as cursor:
        try:
            cursor.executemany(query, params_list)
            connexion.commit()
            return True 
        except psycopg.Error as e:
            logger.error(f"Erreur lors du placement des bateaux : {e}")
            connexion.rollback()
            return False

def search_in_table(connexion, table_name, column_name, term):
    """
    Recherche avec motif partiel.
    """
    motif = f"%{term}%"
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(table_name.lower()),
        sql.Identifier(column_name.lower()),
        sql.Placeholder()
    )
    return execute_select_query(connexion, query, [motif])

def get_top_scores(connexion):
    """
    Récupère les 10 meilleurs scores avec le pseudo du joueur.
    """
    query = """
        SELECT j.pseudo, p.score_final 
        FROM navbat.Partie p
        JOIN navbat.Humain h ON p.idJ_Humain = h.idJ
        JOIN navbat.Joueur j ON h.idJ = j.idJ
        WHERE p.score_final IS NOT NULL
        ORDER BY p.score_final DESC
        LIMIT 10;
    """
    return execute_select_query(connexion, query)    

def get_recent_games_2026(connexion):
    """
    Récupère les 5 dernières parties ayant débuté en 2026.
    """
    query = """
        SELECT DISTINCT p.idP, j.pseudo, s.date_debut, p.etat 
        FROM NavBat.Partie p
        JOIN NavBat.Joueur j ON p.idJ_Humain = j.idJ
        JOIN NavBat.SequenceTemporelle s ON p.idP = s.idP
        WHERE s.date_debut >= '2026-01-01'
        ORDER BY s.date_debut DESC
        LIMIT 5;
    """
    return execute_select_query(connexion, query)

def get_table_like(connexion, nom_table, like_pattern):
    """
    Retourne les instances de la table nom_table dont le nom correspond au motif like_pattern
    String nom_table : nom de la table
    String like_pattern : motif pour une requête LIKE
    """
    motif = '%' + like_pattern + '%'
    nom_att = 'nom'  # nom attribut dans ingrédient 
    if nom_table == 'recette':  
        nom_att += '_recette'  # nom attribut dans recette 
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(nom_table),
        sql.Identifier(nom_att),
        sql.Placeholder())
    return execute_select_query(connexion, query, [motif])

def get_placements_joueur_partie(connexion, id_partie, id_joueur):
    """ 
    Récupère tous les navires placés par un joueur pour une partie
    """
    query = """
        SELECT p.xy, p.sens, p.etat, p.type_bat, tb.taille_bat
        FROM Placements p
        JOIN TypeBateau tb ON p.type_bat = tb.type_bat
        WHERE p.idP = %s AND p.idJ = %s
    """
    return execute_select_query(connexion, query, [id_partie, id_joueur])

def get_tirs_joueur_partie(connexion, id_partie, id_joueur_tireur):
    """
    Récupère les coordonnées sur lesquelles un joueur à tiré pendant une partie
    """
    query = """
        SELECT coordY as lettre, coordX as chiffre, idC as id_carte
        FROM Tir
        WHERE idP = %s AND idJ = %s
        ORDER BY numT ASC, numTi ASC
    """
    return execute_select_query(connexion, query, [id_partie, id_joueur_tireur])

def get_adversaire_partie(connexion, id_partie, id_joueur):
    """
    Retourne l'ID de l'adversaire dans une partie
    """
    query = "SELECT idJ_Virtuel, idJ_Humain FROM Partie WHERE idP = %s"
    res = execute_select_query(connexion, query, [id_partie])
    if res:
        partie = res[0]
        return partie['idj_virtuel'] if partie['idj_humain'] == id_joueur else partie['idj_humain']
    return None

def inserer_tir(connexion, id_carte, id_joueur, id_partie, num_tour, coord_x, coord_y):
    """
    Ajoute un tir dans la table Tir en calculant le numTi automatiquement
    """
    query_max = "SELECT COALESCE(MAX(numTi), 0) + 1 AS next_ti FROM Tir WHERE idP = %s AND numT = %s"
    res_max = execute_select_query(connexion, query_max, [id_partie, num_tour])
    next_ti = res_max[0]['next_ti'] if res_max else 1

    query = """
        INSERT INTO Tir (idC, idJ, idP, numT, numTi, coordX, coordY)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return execute_other_query(connexion, query, [id_carte, id_joueur, id_partie, num_tour, next_ti, coord_x, coord_y])

def creer_nouveau_tour(connexion, id_partie, num_tour):
    """
    Initialise une nouvelle ligne dans la table Tour lors du changement de cycle.
    """
    query = """
        INSERT INTO Tour (idP, numT, nb_coulés_hum, nb_touchés_hum, nb_cell_libres_hum, nb_coulés_virt, nb_touchés_virt, nb_cell_libres_virt) 
        VALUES (%s, %s, 0, 0, 0, 0, 0, 0)
    """
    return execute_other_query(connexion, query, [id_partie, num_tour])

def update_etat_bateau(connexion, id_partie, id_joueur, xy_depart, nouvel_etat):
    """
    Change le statut d'un bateau 
    """
    query = """
        UPDATE Placements
        SET etat = %s
        WHERE idP = %s AND idJ = %s AND xy = %s
    """
    return execute_other_query(connexion, query, [nouvel_etat, id_partie, id_joueur, xy_depart])

def demarrer_partie(connexion, id_partie):
    """
    Crée une partie en base de données et commence le premier tour
    """
    query_etat = "UPDATE Partie SET etat = 'En cours' WHERE idP = %s"
    query_tour = "INSERT INTO Tour (idP, numT, nb_coulés_hum, nb_touchés_hum, nb_cell_libres_hum, nb_coulés_virt, nb_touchés_virt, nb_cell_libres_virt) VALUES (%s, 1, 0, 0, 0, 0, 0, 0)"
    
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query_etat, [id_partie])
            cursor.execute(query_tour, [id_partie])
            connexion.commit()
            return True
        except psycopg.Error as e:
            logger.error(f"Erreur au démarrage de la partie : {e}")
            connexion.rollback()
            return False

def get_partie_by_id(connexion, id_partie):
    """
    Récupère les informations d'une partie
    """
    query = "SELECT idP, etat, idJ_Virtuel, idJ_Humain, idPi FROM Partie WHERE idP = %s"
    res = execute_select_query(connexion, query, [id_partie])
    return res[0] if res else None

def get_dernier_tour_partie(connexion, id_partie):
    """
    Récupère le numéro du dernier tour enregistré pour une partie donnée
    """
    query = "SELECT MAX(numT) as dernier_tour FROM Tour WHERE idP = %s"
    res = execute_select_query(connexion, query, [id_partie])
    return res[0]['dernier_tour'] if res and res[0]['dernier_tour'] else 1

def piocher_carte(connexion, id_partie):
    """
    Pioche une carte aléatoirement
    """
    query = """
        WITH CarteTiree AS (
            SELECT a.idc
            FROM Appartient a
            JOIN Partie p ON a.idPi = p.idpi
            WHERE p.idP = %s AND (a.etat IS NULL OR a.etat = 'Dans la pioche')
            ORDER BY RANDOM()
            LIMIT 1
        ),
        UpdateCarte AS (
            UPDATE Appartient
            SET etat = 'utilisée'
            WHERE idc = (SELECT idc FROM CarteTiree)
            RETURNING idc
        )
        SELECT c.idc, tc.nom, c.code, tc.description, tc.image
        FROM UpdateCarte uc JOIN Carte c ON uc.idc = c.idc 
        JOIN typecarte tc ON c.code = tc.code
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, [id_partie])
            from psycopg.rows import dict_row
            cursor.row_factory = dict_row
            carte = cursor.fetchone()
            connexion.commit()
            return carte
        except Exception as e:
            from logzero import logger
            logger.error(e)
            connexion.rollback()
    return None
    
def generer_pioche_partie(connexion, id_pioche, id_distrib):
    """
    Génère une pioche
    """
    query_distrib = "SELECT * FROM Distribution WHERE idd = %s"
    distrib = execute_select_query(connexion, query_distrib, [id_distrib])[0]

    cartes_a_creer = {
        'C_MISSILE': distrib['c_missile'],
        'C_REJOUE': distrib['c_rejoue'],
        'C_VIDE': distrib['c_vide'],
        'C_MPM': distrib['c_mpm'],
        'C_LEURRE': distrib['c_leurre'],
        'C_WILLY': distrib['c_willy'],
        'C_MEGA': distrib['c_mega'],
        'C_ETOILE': distrib['c_etoile'],
        'C_PASSE': distrib['c_passe'],
        'C_OUPS': distrib['c_oups']
    }
    query_max_carte = "SELECT COALESCE(MAX(idc), 0) AS max FROM Carte"
    res_max = execute_select_query(connexion, query_max_carte)
    max_id = res_max[0]['max'] if res_max else 0

    cartes_insert = []
    appartient_insert = []
    rang = 1

    for code, quantite in cartes_a_creer.items():
            for _ in range(quantite):
                max_id += 1
                cartes_insert.append((max_id, code))
                appartient_insert.append((max_id, id_pioche, rang, 'Dans la pioche'))
                rang += 1

    query_insert_carte = "INSERT INTO Carte (idc, code) VALUES (%s, %s)"
    query_insert_appartient = "INSERT INTO Appartient (idc, idpi, rang, etat) VALUES (%s, %s, %s, %s)"

    with connexion.cursor() as cursor:
        try:
            cursor.executemany(query_insert_carte, cartes_insert)
            cursor.executemany(query_insert_appartient, appartient_insert)
            connexion.commit()
        except Exception as e:
            from logzero import logger
            logger.error(e)
            connexion.rollback()

def terminer_partie(connexion, id_partie, id_gagnant, etat_fin):
    """
    Termine la partie en désignant un vainqueur
    """
    query = """
        UPDATE Partie 
        SET etat = %s, idJ_gagnant = %s, score_final = 100
        WHERE idP = %s
    """
    execute_other_query(connexion, query, [etat_fin, id_gagnant, id_partie])

def modifier_stats_tour(connexion, id_partie, num_tour, type_joueur, nb_touches, nb_coules):
    """
    Met à jour les stats de tirs touchés et coulés d'un joueur donné pour le tour donné
    """
    if nb_touches == 0 and nb_coules == 0:
        return True
    
    col_touche = 'nb_touchés_hum' if type_joueur == 'humain' else 'nb_touchés_virt'
    col_coule = 'nb_coulés_hum' if type_joueur == 'humain' else 'nb_coulés_virt'

    query = f"UPDATE Tour SET {col_touche} = {col_touche} + %s, {col_coule} = {col_coule} + %s WHERE idp = %s and numt = %s"
    return execute_other_query(connexion, query, [nb_touches, nb_coules, id_partie, num_tour])

def suspendre_partie(connexion, id_partie):
    """
    Met une partie à l'état suspendu
    """
    query = "UPDATE Partie SET etat = 'Suspendue' WHERE idp = %s"
    return execute_other_query(connexion, query, [id_partie])

def reprendre_partie(connexion, id_partie):
    """
    Met une partie à l'état en cours
    """
    query = "UPDATE Partie SET etat = 'En cours' WHERE idp = %s"
    return execute_other_query(connexion, query, [id_partie])

def placer_bonus(connexion, id_partie, id_joueur, coord_x, coord_y, type_bat):
    """
    Insère un bonus (leurre ou orque) dans la grille du joueur
    """
    sens = 'H' 
    xy = f"{coord_x};{coord_y}"
    nom_bat = "Leurre" if type_bat == 'Leurre' else 'Willy la petite orque'

    query = """
        INSERT INTO Placements (idp, idj, xy, sens, type_bat, nom_bat, etat, pavillon)
        VALUES (%s, %s, %s, %s, %s, %s, 'opérationnel', 'FRA')
    """
    return execute_other_query(connexion, query, [id_partie, id_joueur, xy, sens, type_bat, nom_bat])

def get_dernier_tir_partie(connexion, id_partie):
    """
    Récupère les coordonnées du dernier tir de la partie
    pour l'afficher lorsqu'on reprend la partie
    """
    query = """
        SELECT coordx, coordy, idj
        FROM Tir 
        WHERE idp = %s
        ORDER by numT DESC, numTi DESC
        LIMIT 1
    """
    resultats = execute_select_query(connexion, query, [id_partie])
    return resultats[0] if resultats else None

def get_bateau_touches(connexion, id_partie, id_joueur):
    query = "SELECT * FROM Placements WHERE idp = %s AND idj = %s AND etat = 'touché'"
    return execute_select_query(connexion, query, [id_partie, id_joueur])

def deplacer_et_reparer_bateau(connexion, id_partie, id_joueur, ancien_xy, nouveau_xy):
    query = "UPDATE Placements SET xy = %s, etat = 'opérationnel' WHERE idp = %s AND idj = %s and xy = %s"
    return execute_other_query(connexion, query, [nouveau_xy, id_partie, id_joueur, ancien_xy])

def couler_plus_petits_bateaux(connexion, id_partie, id_joueur, nombre = 3):
    """
    Coule les 3 navires de plus petite tailles qui ne sont pas encore détruits
    """
    query = """
        UPDATE Placements
        SET etat = 'coulé'
        WHERE (idp,  idj, xy) IN (
            SELECT p.idp, p.idj, p.xy
            FROM Placements p
            JOIN TypeBateau tb ON p.type_bat = tb.type_bat
            WHERE p.idp = %s AND p.idj = %s AND p.etat != 'coulé'
            ORDER BY tb.taille_bat ASC
            LIMIT %s
        )
    """

    return execute_other_query(connexion, query, [id_partie, id_joueur, nombre])

def get_niveau_bot(connexion, id_joueur_virtuel):
    """
    retourne le niveau d'expertise du bot
    """
    query = "SELECT niveau_expertise FROM Virtuel WHERE idj = %s"
    res = execute_select_query(connexion, query, [id_joueur_virtuel])
    return res[0]['niveau_expertise'] if res else None