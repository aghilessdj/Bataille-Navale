-- création d'un schéma
CREATE SCHEMA BatNav;
SET search_path TO BatNav;

-- ------------------------------------------------------
-- JOUEURS ----------------------------------------------
-- ------------------------------------------------------

CREATE TABLE joueur (
    idJ SERIAL PRIMARY KEY,
    pseudo varchar(50),
    typeJ varchar(50),
    nom varchar(80),
    prénom varchar(80),
    email varchar(150),
    date_n date
    
);

INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('Yacou', 'Humain', 'ACOULAY', 'Yves', 'YH@titi.fr', '2001-02-04');
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('Zelda', 'Virtuel', NULL, NULL, NULL, NULL);
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('Mario', 'Virtuel', NULL, NULL, NULL, NULL);
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('You', 'Humain', 'AITORPILLET', 'Youssef', 'YA@toto.fr', '2002-12-23');
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('Kirby', 'Virtuel', NULL, NULL, NULL, NULL);
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('Pikachu', 'Virtuel', NULL, NULL, NULL, NULL);
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('JD', 'Humain', 'DEAU', 'John', 'JD@tata.fr', '1999-11-02');
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('evaB', 'Humain', 'BOMBARDER', 'Eva', 'EB@tutu.fr', '1999-11-02');
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('LaRo', 'Humain', 'ROQUETTE', 'Lance', 'LR@tyty.fr', '1998-10-07');
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('Thanos', 'Virtuel', NULL, NULL, NULL, NULL);
INSERT INTO joueur (pseudo, typeJ, nom, prénom, email, date_n) VALUES ('ET', 'Humain', 'TOUCOULET', 'Ella', 'ET@maison.fr', '2005-08-14');
SELECT * FROM joueur;

CREATE TABLE info_Joueur_Virtuel(
    idJ integer,
    idJ_createur integer,
    date_c date,
    niveau_exp_JV varchar(50)
);

INSERT INTO info_Joueur_Virtuel (idJ, idJ_createur, date_c, niveau_exp_JV ) VALUES (2,1,'2026-03-03','Expert');
INSERT INTO info_Joueur_Virtuel (idJ, idJ_createur, date_c, niveau_exp_JV ) VALUES (3,4,'2026-03-04','Faible');
INSERT INTO info_Joueur_Virtuel (idJ, idJ_createur, date_c, niveau_exp_JV ) VALUES (5,4,'2026-03-06','Faible');
INSERT INTO info_Joueur_Virtuel (idJ, idJ_createur, date_c, niveau_exp_JV ) VALUES (6,7,'2026-03-07','Intermédiaire');
INSERT INTO info_Joueur_Virtuel (idJ, idJ_createur, date_c, niveau_exp_JV ) VALUES (10,11,'2026-03-11','Expert');
SELECT * FROM info_Joueur_Virtuel;

-- ------------------------------------------------------
-- PARTIE ----------------------------------------------
-- ------------------------------------------------------

CREATE TABLE partie (
    idP integer PRIMARY KEY,
    état varchar(50),
    idJ_virtuel integer,
    idJ_humain integer,
    score_final integer,
    idPioche integer,
    idJ_gagnant integer,
    seq_tempo_1_debut timestamp,
    seq_tempo_1_fin timestamp,
    seq_tempo_2_debut timestamp,
    seq_tempo_2_fin timestamp,
    seq_tempo_3_debut timestamp,
    seq_tempo_3_fin timestamp
  );

INSERT INTO partie (
    idP, état, idJ_virtuel, idJ_humain, score_final, idPioche , idJ_gagnant,
    seq_tempo_1_debut, seq_tempo_1_fin, 
    seq_tempo_2_debut,seq_tempo_2_fin , 
    seq_tempo_3_debut, seq_tempo_3_fin
)VALUES (41, 'Terminé', 2, 1, 140, 103, 1,
         '2026-03-04 10:05:00', '2026-03-04 10:35:00',
         '2026-03-04 14:00:00', '2026-03-04 15:32:00',
         NULL, NULL );
INSERT INTO partie (
    idP, état, idJ_virtuel, idJ_humain, score_final, idPioche , idJ_gagnant,
    seq_tempo_1_debut, seq_tempo_1_fin, 
    seq_tempo_2_debut,seq_tempo_2_fin , 
    seq_tempo_3_debut, seq_tempo_3_fin
)VALUES (52, 'En cours', 3, 1, NULL, 105, NULL,
         '2026-03-13 09:15:00', NULL,
         NULL, NULL,
         NULL, NULL);
