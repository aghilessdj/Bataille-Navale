'''
VITTEAU Magdi 12511408
SAIDJ Aghiles 12511222
'''

from model.model_pg import nouvelle_partie, get_catalogue_bateaux, placer_bateaux, get_adversaire_partie, get_placements_joueur_partie, demarrer_partie, get_tirs_joueur_partie, get_partie_by_id, get_dernier_tour_partie, piocher_carte, creer_nouveau_tour, terminer_partie, reprendre_partie, suspendre_partie, placer_bonus, get_dernier_tir_partie, get_niveau_bot
from controleurs.includes import add_activity, generer_flotte_virtuelle, preparer_composition_flotte, generer_etats_grilles, evaluer_et_enregistrer_tir, choisir_cible_ia_intermediaire, verifier_fin_partie, determiner_etape_apres_pioche, calculer_occupation_bateau, choisir_cible_ia_impossible

add_activity(SESSION['HISTORIQUE'], "Consultation d'une partie en cours")

if SESSION.get('JOUEUR_COURANT'):
    id_joueur = SESSION['JOUEUR_COURANT']['idj']
    conn = SESSION['CONNEXION']
    REQUEST_VARS['acces_refuse'] = False 
    REQUEST_VARS['carte_active'] = SESSION.get('CARTE_ACTIVE')

    # Détection de l'identifiant de la partie pour charger l'état
    id_partie_active = None
    if GET and 'id' in GET:
        id_partie_active = int(GET['id'][0])
    elif POST and 'id_partie' in POST:
        id_partie_active = int(POST['id_partie'][0])
    elif POST and 'id_partie_reprise' in POST:
        id_partie_active = int(POST['id_partie_reprise'][0])

    # Reconstruction de l'état si une partie est active
    if id_partie_active:
        partie_data = get_partie_by_id(conn, id_partie_active)
        if partie_data:
            REQUEST_VARS['partie'] = {'idp': id_partie_active, 'etat': partie_data['etat']}
            REQUEST_VARS['num_tour'] = get_dernier_tour_partie(conn, id_partie_active)
            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)
            
            if partie_data['etat'] == 'En cours':
                if int(REQUEST_VARS.get('num_tour', 1)) % 2 != 0:
                    REQUEST_VARS['etape_tour'] = determiner_etape_apres_pioche(REQUEST_VARS['carte_active'], id_partie_active, id_joueur, conn)
                else:
                    REQUEST_VARS['etape_tour'] = 'attente_suivant_joueur'
            elif partie_data['etat'] == 'Créée':
                REQUEST_VARS['etape_tour'] = 'attente_commencer'
    else:
        REQUEST_VARS['grille_joueur'] = {}
        REQUEST_VARS['grille_adversaire'] = {}
    
    if POST and 'bouton_nouvelle_partie' in POST:
        id_adversaire = int(POST.get('id_adversaire')[0])
        
        id_partie = nouvelle_partie(conn, id_joueur, id_adversaire)

        if id_partie:
            catalogue = get_catalogue_bateaux(conn)
            bateaux_requis = preparer_composition_flotte(catalogue)

            placements_ia = generer_flotte_virtuelle(bateaux_requis)
            placer_bateaux(conn, id_partie, id_adversaire, placements_ia)

            placements_joueur = generer_flotte_virtuelle(bateaux_requis)
            placer_bateaux(conn, id_partie, id_joueur, placements_joueur)

            REQUEST_VARS['partie'] = {'idp': id_partie, 'etat': 'Créée'}
            REQUEST_VARS['num_tour'] = 0
            REQUEST_VARS['etape_tour'] = 'attente_commencer'
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie, id_joueur, id_adversaire)
            
            REQUEST_VARS['message'] = "Déploiement terminé. En attente de l'ordre d'engagement."
            REQUEST_VARS['message_class'] = "alert-success"

    elif POST and 'bouton_reprendre_partie' in POST:
        if id_partie_active:
            if reprendre_partie(conn, id_partie_active):
                REQUEST_VARS['partie']['idp'] = id_partie_active
                REQUEST_VARS['partie']['etat'] = 'En cours'
                REQUEST_VARS['num_tour'] = get_dernier_tour_partie(conn, id_partie_active)

                id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
                REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)
                
                dernier_tir = get_dernier_tir_partie(conn, id_partie_active)
                contexte_tir = ""
                if dernier_tir:
                    if str(dernier_tir['idj']) == str(id_joueur):
                        contexte_tir = f"Vous aviez tiré en {dernier_tir['coordy']}{dernier_tir['coordx']} la dernière fois."
                    else:
                        contexte_tir = f"L'adversaire avait tiré en {dernier_tir['coordy']}{dernier_tir['coordx']} la dernière fois."
                if REQUEST_VARS['num_tour'] % 2 == 0:
                    REQUEST_VARS['etape_tour'] = determiner_etape_apres_pioche(REQUEST_VARS['carte_active'], id_partie_active, id_joueur, conn)
                    carte = piocher_carte(conn, id_partie_active)
                    SESSION['CARTE_ACTIVE'] = carte
                    REQUEST_VARS['carte_active'] = carte
                
                    REQUEST_VARS['message'] = f"La partie a repris. C'est à vous de tirer. {contexte_tir}"
                    REQUEST_VARS['message_class'] = "alert-success"
                else: 
                    REQUEST_VARS['etape_tour'] = 'attente_suivant_joueur'
                    REQUEST_VARS['message'] = f"La partie a repris. C'est à l'adversaire de jouer. {contexte_tir}"
                    REQUEST_VARS['message_class'] = "alert-success"
            
            else:
                REQUEST_VARS['message'] = "Erreur lors de la reprise de la partie"
                REQUEST_VARS['message_class'] = "alert-error"
        
        else:
            REQUEST_VARS['message'] = "Aucune partie active trouvée"
            REQUEST_VARS['message_class'] = "alert-error"

    elif POST and 'bouton_commencer' in POST:
        if id_partie_active and demarrer_partie(conn, id_partie_active):
            REQUEST_VARS['partie']['etat'] = 'En cours'
            REQUEST_VARS['num_tour'] = 1
            REQUEST_VARS['etape_tour'] = determiner_etape_apres_pioche(REQUEST_VARS['carte_active'], id_partie_active, id_joueur, conn)
            
            carte = piocher_carte(conn, id_partie_active)
            SESSION['CARTE_ACTIVE'] = carte
            REQUEST_VARS['carte_active'] = carte

            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)
            
            REQUEST_VARS['message'] = "La partie a démarré. À vous de tirer."
            REQUEST_VARS['message_class'] = "alert-success"
        else:
            REQUEST_VARS['message'] = "Échec de l'initialisation du tour."
            REQUEST_VARS['message_class'] = "alert-error"

    elif POST and 'bouton_placer_bonus' in POST:
        coord_x = int(POST.get('coordX')[0])
        coord_y = POST.get('coordY')[0].upper()

        if id_partie_active:
            carte_actuelle = SESSION.get('CARTE_ACTIVE')
            type_bat = 'Leurre' if carte_actuelle['code'] == 'C_LEURRE' else 'Orque'

            if placer_bonus(conn, id_partie_active, id_joueur, coord_x, coord_y, type_bat):
                REQUEST_VARS['message'] = f"{type_bat} déployé en {coord_y}{coord_x}. Vous pouvez maintenant tirer."
                REQUEST_VARS['message_class'] = "alert-success"
                SESSION['CARTE_ACTIVE'] = None
                REQUEST_VARS['carte_active'] = None 
                REQUEST_VARS['etape_tour'] = 'attente_tir_joueur'
            else:
                REQUEST_VARS['message'] = "Erreur lors du placement. Réessayez."
                REQUEST_VARS['message_class'] = "alert-error"
                REQUEST_VARS['etape_tour'] = 'attente_placement_bonus'

            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)
    
    elif POST and 'bouton_verifier' in POST:
        coord_x = int(POST.get('coordX')[0])
        coord_y = POST.get('coordY')[0].upper()

        if id_partie_active:
            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            placements_cible = get_placements_joueur_partie(conn, id_partie_active, id_adversaire)

            coord_visee = f"{coord_y}{coord_x}"
            case_occupee = False 

            if placements_cible:
                for bateau in placements_cible:
                    coords_bateau = calculer_occupation_bateau(bateau['xy'], bateau['sens'], bateau['taille_bat'])
                    if coord_visee in coords_bateau and bateau['etat'] != 'coulé':
                        case_occupee = True
                        break
            
            if case_occupee:
                REQUEST_VARS['message'] = f"Il y a bien un bateau en {coord_y}{coord_x} !"
                REQUEST_VARS['message_class'] = "alert-success"
            else:
                REQUEST_VARS['message'] = f"Aucun bateau detecté en {coord_y}{coord_x}."
                REQUEST_VARS['message_class'] = "alert-warning"

            SESSION['CARTE_ACTIVE'] = None
            REQUEST_VARS['carte_active'] = None
            REQUEST_VARS['etape_tour'] = 'attente_tir_joueur'
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)
    
    elif POST and 'bouton_reparer_mpm' in POST:
        ancien_xy = POST.get('ancienXY')[0] # Coordonnée du bateau touché
        nouveau_x = int(POST.get('coordX')[0])
        nouveau_y = POST.get('coordY')[0].upper()
        nouveau_xy = f"{nouveau_y}{nouveau_x}"

        if id_partie_active:
            if deplacer_et_reparer_bateau(conn, id_partie_active, id_joueur, ancien_xy, nouveau_xy):
                REQUEST_VARS['message'] = f"Bateau réparé et repositionné secrètement."
                REQUEST_VARS['message_class'] = "alert-success"
            else:
                REQUEST_VARS['message'] = f"Erreur: le bateau n'a pas pu être replacé"
                REQUEST_VARS['message_class'] = "alert-error"
                
            SESSION['CARTE_ACTIVE'] = None
            REQUEST_VARS['carte_active'] = None
            REQUEST_VARS['etape_tour'] = 'attente_tir_joueur'
            
            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)

    elif POST and ('bouton_accepter_passe' in POST or 'bouton_accepter_oups' in POST):
        if id_partie_active:
            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            
            if 'bouton_accepter_oups' in POST:
                cible = choisir_cible_ia_impossible(conn, id_partie_active, id_joueur, id_adversaire)
                if cible:
                    coord_y = cible[0]
                    coord_x = int(cible[1:])
                    
                    touches, coules, willy = evaluer_et_enregistrer_tir(conn, id_partie_active, id_adversaire, id_joueur, coord_x, coord_y, REQUEST_VARS.get('num_tour', 1), None)
                    REQUEST_VARS['message'] = f"Oups ! L'un de vos matelots a fait tomber un missile sur votre propre pont en {coord_y}{coord_x}. Manque de chance, il a survécu et recommencera surement."
                    REQUEST_VARS['message_class'] = "alert-error"
                else:
                    REQUEST_VARS['message'] = "Erreur: le missile tombé sur votre pont n'a pas explosé, étrange."
                    REQUEST_VARS['message_class'] = "alert-warning"
            else:
                REQUEST_VARS['message'] = "Vous avez passé votre tour."
                REQUEST_VARS['message_class'] = "alert-warning"

            SESSION['CARTE_ACTIVE'] = None
            REQUEST_VARS['carte_active'] = None

            if verifier_fin_partie(conn, id_partie_active, id_joueur):
                terminer_partie(conn, id_partie_active, id_adversaire, 'Perdue')
                REQUEST_VARS['partie']['etat'] = 'Perdue'
                REQUEST_VARS['message'] = "Le missile que votre matelot a fait tomber a détruit votre dernier bateau, c'était peut être une erreur de le recruter."
                REQUEST_VARS['etape_tour'] = 'fin_partie'
            else:
                REQUEST_VARS['etape_tour'] = 'attente_suivant_joueur'
                nouveau_tour = int(REQUEST_VARS.get('num_tour', 1)) + 1
                REQUEST_VARS['num_tour'] = nouveau_tour
                creer_nouveau_tour(conn, id_partie_active, nouveau_tour)
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)
    
    elif POST and 'bouton_tirer' in POST:
        coord_x = int(POST.get('coordX')[0])
        coord_y = POST.get('coordY')[0].upper()
        
        if id_partie_active:            
            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            carte_actuelle = SESSION.get('CARTE_ACTIVE')
            
            touches, coules, willy = evaluer_et_enregistrer_tir(
                conn, id_partie_active, id_joueur, id_adversaire, 
                coord_x, coord_y, REQUEST_VARS.get('num_tour', 1), carte_actuelle
            )
            
            SESSION['CARTE_ACTIVE'] = None
            REQUEST_VARS['carte_active'] = None 
            
            
            if coules > 0:
                REQUEST_VARS['message'] = f"Bateau ennemi détruit en {coord_y}{coord_x}."
                REQUEST_VARS['message_class'] = "alert-success"
            elif touches > 0:
                REQUEST_VARS['message'] = f"Impact confirmé en {coord_y}{coord_x}."
                REQUEST_VARS['message_class'] = "alert-success"
            else:
                REQUEST_VARS['message'] = f"Tir non concluant en {coord_y}{coord_x}."
                REQUEST_VARS['message_class'] = "alert-warning"
            
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)

            if willy:
                REQUEST_VARS['message'] = "Oh non, vous avez tué Willy ! Les écologistes ne sont pas contents et s'en prennent à vos bateaux. Faites où vous tirez la prochaine fois..."
                REQUEST_VARS['message_class'] = "alert-warning"

            if verifier_fin_partie(conn, id_partie_active, id_adversaire):
                terminer_partie(conn, id_partie_active, id_joueur, 'Gagnée')
                REQUEST_VARS['partie']['etat'] = 'Gagnée'
                if willy:
                    REQUEST_VARS['message'] = "Vous avez gagné ! Mais à quel prix ? Willy a été brutalement assassiné..."
                else:
                    REQUEST_VARS['message'] = "Vous avez gagné ! Vous avez détruit tous les bateaux de votre adversaire."
                REQUEST_VARS['etape_tour'] = 'fin_partie'
            else:
                if carte_actuelle and carte_actuelle['code'] == 'C_REJOUE':
                    REQUEST_VARS['etape_tour'] = 'attente_tir_joueur'
                    REQUEST_VARS['message'] += " Grâce à votre carte, vous pouvez tirer une seconde fois !"
                else:
                    REQUEST_VARS['etape_tour'] = 'attente_suivant_joueur'
                    nouveau_tour = int(REQUEST_VARS.get('num_tour', 1)) + 1
                    REQUEST_VARS['num_tour'] = nouveau_tour
                    creer_nouveau_tour(conn, id_partie_active, nouveau_tour)

            SESSION['CARTE_ACTIVE'] = None
            REQUEST_VARS['carte_active'] = None

    elif POST and 'bouton_suivant' in POST:
        if id_partie_active:
            id_adversaire = get_adversaire_partie(conn, id_partie_active, id_joueur)
            
            carte_bot = piocher_carte(conn, id_partie_active)
            niveau_bot = get_niveau_bot(conn, id_adversaire)

            if niveau_bot == 'Impossible':
                cible = choisir_cible_ia_impossible(conn, id_partie_active, id_joueur, id_adversaire)
            else:
                cible = choisir_cible_ia_intermediaire(REQUEST_VARS['grille_joueur'])
            
            if cible:
                coord_y = cible[0]
                coord_x = int(cible[1:])
                
                # L'IA tire
                touches, coules, willy = evaluer_et_enregistrer_tir(
                    conn, id_partie_active, id_adversaire, id_joueur, 
                    coord_x, coord_y, REQUEST_VARS.get('num_tour', 1), carte_bot
                )
                if willy:
                    REQUEST_VARS['message'] = "L'adversaire a tiré sur Willy ! Les écologistes se sont chargés de lui, il ne fera plus de mal aux animaux."
                    REQUEST_VARS['message_class'] = "alert-warning"
                elif coules > 0:
                    REQUEST_VARS['message'] = f"L'ennemi a coulé un de vos bateaux en tirant en {coord_y}{coord_x} !"
                    REQUEST_VARS['message_class'] = "alert-error"
                elif touches > 0:
                    REQUEST_VARS['message'] = f"L'ennemi vous a touché en {coord_y}{coord_x} !"
                    REQUEST_VARS['message_class'] = "alert-error"
                else:
                    REQUEST_VARS['message'] = f"Le tir ennemi en {coord_y}{coord_x} a manqué sa cible."
                    REQUEST_VARS['message_class'] = "alert-success"
            
                REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)



                if verifier_fin_partie(conn, id_partie_active, id_joueur):
                    if willy:
                        REQUEST_VARS['message'] = "Victoire inattendue ! L'adversaire a tiré sur Willy, les écologistes ont détruit sa flotte en représaille. Il avait qu'à mieux choisir sa cible."
                        REQUEST_VARS['partie']['etat'] = 'Gagnée'
                        terminer_partie(conn, id_partie_active, id_joueur, 'Gagnée')
                    else:
                        terminer_partie(conn, id_partie_active, id_adversaire, 'Perdue')
                        REQUEST_VARS['partie']['etat'] = 'Perdue'
                        REQUEST_VARS['message'] = "Vous avez perdu :c"
                    REQUEST_VARS['etape_tour'] = 'fin_partie'
                else:
                    nouveau_tour = int(REQUEST_VARS.get('num_tour', 1)) + 1
                    REQUEST_VARS['num_tour'] = nouveau_tour
                    creer_nouveau_tour(conn, id_partie_active, nouveau_tour)
                    carte_joueur = piocher_carte(conn, id_partie_active)
                    SESSION['CARTE_ACTIVE'] = carte_joueur
                    REQUEST_VARS['carte_active'] = carte_joueur
                    REQUEST_VARS['etape_tour'] = determiner_etape_apres_pioche(carte_joueur, id_partie_active, id_joueur, conn)

            # On met à jour l'affichage
            REQUEST_VARS['grille_joueur'], REQUEST_VARS['grille_adversaire'] = generer_etats_grilles(conn, id_partie_active, id_joueur, id_adversaire)

    elif POST and 'bouton_suspendre' in POST:
        if id_partie_active:
            if suspendre_partie(conn, id_partie_active):
                REQUEST_VARS['partie']['etat'] = 'Suspendue'
                REQUEST_VARS['message'] = "La partie a été suspendue. Vous pourrez la reprendre quand bon vous semblera." 
                REQUEST_VARS['message_class'] = 'alert-success'
                REQUEST_VARS['etape_tour'] = 'partie_suspendue'
            else:
                REQUEST_VARS['message'] = "Echec lors de la tentative de suspension de la partie"
                REQUEST_VARS['message_class'] = 'alert-error'

else:
    REQUEST_VARS['acces_refuse'] = True
    REQUEST_VARS['carte_active'] = SESSION.get('CARTE_ACTIVE')
    REQUEST_VARS['message'] = "Accès refusé. Veuillez vous identifier."
    REQUEST_VARS['message_class'] = "alert-error"