INSERT INTO partie (
    idP, état, idJ_virtuel, idJ_humain, score_final, idPioche , idJ_gagnant,
    seq_tempo_1_debut, seq_tempo_1_fin, 
    seq_tempo_2_debut,seq_tempo_2_fin , 
    seq_tempo_3_debut, seq_tempo_3_fin
)VALUES (63, 'Suspendue', 3, 4, NULL, 103, NULL,
         '2026-03-10 18:05:00', '2026-03-10 19:05:00',
         NULL, NULL,
         NULL, NULL );

SELECT * FROM partie;

-- ------------------------------------------------------
-- TOUR   ----------------------------------------------
-- ------------------------------------------------------

CREATE TABLE tour (
    idP integer,
    numT integer
  
);
ALTER TABLE tour ADD CONSTRAINT pk_tour PRIMARY KEY (idP, numT);
ALTER TABLE tour ADD CONSTRAINT fk_tour_partie FOREIGN KEY (idP) REFERENCES partie (idP);

INSERT INTO tour (idP, numT) VALUES (41,1),(41,2),(41,3);
INSERT INTO tour (idP, numT) VALUES (52,1),(52,2);
INSERT INTO tour (idP, numT) VALUES (63,1);

SELECT * FROM tour;

-- ------------------------------------------------------
-- DISTRIBUTIONS DE CARTES  -----------------------------
-- ------------------------------------------------------

CREATE TABLE distribution_cartes (
    idD integer PRIMARY KEY,
    nom varchar(50),
    c_missile integer,
    c_rejoue integer,
    c_vide integer,
    c_mpm integer,
    c_leurre integer,
    c_willy integer,
    c_mega integer,
    c_etoile integer,
    c_passe integer,
    c_oups integer
);
DELETE FROM distribution_cartes;
INSERT INTO distribution_cartes (idD, nom, c_missile, c_rejoue, c_vide, c_mpm, c_leurre, c_willy, c_mega, c_etoile, c_passe, c_oups)
 VALUES (1, 'Distrib 1', 50, 10, 5, 5, 3, 3, 3, 1, 10, 5);
INSERT INTO distribution_cartes (idD, nom, c_missile, c_rejoue, c_vide, c_mpm, c_leurre, c_willy, c_mega, c_etoile, c_passe, c_oups)
 VALUES (2, 'Distrib 2',20, 15, 13, 10, 5, 5, 5, 2, 15, 10);
INSERT INTO distribution_cartes (idD, nom, c_missile, c_rejoue, c_vide, c_mpm, c_leurre, c_willy, c_mega, c_etoile, c_passe, c_oups)
 VALUES (3, 'Distrib 3',10, 5, 15, 10, 10, 10, 10, 5, 5, 20);

SELECT * FROM distribution_cartes;

-- ------------------------------------------------------
-- PIOCHE     -------------------------------------------
-- ------------------------------------------------------

CREATE TABLE pioche (
    idPi integer,
    idDist integer
);
ALTER TABLE pioche ADD CONSTRAINT pk_pioche PRIMARY KEY (idPi, idDist);
ALTER TABLE pioche ADD CONSTRAINT fk_pioche_distrib FOREIGN KEY (idDist) REFERENCES distribution_cartes (idD);


INSERT INTO pioche (idPi, idDist) VALUES (103,1), (105,3);

SELECT * FROM pioche;

-- ------------------------------------------------------
-- TYPE_CARTE    ----------------------------------------
-- ------------------------------------------------------

CREATE TABLE type_carte(
    codeTC varchar(20) PRIMARY KEY,
    est_bonus boolean,
    nom varchar(80),
    description_tc text,
    image_tc varchar(80)
 );

INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_MISSILE', NULL, 'Missile', 'Cette carte permet de tirer un missile "classique" qui touchera la case indiquée', 'carte1.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_REJOUE', true, 'Rejoue une fois', 'Cette carte  permet à celui qui la tire de tirer dans le même tour une seconde fois', 'carte2.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_VIDE', true, 'Vide ou pas vide?', 'Cette carte permet à celui qui la tire de savoir avant de lancer son missile si une case est vide ou pas par une notification. Cela lui permet de confirmer le tir où de changer de coordonnées.', 'carte3.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_MPM', true, 'Même pas mal', 'Cette carte permet à celui qui la tire d''annuler un dégât subi sur un de ses navires et de le changer de place', 'carte4.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_LEURRE', true, 'Bâteau leurre', 'Cette carte permet à celui qui la tire de placer un bateau leurre dans la grille. Si durant la partie le leurre est touché, il disparaît en laissant croire à l''adversaire qu''il a touché un navire ', 'carte5.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_WILLY', true, 'Sauvez Willy', 'Cette carte permet à celui qui la tire de placer une orque dans la grille. Si durant la partie l''orque est touchée, les trois plus petits navires non encore coulés sont alors coulés en représailles des activistes écologistes
', 'carte6.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_MEGA', true, 'Méga-bombe', 'Cette carte ermet à celui qui la tire de remplacer son prochain missile par une méga-bombe qui fera des dégâts également sur les 8 cases adjacentes à la cible, soit 9 cases d''un coup', 'carte7.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_ETOILE', true, 'Étoile de la mort', 'Cette carte permet à celui qui la tire de remplacer son prochain missile par un tir depuis l''étoile de la mort qui fera des dégâts également sur les 24 cases les plus proches de la cible, soit 25 cases d''un coup', 'carte8.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_PASSE', false, 'Passe ton tour', 'Le joueur qui pioche cette carte perd son tour. Son adversaire joue donc deux fois de suite.', 'carte9.png');
INSERT INTO type_carte (codeTC, est_bonus, nom, description_tc, image_tc)
VALUES ('C_OUPS', false, 'Mauvaise manip', 'Cette carte fait que le missile que vous vous apprêtiez à tirer a été échappé par le matelot qui devait le charger dans le silo. C''est donc un de vos navires, choisi aléatoirement qui est touché et vous perdez votre tour', 'carte10.png');

SELECT * FROM type_carte;

-- ------------------------------------------------------
-- LIEN CARTES / TYPE_CARTE / PIOCHE    -----------------
-- ------------------------------------------------------

CREATE TABLE appartient(
    idCarte integer PRIMARY KEY,
    codeTC varchar(20),
    idPi integer,
    rang integer
 );

INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (1, 'C_MISSILE' , 105 , 1 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (2, 'C_MISSILE' , 105 , 2 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (3, 'C_MISSILE' , 105 , 3 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (4, 'C_MISSILE' , 105 , 4 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (5, 'C_MISSILE' , 105 , 5 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (6, 'C_MISSILE' , 105 , 6 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (7, 'C_MISSILE' , 105 , 7 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (8, 'C_MISSILE' , 105 , 8 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (9, 'C_MISSILE' , 105 , 9 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (10, 'C_MISSILE' , 105 , 10 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (11, 'C_MISSILE' , 105 , 11 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (12, 'C_MISSILE' , 105 , 12 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (13, 'C_MISSILE' , 105 , 13 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (14, 'C_MISSILE' , 105 , 14 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (15, 'C_MISSILE' , 105 , 15 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (16, 'C_MISSILE' , 105 , 16 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (17, 'C_MISSILE' , 105 , 17 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (18, 'C_MISSILE' , 105 , 18 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (19, 'C_MISSILE' , 105 , 19 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (20, 'C_MISSILE' , 105 , 20 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (21, 'C_MISSILE' , 105 , 21 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (22, 'C_MISSILE' , 105 , 22 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (23, 'C_MISSILE' , 105 , 23 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (24, 'C_MISSILE' , 105 , 24 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (25, 'C_MISSILE' , 105 , 25 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (26, 'C_MISSILE' , 105 , 26 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (27, 'C_MISSILE' , 105 , 27 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (28, 'C_MISSILE' , 105 , 28 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (29, 'C_MISSILE' , 105 , 29 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (30, 'C_MISSILE' , 105 , 30 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (31, 'C_MISSILE' , 105 , 31 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (32, 'C_MISSILE' , 105 , 32 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (33, 'C_MISSILE' , 105 , 33 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (34, 'C_MISSILE' , 105 , 34 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (35, 'C_MISSILE' , 105 , 35 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (36, 'C_MISSILE' , 105 , 36 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (37, 'C_MISSILE' , 105 , 37 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (38, 'C_MISSILE' , 105 , 38 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (39, 'C_MISSILE' , 105 , 39 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (40, 'C_MISSILE' , 105 , 40 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (41, 'C_MISSILE' , 105 , 41 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (42, 'C_MISSILE' , 105 , 42 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (43, 'C_MISSILE' , 105 , 43 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (44, 'C_MISSILE' , 105 , 44 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (45, 'C_MISSILE' , 105 , 45 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (46, 'C_MISSILE' , 105 , 46 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (47, 'C_MISSILE' , 105 , 47 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (48, 'C_MISSILE' , 105 , 48 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (49, 'C_MISSILE' , 105 , 49 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (50, 'C_MISSILE' , 105 , 50 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (51, 'C_REJOUE' , 105 , 51 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (52, 'C_REJOUE' , 105 , 52 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (53, 'C_REJOUE' , 105 , 53 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (54, 'C_REJOUE' , 105 , 54 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (55, 'C_REJOUE' , 105 , 55 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (56, 'C_REJOUE' , 105 , 56 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (57, 'C_REJOUE' , 105 , 57 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (58, 'C_REJOUE' , 105 , 58 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (59, 'C_REJOUE' , 105 , 59 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (60, 'C_REJOUE' , 105 , 60 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (61, 'C_VIDE' , 105 , 61 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (62, 'C_VIDE' , 105 , 62 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (63, 'C_VIDE' , 105 , 63 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (64, 'C_VIDE' , 105 , 64 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (65, 'C_VIDE' , 105 , 65 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (66, 'C_VIDE' , 105 , 66 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (67, 'C_VIDE' , 105 , 67 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (68, 'C_VIDE' , 105 , 68 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (69, 'C_VIDE' , 105 , 69 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (70, 'C_VIDE' , 105 , 70 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (71, 'C_MPM' , 105 , 71 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (72, 'C_MPM' , 105 , 72 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (73, 'C_MPM' , 105 , 73 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (74, 'C_MPM' , 105 , 74 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (75, 'C_MPM' , 105 , 75 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (76, 'C_LEURRE' , 105 , 76 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (77, 'C_LEURRE' , 105 , 77 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (78, 'C_LEURRE' , 105 , 78 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (79, 'C_WILLY' , 105 , 79 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (80, 'C_WILLY' , 105 , 80 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (81, 'C_WILLY' , 105 , 81 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (82, 'C_MEGA' , 105 , 82 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (83, 'C_MEGA' , 105 , 83 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (84, 'C_MEGA' , 105 , 84 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (85, 'C_ETOILE' , 105 , 85 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (86, 'C_PASSE' , 105 , 86 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (87, 'C_PASSE' , 105 , 87 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (88, 'C_PASSE' , 105 , 88 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (89, 'C_PASSE' , 105 , 89 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (90, 'C_PASSE' , 105 , 90 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (91, 'C_PASSE' , 105 , 91 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (92, 'C_PASSE' , 105 , 92 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (93, 'C_PASSE' , 105 , 93 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (94, 'C_PASSE' , 105 , 94 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (95, 'C_PASSE' , 105 , 95 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (96, 'C_OUPS' , 105 , 96 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (97, 'C_OUPS' , 105 , 97 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (98, 'C_OUPS' , 105 , 98 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (99, 'C_OUPS' , 105 , 99 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (100, 'C_OUPS' , 105 , 100 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (101, 'C_MISSILE' , 103 , 1 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (102, 'C_MISSILE' , 103 , 2 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (103, 'C_MISSILE' , 103 , 3 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (104, 'C_MISSILE' , 103 , 4 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (105, 'C_MISSILE' , 103 , 5 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (106, 'C_MISSILE' , 103 , 6 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (107, 'C_MISSILE' , 103 , 7 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (108, 'C_MISSILE' , 103 , 8 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (109, 'C_MISSILE' , 103 , 9 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (110, 'C_MISSILE' , 103 , 10 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (111, 'C_REJOUE' , 103 , 11 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (112, 'C_REJOUE' , 103 , 12 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (113, 'C_REJOUE' , 103 , 13 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (114, 'C_REJOUE' , 103 , 14 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (115, 'C_REJOUE' , 103 , 15 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (116, 'C_VIDE' , 103 , 16 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (117, 'C_VIDE' , 103 , 17 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (118, 'C_VIDE' , 103 , 18 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (119, 'C_VIDE' , 103 , 19 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (120, 'C_VIDE' , 103 , 20 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (121, 'C_VIDE' , 103 , 21 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (122, 'C_VIDE' , 103 , 22 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (123, 'C_VIDE' , 103 , 23 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (124, 'C_VIDE' , 103 , 24 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (125, 'C_VIDE' , 103 , 25 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (126, 'C_VIDE' , 103 , 26 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (127, 'C_VIDE' , 103 , 27 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (128, 'C_VIDE' , 103 , 28 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (129, 'C_VIDE' , 103 , 29 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (130, 'C_VIDE' , 103 , 30 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (131, 'C_MPM' , 103 , 31 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (132, 'C_MPM' , 103 , 32 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (133, 'C_MPM' , 103 , 33 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (134, 'C_MPM' , 103 , 34 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (135, 'C_MPM' , 103 , 35 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (136, 'C_MPM' , 103 , 36 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (137, 'C_MPM' , 103 , 37 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (138, 'C_MPM' , 103 , 38 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (139, 'C_MPM' , 103 , 39 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (140, 'C_MPM' , 103 , 40 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (141, 'C_LEURRE' , 103 , 41 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (142, 'C_LEURRE' , 103 , 42 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (143, 'C_LEURRE' , 103 , 43 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (144, 'C_LEURRE' , 103 , 44 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (145, 'C_LEURRE' , 103 , 45 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (146, 'C_LEURRE' , 103 , 46 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (147, 'C_LEURRE' , 103 , 47 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (148, 'C_LEURRE' , 103 , 48 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (149, 'C_LEURRE' , 103 , 49 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (150, 'C_LEURRE' , 103 , 50 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (151, 'C_WILLY' , 103 , 51 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (152, 'C_WILLY' , 103 , 52 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (153, 'C_WILLY' , 103 , 53 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (154, 'C_WILLY' , 103 , 54 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (155, 'C_WILLY' , 103 , 55 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (156, 'C_WILLY' , 103 , 56 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (157, 'C_WILLY' , 103 , 57 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (158, 'C_WILLY' , 103 , 58 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (159, 'C_WILLY' , 103 , 59 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (160, 'C_WILLY' , 103 , 60 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (161, 'C_MEGA' , 103 , 61 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (162, 'C_MEGA' , 103 , 62 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (163, 'C_MEGA' , 103 , 63 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (164, 'C_MEGA' , 103 , 64 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (165, 'C_MEGA' , 103 , 65 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (166, 'C_MEGA' , 103 , 66 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (167, 'C_MEGA' , 103 , 67 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (168, 'C_MEGA' , 103 , 68 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (169, 'C_MEGA' , 103 , 69 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (170, 'C_MEGA' , 103 , 70 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (171, 'C_ETOILE' , 103 , 71 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (172, 'C_ETOILE' , 103 , 72 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (173, 'C_ETOILE' , 103 , 73 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (174, 'C_ETOILE' , 103 , 74 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (175, 'C_ETOILE' , 103 , 75 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (176, 'C_PASSE' , 103 , 76 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (177, 'C_PASSE' , 103 , 77 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (178, 'C_PASSE' , 103 , 78 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (179, 'C_PASSE' , 103 , 79 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (180, 'C_PASSE' , 103 , 80 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (181, 'C_OUPS' , 103 , 81 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (182, 'C_OUPS' , 103 , 82 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (183, 'C_OUPS' , 103 , 83 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (184, 'C_OUPS' , 103 , 84 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (185, 'C_OUPS' , 103 , 85 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (186, 'C_OUPS' , 103 , 86 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (187, 'C_OUPS' , 103 , 87 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (188, 'C_OUPS' , 103 , 88 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (189, 'C_OUPS' , 103 , 89 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (190, 'C_OUPS' , 103 , 90 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (191, 'C_OUPS' , 103 , 91 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (192, 'C_OUPS' , 103 , 92 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (193, 'C_OUPS' , 103 , 93 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (194, 'C_OUPS' , 103 , 94 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (195, 'C_OUPS' , 103 , 95 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (196, 'C_OUPS' , 103 , 96 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (197, 'C_OUPS' , 103 , 97 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (198, 'C_OUPS' , 103 , 98 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (199, 'C_OUPS' , 103 , 99 );
INSERT INTO appartient (idCarte, codeTC, idPi, rang) VALUES (200, 'C_OUPS' , 103 , 100 );

SELECT * FROM appartient;

-- ------------------------------------------------------
-- PLACEMENT DES NAVIRES    -----------------------------
-- ------------------------------------------------------

CREATE TABLE placements (
    idP integer,
    idJ integer,
    xy varchar(10),
    sens char(1),
    type_bat varchar(50),
    nom_bat varchar(80),
    taille_bat integer
);

INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,1,'2;B', 'V', 'torpilleur', NULL, 2);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,1,'4;C', 'H', 'porte-avion', 'Le Charles de Gaulle', 5);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,1,'8;D', 'H', 'contre-torpilleur', 'Le Triomphant', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,1,'9;F', 'H', 'contre-torpilleur', 'Le Terrible', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,1,'1;G', 'V', 'croiseur', 'Colbert', 4);

INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,2,'3;C', 'V', 'torpilleur', NULL, 2);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,2,'5;D', 'H', 'porte-avion', 'Le Charles de Gaulle', 5);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,2,'7;E', 'H', 'contre-torpilleur', 'Le Triomphant', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,2,'8;F', 'H', 'contre-torpilleur', 'Le Terrible', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (41,2,'2;I', 'V', 'croiseur', 'Colbert', 4);

INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,1,'2;B', 'V', 'torpilleur', NULL, 2);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,1,'4;C', 'H', 'porte-avion', 'Le Charles de Gaulle', 5);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,1,'8;D', 'H', 'contre-torpilleur', 'Le Triomphant', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,1,'9;F', 'H', 'contre-torpilleur', 'Le Terrible', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,1,'1;G', 'V', 'croiseur', 'Colbert', 4);

INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,3,'3;C', 'V', 'torpilleur', NULL, 2);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,3,'5;D', 'H', 'porte-avion', 'Le Charles de Gaulle', 5);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,3,'7;E', 'H', 'contre-torpilleur', 'Le Triomphant', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,3,'8;F', 'H', 'contre-torpilleur', 'Le Terrible', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (52,3,'2;I', 'V', 'croiseur', 'Colbert', 4);

INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,4,'2;B', 'V', 'torpilleur', NULL, 2);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,4,'4;C', 'H', 'porte-avion', 'Le Charles de Gaulle', 5);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,4,'8;D', 'H', 'contre-torpilleur', 'Le Triomphant', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,4,'9;F', 'H', 'contre-torpilleur', 'Le Terrible', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,4,'1;G', 'V', 'croiseur', 'Colbert', 4);

INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,3,'3;C', 'V', 'torpilleur', NULL, 2);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,3,'5;D', 'H', 'porte-avion', 'Le Charles de Gaulle', 5);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,3,'7;E', 'H', 'contre-torpilleur', 'Le Triomphant', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,3,'8;F', 'H', 'contre-torpilleur', 'Le Terrible', 3);
INSERT INTO placements (idP, idJ, xy, sens, type_bat, nom_bat, taille_bat ) VALUES (63,3,'2;I', 'V', 'croiseur', 'Colbert', 4);

SELECT * FROM placements;

-- ------------------------------------------------------
-- TIR                      -----------------------------
-- ------------------------------------------------------

CREATE TABLE tir (
    idP integer,
    numT integer,
    numTi integer,
    coordx integer,
    coordy char(1),
    idJ integer,
    idCarte integer
);

INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (41,1,1,3 , 'C' , 1,12);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (41,1,2,6 , 'A' , 2,24);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (41,2,1,3 , 'C' , 1,10);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (41,2,2,NULL , NULL , 2,66);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (41,3,1,3 , 'D' , 1,6);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (41,3,2,7 , 'E' , 2,16);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (52,1,1,1 , 'A' , 1,6);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (52,1,2,5 , 'D' , 3,14);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (52,1,3,6 , 'D' , 3,25);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (52,2,1,8 , 'B' , 1,11);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (52,2,2,8 , 'B' , 3,60);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (63,1,1,4 , 'F' , 4,18);
INSERT INTO tir (idP, numT, numTi, coordx, coordy, idJ, idCarte) VALUES (63,1,2,6 , 'C' , 3,50);

SELECT * FROM tir;

-- Generated by Mocodo 4.3.3
CREATE SCHEMA NavBat;
SET search_path TO NavBat;

-- -----------------------------
-- ---------- JOUEURS ----------
-- -----------------------------
CREATE TABLE Joueur (
  idJ              SERIAL PRIMARY KEY,
  pseudo           VARCHAR(42) NOT NULL UNIQUE,
  estVirtuel       boolean
);

INSERT INTO Joueur SELECT j.idJ, j.pseudo, false FROM BatNav.joueur j where j.typej = 'Humain';
INSERT INTO Joueur SELECT j.idJ, j.pseudo, true FROM BatNav.joueur j where j.typej = 'Virtuel';

SELECT setval('joueur_idj_seq', (SELECT MAX(idJ) FROM Joueur), true);

-- Type niveau
CREATE TYPE niveau AS ENUM ('Faible', 'Intermédiaire', 'Expert', 'Impossible');

-- -----------------------------
-- ---------- VIRTUEL ----------
-- -----------------------------
CREATE TABLE Virtuel (
  idJ              integer PRIMARY KEY,
  date_creation    DATE,
  idJ_createur     integer,
  niveau_expertise niveau
);

ALTER TABLE Virtuel ADD CONSTRAINT fk_idJ_virtuel FOREIGN KEY (idJ) REFERENCES Joueur (idJ);

INSERT INTO Virtuel SELECT i.idJ, i.date_c, i.idJ_createur, i.niveau_exp_JV::niveau FROM batnav.info_Joueur_Virtuel i;

-- ----------------------------
-- ---------- HUMAIN ----------
-- ----------------------------
CREATE TABLE Humain (
  idJ              integer PRIMARY KEY,
  nom              VARCHAR(42),
  prenom           VARCHAR(42),
  date_creation    DATE DEFAULT CURRENT_DATE,
  date_naissance   DATE
);

ALTER TABLE Humain ADD CONSTRAINT fk_idJ_humain FOREIGN KEY (idJ) REFERENCES Joueur (idJ);

INSERT INTO Humain SELECT j.idJ, j.nom, j.prénom, CURRENT_DATE, j.date_n FROM BatNav.joueur j where j.typej = 'Humain';

-- ----------------------------
-- ------- Distribution -------
-- ----------------------------
CREATE TABLE Distribution (
  idD         integer PRIMARY KEY,
  nom         VARCHAR(50) NOT NULL,
  c_missile   integer,
  c_rejoue    integer,
  c_vide      integer,
  c_mpm       integer,
  c_leurre    integer,
  c_willy     integer,
  c_mega      integer,
  c_etoile    integer,
  c_passe     integer,
  c_oups      integer
);

INSERT INTO Distribution SELECT d.* FROM batnav.distribution_cartes d;

-- ----------------------------
-- ---------- Pioche ----------
-- ----------------------------
CREATE TABLE Pioche (
  idPi integer PRIMARY KEY,
  idD  integer
);

INSERT INTO Pioche SELECT p.idPi, p.idDist FROM batnav.pioche p;

CREATE TYPE etat as ENUM ('Créée', 'En cours', 'Suspendue', 'Gagnée', 'Perdue', 'Terminé');

-- ----------------------------
-- ---------- Partie ----------
-- ----------------------------
CREATE TABLE Partie (
  idP          integer PRIMARY KEY,
  etat         etat,
  idJ_Virtuel  integer,
  idJ_Humain   integer,
  idJ_gagnant  integer,
  score_final  integer,
  idPi         integer
);


ALTER TABLE Partie ADD CONSTRAINT fk_idJ_Virtuel_Partie FOREIGN KEY (idJ_Virtuel) REFERENCES Virtuel (idJ);
ALTER TABLE Partie ADD CONSTRAINT fk_idJ_Humain_Partie FOREIGN KEY (idJ_Humain) REFERENCES Humain (idJ);
ALTER TABLE Partie ADD CONSTRAINT fk_idJ_gagnant FOREIGN KEY (idJ_gagnant) REFERENCES Joueur (idJ);
ALTER TABLE Partie ADD CONSTRAINT fk_idJ_Pioche_Partie FOREIGN KEY (idPi) REFERENCES Pioche (idPi);

INSERT INTO Partie SELECT p.idP, p.état::etat, p.idJ_virtuel, p.idJ_humain, p.idJ_gagnant, p.score_final,  p.idPioche FROM BatNav.partie p;

-- -----------------------------
-- --------- TypeCarte ---------
-- -----------------------------
CREATE TABLE TypeCarte (
  code        VARCHAR(42) PRIMARY KEY,
  estBonus    boolean,
  nom         VARCHAR(80),
  description text,
  image       VARCHAR(80)
);

INSERT INTO TypeCarte SELECT tc.codeTC, tc.est_bonus, tc.nom, tc.description_tc, tc.image_tc FROM batnav.type_carte tc;


-- -----------------------------
-- ----------- Carte -----------
-- -----------------------------
CREATE TABLE Carte (
  idC  integer PRIMARY KEY,
  code VARCHAR(42)
);

ALTER TABLE Carte ADD CONSTRAINT fk_Carte_TypeCarte FOREIGN KEY (code) REFERENCES TypeCarte (code);

INSERT INTO Carte SELECT a.idCarte, a.codeTC FROM batnav.appartient a;

CREATE TYPE etat_carte AS ENUM ('Dans la pioche', 'utilisée');

-- ----------------------------
-- -------- Appartient --------
-- ----------------------------
CREATE TABLE Appartient (
  idC       integer PRIMARY KEY, 
  idPi      integer,
  rang      integer,
  etat      etat_carte
);

ALTER TABLE Appartient ADD CONSTRAINT fk_idC_Appartient FOREIGN KEY (idC) REFERENCES Carte (idC);
ALTER TABLE Appartient ADD CONSTRAINT fk_idPi_Appartient FOREIGN KEY (idPi) REFERENCES Pioche (idPi);

INSERT INTO Appartient SELECT a.idCarte, a.idPi, a.rang, NULL FROM batnav.appartient a;

-- ----------------------------
-- ---- SequenceTemporelle ----
-- ----------------------------
CREATE TABLE SequenceTemporelle (
  idP         integer,
  date_debut  DATE,
  heure_debut time,
  date_fin    DATE,
  heure_fin   time
);

ALTER TABLE SequenceTemporelle ADD CONSTRAINT pk_SeqTemp PRIMARY KEY (idP, date_debut, heure_debut);
ALTER TABLE SequenceTemporelle ADD CONSTRAINT fk_SeqTemp_Partie FOREIGN KEY (idP) REFERENCES Partie (idP);

INSERT INTO SequenceTemporelle
  SELECT p.idP, p.seq_tempo_1_debut::date, p.seq_tempo_1_debut::time, p.seq_tempo_1_fin::date, p.seq_tempo_1_fin::time 
  FROM batnav.partie p
  WHERE seq_tempo_1_debut IS NOT NULL
  UNION ALL
  SELECT p.idP, p.seq_tempo_2_debut::date, p.seq_tempo_2_debut::time, p.seq_tempo_2_fin::date, p.seq_tempo_2_fin::time 
  FROM batnav.partie p
  WHERE seq_tempo_2_debut IS NOT NULL
  UNION ALL
  SELECT p.idP, p.seq_tempo_3_debut::date, p.seq_tempo_3_debut::time, p.seq_tempo_3_fin::date, p.seq_tempo_3_fin::time 
  FROM batnav.partie p
  WHERE seq_tempo_3_debut IS NOT NULL;

-- ----------------------------
-- ----------- Tour -----------
-- ----------------------------
CREATE TABLE Tour (
  idP                 integer,
  numT                integer,
  nb_coulés_hum       integer, 
  nb_touchés_hum      integer, 
  nb_cell_libres_hum  integer,
  nb_coulés_virt      integer, 
  nb_touchés_virt     integer, 
  nb_cell_libres_virt integer
);

ALTER TABLE Tour ADD CONSTRAINT pk_Tour PRIMARY KEY (idP, numT);
ALTER TABLE Tour ADD CONSTRAINT fk_Tour_Partie FOREIGN KEY (idP) REFERENCES Partie (idP);

INSERT INTO Tour (idP, numT) SELECT t.idP, t.numT FROM batnav.tour t;

-- -----------------------------
-- ------------ Tir ------------
-- -----------------------------
CREATE TABLE Tir (
  idC     integer,
  idJ     integer,
  idP     integer,
  numT    integer,
  numTi   integer,
  coordX  integer,
  coordY  char(1)
);

ALTER TABLE Tir ADD CONSTRAINT pk_Tir PRIMARY KEY (idP, numT, numTi);
ALTER TABLE Tir ADD CONSTRAINT fk_Tir_Carte FOREIGN KEY (idC) REFERENCES Carte (idC);
ALTER TABLE Tir ADD CONSTRAINT fk_Tir_Joueur FOREIGN KEY (idJ) REFERENCES Joueur (idJ);
ALTER TABLE Tir ADD CONSTRAINT fk_Tir_Partie FOREIGN KEY (idP) REFERENCES Partie (idP);
ALTER TABLE Tir ADD CONSTRAINT fk_Tir_Tour FOREIGN KEY (idP, numT) REFERENCES Tour (idP, numT);

INSERT INTO Tir SELECT t.idCarte, t.idJ, t.idP, t.numT, t.numTi, t.coordx, t.coordy FROM batnav.tir t;

-- ----------------------------
-- -------- TypeBateau --------
-- ----------------------------
CREATE TABLE TypeBateau (
  type_bat    varchar(50) PRIMARY KEY,
  taille_bat  integer NOT NULL
);

INSERT INTO TypeBateau SELECT DISTINCT p.type_bat, p.taille_bat FROM batnav.placements p; 
INSERT INTO TypeBateau (type_bat, taille_bat) VALUES ('Leurre', 3);
INSERT INTO TypeBateau (type_bat, taille_bat) VALUES ('Orque', 1);

CREATE TYPE etat_navire AS ENUM ('opérationnel', 'touché', 'coulé');
CREATE TYPE sens AS ENUM ('V', 'H');

-- ----------------------------
-- --------- Pavillon ---------
-- ----------------------------
CREATE TABLE Pavillon (
  code_pays   VARCHAR(3) PRIMARY KEY,
  nom_pays    VARCHAR(50)
);

INSERT INTO NavBat.Pavillon (code_pays, nom_pays) VALUES ('FRA', 'France');

-- ----------------------------
-- -------- Placements --------
-- ----------------------------
CREATE TABLE Placements (
  idP         integer, 
  idJ         integer,
  xy          VARCHAR(10),
  sens        sens,
  type_bat    VARCHAR(50),
  nom_bat     VARCHAR(80),
  etat        etat_navire DEFAULT 'opérationnel',
  pavillon    VARCHAR(3)
);

ALTER TABLE Placements ADD CONSTRAINT pk_Placements PRIMARY KEY (idP, idJ, xy);
ALTER TABLE Placements ADD CONSTRAINT fk_Placements_TypeBateau FOREIGN KEY (type_bat) REFERENCES TypeBateau (type_bat);
ALTER TABLE Placements ADD CONSTRAINT fk_Placements_Pavillon FOREIGN KEY (pavillon) REFERENCES Pavillon (code_pays);
INSERT INTO Placements (idP, idJ, xy, sens, type_bat, nom_bat) SELECT p.idP, p.idJ, p.xy, p.sens::sens, p.type_bat, p.nom_bat FROM batnav.placements p;

-- ----------------------------
-- ---------- Grille ----------
-- ----------------------------
CREATE TABLE Grille (
  idG         integer PRIMARY KEY,
  idP         integer,
  idJ         integer, 
  largeur     integer, 
  hauteur    integer,
  img_eau     VARCHAR(80),
  img_touché  VARCHAR(80),
  img_vide    VARCHAR(80)
);

ALTER TABLE Grille ADD CONSTRAINT fk_Grille_Partie FOREIGN KEY (idp) REFERENCES Partie (idP);
ALTER TABLE Grille ADD CONSTRAINT fk_Grille_Joueur FOREIGN KEY (idJ) REFERENCES Joueur (idJ);

DROP SCHEMA batnav CASCADE;