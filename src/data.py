# -*- coding: utf-8 -*-
"""Page unique « Éclairage & signalisation » — les donnees.

BRIEF DU CLIENT (messages du 24 aout) :
  « Eclairage donc lampe inclus »
  « Tout les produits derives de lumiere »
  « Et eclairage et panneaux de signalisation »

Une seule page, un seul catalogue, deux grandes familles qui se filtrent.

CE QUE CETTE PAGE EST
---------------------
Un SQUELETTE DE CATALOGUE. Chaque carte est une CATEGORIE de produit, pas une
reference commerciale. Une categorie porte trois choses : ce qu'elle regroupe,
les usages ou elle intervient, et la GRILLE DE CARACTERISTIQUES qui sert a
comparer deux produits de cette categorie.

C'est cette grille qui a de la valeur. Un acheteur ne choisit pas une lanterne
routiere « parce qu'elle est belle » : il la choisit sur le flux, l'IP, la
classe photometrique et la temperature de couleur. Un panneau se choisit sur
la classe de retroreflexion, la gamme et le support. Tant que ces champs ne
sont pas poses, un catalogue n'est qu'une liste de photos.

CE QUI N'Y EST PAS, VOLONTAIREMENT
----------------------------------
  - AUCUNE VALEUR CHIFFREE attribuee a un produit. Pas « 12 000 lm », pas
    « IP66 », pas « classe M3 ». Je n'ai mesure aucun produit et le client n'a
    pas encore fourni de donnees fournisseur. La page annonce QUELS champs
    remplir, jamais AVEC QUOI.
  - AUCUNE NORME attribuee a un produit. Les intitules de normes qui
    apparaissent (classe photometrique, classe de retroreflexion, gamme de
    panneau) sont des NOMS DE CHAMPS, pas des valeurs certifiees.
  - AUCUN PRIX, aucune remise, aucun delai de livraison.
  - AUCUNE MARQUE de fabricant. Citer un fabricant sur une page commerciale
    sans accord est un probleme, et un catalogue qui liste des marques qu'il ne
    distribue pas trompe l'acheteur.
  - AUCUN STOCK, aucune disponibilite.

Les compteurs affiches sur la page sont DERIVES de ces listes. Aucun nombre
n'est ecrit a la main dans le HTML.
"""

# Le client a dit explicitement, le 24 aout, que le nom n'est pas fige. On ne
# code donc aucun nom en dur : celui-ci est un descriptif, remplacable en une
# ligne, et la page le signale elle-meme en haut.
MARQUE = 'ÉCLAIRAGE & SIGNALISATION'
TITRE = 'catalogue technique — éclairage et signalisation routière'

# Palette : sujet technique et routier. Encre froide, accent ambre (la couleur
# du sujet). Tous les contrastes sont MESURES par tests.py, jamais estimes.
FOND     = '#f4f6f8'
CARTE    = '#ffffff'
LIGNE    = '#dde2e9'
ENCRE    = '#111823'
TEXTE    = '#333d4d'
MUET     = '#596375'
ACCENT   = '#8a4f00'
ACCENT_D = '#6b3d00'

# ---------------------------------------------------------------------------
# LES DEUX DOMAINES. Ce sont les « deux familles » du brief.
# ---------------------------------------------------------------------------
DOMAINES = [
    ('eclairage',     'Éclairage'),
    ('signalisation', 'Signalisation routière'),
]

# ---------------------------------------------------------------------------
# LES FAMILLES, rattachees a un domaine. L'ordre est l'ordre d'affichage du
# menu deroulant ; les codes servent au filtrage et ne sont jamais affiches.
# ---------------------------------------------------------------------------
FAMILLES = [
    ('sources',      'Sources lumineuses (lampes)',            'eclairage'),
    ('interieur',    'Luminaires intérieurs',                  'eclairage'),
    ('exterieur',    'Éclairage extérieur et public',          'eclairage'),
    ('industriel',   'Éclairage industriel',                   'eclairage'),
    ('projecteurs',  'Projecteurs et éclairage scénique',      'eclairage'),
    ('secours',      'Éclairage de sécurité et de secours',    'eclairage'),
    ('decoratif',    'Éclairage décoratif',                    'eclairage'),
    ('composants',   'Composants et pilotage',                 'eclairage'),
    ('verticale',    'Signalisation verticale',                'signalisation'),
    ('horizontale',  'Signalisation horizontale',              'signalisation'),
    ('temporaire',   'Signalisation temporaire de chantier',   'signalisation'),
    ('equipements',  'Équipements de sécurité routière',       'signalisation'),
]

# ---------------------------------------------------------------------------
# LES USAGES. C'est le deuxieme axe : la meme categorie de produit se vend a un
# gestionnaire de voirie et a un architecte d'interieur, mais pas pour les
# memes raisons. Une categorie porte donc PLUSIEURS usages.
# ---------------------------------------------------------------------------
USAGES = [
    ('voirie',       'Voirie et espace public'),
    ('tunnel',       'Tunnel et ouvrage d’art'),
    ('industriel',   'Industrie et logistique'),
    ('tertiaire',    'Tertiaire et bureaux'),
    ('commerce',     'Commerce et hôtellerie'),
    ('residentiel',  'Résidentiel'),
    ('evenementiel', 'Événementiel et scénique'),
    ('chantier',     'Chantier et travaux'),
]

# ---------------------------------------------------------------------------
# LA GRILLE DE CARACTERISTIQUES. Ce sont des NOMS DE CHAMPS a renseigner, pas
# des valeurs. Chaque categorie declare ceux qui la definissent.
# ---------------------------------------------------------------------------
CARACS = [
    ('flux',        'Flux lumineux (lm)'),
    ('puissance',   'Puissance (W)'),
    ('efficacite',  'Efficacité lumineuse (lm/W)'),
    ('temperature', 'Température de couleur (K)'),
    ('irc',         'Indice de rendu des couleurs'),
    ('faisceau',    'Angle de faisceau'),
    ('ip',          'Indice de protection IP'),
    ('ik',          'Résistance aux chocs IK'),
    ('tension',     'Tension d’alimentation'),
    ('duree',       'Durée de vie annoncée (h)'),
    ('photo',       'Classe photométrique voirie'),
    ('culot',       'Culot ou douille'),
    ('pilotage',    'Gradation et protocole de pilotage'),
    ('autonomie',   'Autonomie en secours (h)'),
    ('retro',       'Classe de rétroréflexion'),
    ('gamme',       'Gamme de panneau'),
    ('format',      'Format et dimensions'),
    ('support',     'Support et fixation'),
    ('materiau',    'Matériau'),
    ('coloris',     'Coloris'),
    ('vent',        'Résistance au vent'),
    ('pose',        'Mode de pose'),
]

# ---------------------------------------------------------------------------
# LES CATEGORIES.
#   (famille, nom, [usages], description, [caracteristiques])
# La description dit ce que la categorie REGROUPE et sur quoi l'acheteur
# arbitre. Elle n'annonce aucune valeur.
# ---------------------------------------------------------------------------
CATEGORIES = [

    # --- Sources lumineuses ------------------------------------------------
    ('sources', 'Lampes LED à culot E27 et E14',
     ['residentiel', 'tertiaire', 'commerce'],
     'Les lampes de remplacement les plus courantes, en standard, flamme, '
     'sphérique ou globe. Le choix se joue sur le culot, la température de '
     'couleur et la compatibilité avec les variateurs déjà en place.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'irc', 'culot', 'duree', 'pilotage']),

    ('sources', 'Lampes LED à culot GU10 et GU5.3',
     ['residentiel', 'commerce', 'tertiaire'],
     'Sources directionnelles pour spots encastrés et rails. L’angle de '
     'faisceau change tout : le même luminaire éclaire une allée de magasin ou '
     'un tableau selon la lampe qu’on y met.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'culot', 'tension', 'pilotage']),

    ('sources', 'Tubes LED T8 et T5',
     ['tertiaire', 'industriel', 'commerce'],
     'Remplacement des tubes fluorescents en rénovation. Le point de vigilance '
     'n’est pas la lampe mais le luminaire existant : ballast conservé ou '
     'déposé, câblage simple ou double extrémité.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'irc', 'format', 'culot', 'duree']),

    ('sources', 'Lampes LED à culot E40 pour éclairage public',
     ['voirie', 'industriel'],
     'Sources de forte puissance destinées aux lanternes et projecteurs '
     'existants. Elles permettent de passer en LED sans déposer le luminaire, '
     'à condition que la répartition du flux reste compatible avec la voie.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'ip', 'culot', 'tension', 'duree']),

    ('sources', 'Lampes à décharge haute pression',
     ['voirie', 'industriel', 'evenementiel'],
     'Sodium haute pression et iodures métalliques, encore présents sur de '
     'nombreux parcs. Référencés pour la maintenance des installations qui ne '
     'sont pas encore converties.',
     ['flux', 'puissance', 'temperature', 'irc', 'culot', 'tension', 'duree']),

    ('sources', 'Lampes halogènes et à filament',
     ['residentiel', 'commerce', 'evenementiel'],
     'Sources à filament et halogènes, y compris les versions décoratives à '
     'filament apparent. Retenues pour la scénographie, la vitrine et les '
     'installations où le rendu chaud prime sur la consommation.',
     ['flux', 'puissance', 'temperature', 'irc', 'culot', 'tension', 'duree']),

    ('sources', 'Modules et platines LED',
     ['tertiaire', 'commerce', 'industriel'],
     'Cartes et platines destinées à être intégrées dans un luminaire ou à '
     'remplacer une platine défaillante. Se commandent par couple module + '
     'driver, jamais séparément.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'irc', 'tension', 'format', 'duree']),

    # --- Luminaires intérieurs ---------------------------------------------
    ('interieur', 'Dalles et panneaux LED encastrés',
     ['tertiaire', 'commerce'],
     'Le standard du plafond de bureau, en encastré dans faux plafond ou en '
     'saillie avec kit. L’arbitrage porte sur l’uniformité, l’éblouissement '
     'aux postes écran et la possibilité de graduer.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'irc', 'format', 'pilotage', 'pose']),

    ('interieur', 'Réglettes et bandeaux LED',
     ['tertiaire', 'residentiel', 'commerce'],
     'Linéaires simples pour couloirs, réserves, cuisines et plans de travail. '
     'Se posent en applique, en suspension ou en éclairage indirect selon les '
     'accessoires.',
     ['flux', 'puissance', 'temperature', 'irc', 'format', 'tension', 'pose', 'pilotage']),

    ('interieur', 'Downlights et spots encastrés',
     ['commerce', 'tertiaire', 'residentiel'],
     'Encastrés ponctuels, fixes ou orientables. Le diamètre de perçage et la '
     'profondeur disponible dans le plénum décident du modèle bien avant les '
     'considérations photométriques.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'format', 'ip', 'pose']),

    ('interieur', 'Luminaires sur rail triphasé',
     ['commerce', 'tertiaire', 'evenementiel'],
     'Projecteurs sur rail pour surfaces de vente et espaces d’exposition. '
     'L’intérêt du rail est la reconfiguration : les luminaires suivent le '
     'réaménagement du magasin sans travaux.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'tension', 'pilotage', 'coloris']),

    ('interieur', 'Suspensions et luminaires décoratifs de plafond',
     ['commerce', 'tertiaire', 'residentiel'],
     'Suspensions sur câble, pour salles de réunion, halls et restauration. '
     'Le rendu de couleur compte autant que le flux dès qu’il y a des visages '
     'ou de la nourriture sous le luminaire.',
     ['flux', 'puissance', 'temperature', 'irc', 'format', 'materiau', 'coloris', 'pose']),

    ('interieur', 'Plafonniers et hublots',
     ['residentiel', 'tertiaire', 'industriel'],
     'Luminaires fermés pour circulations, caves, parkings couverts et locaux '
     'techniques. Souvent associés à une détection de présence intégrée.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'format', 'pose', 'pilotage']),

    ('interieur', 'Appliques murales intérieures',
     ['commerce', 'residentiel', 'tertiaire'],
     'Éclairage mural direct, indirect ou double flux. Utilisées en couloir '
     'd’hôtel, en tête de lit et en éclairage d’accompagnement d’escalier.',
     ['flux', 'puissance', 'temperature', 'irc', 'format', 'materiau', 'pose']),

    ('interieur', 'Luminaires de bureau et lampes de travail',
     ['tertiaire', 'industriel', 'residentiel'],
     'Lampes à poser, sur pince ou sur pied, et éclairages de poste. '
     'L’éblouissement et la gradation individuelle priment sur le flux total.',
     ['flux', 'puissance', 'temperature', 'irc', 'tension', 'pilotage', 'materiau']),

    # --- Éclairage extérieur et public -------------------------------------
    ('exterieur', 'Lanternes routières LED',
     ['voirie'],
     'Le luminaire d’éclairage public au sens strict, monté en tête de mât ou '
     'sur crosse. C’est ici que la classe photométrique de la voie décide du '
     'produit, avant toute considération esthétique.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'ip', 'ik', 'photo', 'pilotage', 'support']),

    ('exterieur', 'Mâts, crosses et candélabres',
     ['voirie', 'chantier'],
     'La structure qui porte le luminaire : mâts droits, mâts à crosse, '
     'consoles murales et platines d’ancrage. Le dimensionnement dépend de la '
     'prise au vent et de la hauteur de feu retenue.',
     ['materiau', 'format', 'support', 'vent', 'coloris', 'pose']),

    ('exterieur', 'Luminaires résidentiels de voirie',
     ['voirie', 'residentiel'],
     'Lanternes de style, bornes de trottoir et luminaires de lotissement. '
     'La contrainte dominante est la limitation du flux vers le ciel et vers '
     'les façades.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'photo', 'materiau', 'coloris']),

    ('exterieur', 'Bornes et potelets lumineux',
     ['voirie', 'residentiel', 'commerce'],
     'Éclairage bas pour cheminements piétons, parvis et jardins. Le point '
     'faible connu de la catégorie est le vandalisme : la tenue aux chocs se '
     'regarde avant le flux.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'format', 'materiau', 'pose']),

    ('exterieur', 'Appliques et hublots extérieurs',
     ['residentiel', 'commerce', 'industriel'],
     'Éclairage de façade fonctionnel : entrées, coursives, quais et abords de '
     'bâtiment. Étanchéité et tenue à la corrosion selon l’exposition.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'materiau', 'pose', 'pilotage']),

    ('exterieur', 'Encastrés de sol et spots enterrés',
     ['voirie', 'commerce', 'evenementiel'],
     'Mise en lumière de façades, d’arbres et de cheminements depuis le sol. '
     'La résistance à la charge roulante et l’évacuation de l’eau conditionnent '
     'la pose plus que la photométrie.',
     ['flux', 'puissance', 'temperature', 'faisceau', 'ip', 'ik', 'materiau', 'pose']),

    ('exterieur', 'Éclairage de passage piéton',
     ['voirie'],
     'Dispositifs dédiés à la traversée piétonne, en éclairage positif ou '
     'négatif. L’objectif est le contraste du piéton sur la chaussée, pas le '
     'niveau d’éclairement de la zone.',
     ['flux', 'puissance', 'temperature', 'faisceau', 'ip', 'photo', 'support', 'pose']),

    ('exterieur', 'Éclairage solaire autonome',
     ['voirie', 'residentiel', 'chantier'],
     'Ensembles panneau, batterie et luminaire, sans raccordement au réseau. '
     'Le dimensionnement se fait sur l’autonomie visée en période défavorable, '
     'pas sur le flux nominal.',
     ['flux', 'puissance', 'temperature', 'ip', 'autonomie', 'support', 'pilotage']),

    ('exterieur', 'Éclairage de tunnel et d’ouvrage d’art',
     ['tunnel', 'voirie'],
     'Luminaires de section courante, de renforcement d’entrée et de secours. '
     'La catégorie est à part : elle se dimensionne sur l’adaptation visuelle à '
     'l’entrée et sur la tenue au lavage haute pression.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'photo', 'materiau', 'pilotage']),

    ('exterieur', 'Projecteurs de parking et d’aire de stationnement',
     ['voirie', 'commerce', 'industriel'],
     'Éclairage de surfaces ouvertes sur mât ou en applique haute. '
     'L’uniformité et la maîtrise de l’éblouissement pèsent plus que la '
     'puissance installée.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'ip', 'faisceau', 'support', 'pilotage']),

    # --- Éclairage industriel ----------------------------------------------
    ('industriel', 'Cloches et luminaires High Bay',
     ['industriel'],
     'Éclairage de grande hauteur pour ateliers, entrepôts et halls. Le choix '
     'du réflecteur dépend directement de la hauteur sous ferme et de la '
     'largeur des allées.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'irc', 'ip', 'faisceau', 'pilotage']),

    ('industriel', 'Réglettes étanches',
     ['industriel', 'commerce'],
     'Linéaires étanches pour parkings, réserves, ateliers et locaux humides. '
     'Le format et le raccordement en ligne continue déterminent le nombre de '
     'points d’alimentation.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'ip', 'ik', 'format', 'pose']),

    ('industriel', 'Luminaires pour atmosphères explosives',
     ['industriel'],
     'Matériel destiné aux zones classées : chimie, pétrole, silos, '
     'traitement des poudres. Ces produits ne se substituent pas entre eux — '
     'la zone d’installation impose le matériel, jamais l’inverse.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'tension', 'materiau', 'pose']),

    ('industriel', 'Éclairage de quai et de zone logistique',
     ['industriel'],
     'Bras articulés de quai, éclairage de niveleur et de zone de chargement. '
     'La contrainte est mécanique avant d’être lumineuse : le luminaire prend '
     'des coups.',
     ['flux', 'puissance', 'temperature', 'ip', 'ik', 'support', 'tension', 'pose']),

    ('industriel', 'Éclairage de machine et de poste de travail',
     ['industriel'],
     'Luminaires de carter, de commande numérique et de poste d’assemblage. '
     'Alimentation en très basse tension et étanchéité aux fluides de coupe.',
     ['flux', 'puissance', 'temperature', 'irc', 'ip', 'ik', 'tension', 'support']),

    ('industriel', 'Projecteurs de cour et d’enceinte industrielle',
     ['industriel', 'voirie'],
     'Éclairage de périmètre, de voie de circulation interne et de zone de '
     'stockage extérieur. Souvent couplé à de la détection et à un régime de '
     'nuit réduit.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'ip', 'faisceau', 'support', 'pilotage']),

    # --- Projecteurs et scénique -------------------------------------------
    ('projecteurs', 'Projecteurs d’inondation LED',
     ['voirie', 'industriel', 'chantier', 'commerce'],
     'Le projecteur généraliste, du petit modèle de façade au projecteur de '
     'mât. L’angle de faisceau et la maîtrise de la lumière intrusive sont les '
     'deux vrais critères.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'ip', 'ik', 'faisceau', 'support']),

    ('projecteurs', 'Projecteurs de terrain sportif',
     ['evenementiel', 'voirie'],
     'Éclairage de stades, terrains d’entraînement et salles. Le niveau requis '
     'dépend du niveau de compétition et de la présence de caméras, ce qui se '
     'décide au dossier, pas au catalogue.',
     ['flux', 'puissance', 'efficacite', 'temperature', 'irc', 'ip', 'faisceau', 'support']),

    ('projecteurs', 'Projecteurs asymétriques de façade',
     ['commerce', 'voirie', 'evenementiel'],
     'Mise en valeur de façades, de panneaux et de surfaces verticales avec un '
     'faisceau dissymétrique qui évite de renvoyer la lumière vers le ciel.',
     ['flux', 'puissance', 'temperature', 'irc', 'ip', 'faisceau', 'materiau', 'pose']),

    ('projecteurs', 'Projecteurs motorisés et lyres',
     ['evenementiel'],
     'Projecteurs asservis pour scène, plateau et événement. Se commandent '
     'toujours avec leur protocole de pilotage : un projecteur asservi sans '
     'console est un luminaire fixe cher.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'tension', 'pilotage', 'materiau']),

    ('projecteurs', 'Barres LED, wash et éclairage couleur',
     ['evenementiel', 'commerce'],
     'Sources colorées RGB et RGBW pour ambiance, plateau télé et animation '
     'commerciale. Le rendu sur la peau et sur les textiles se vérifie en '
     'essai, pas sur une fiche.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'ip', 'pilotage', 'coloris']),

    ('projecteurs', 'Découpes, PC et poursuites',
     ['evenementiel'],
     'Projecteurs de théâtre à optique fixe ou zoom. Catégorie où le poids, la '
     'longueur et l’accroche comptent autant que la photométrie.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'tension', 'materiau', 'support']),

    # --- Sécurité et secours ------------------------------------------------
    ('secours', 'Blocs autonomes d’éclairage de sécurité',
     ['tertiaire', 'commerce', 'industriel'],
     'Blocs d’évacuation et d’ambiance alimentés par batterie intégrée. '
     'L’autonomie et le régime de test conditionnent l’exploitation autant que '
     'le produit lui-même.',
     ['flux', 'puissance', 'autonomie', 'ip', 'ik', 'format', 'pose', 'pilotage']),

    ('secours', 'Blocs d’ambiance et anti-panique',
     ['commerce', 'tertiaire', 'industriel'],
     'Maintien d’un niveau minimal dans les grands volumes pour éviter le '
     'mouvement de foule. Dimensionnés à la surface, pas au point de sortie.',
     ['flux', 'puissance', 'autonomie', 'ip', 'format', 'pose', 'pilotage']),

    ('secours', 'Signalétique d’évacuation lumineuse',
     ['tertiaire', 'commerce', 'industriel', 'tunnel'],
     'Étiquettes et blocs de balisage indiquant les issues et les '
     'cheminements. La distance de reconnaissance dépend du format du '
     'pictogramme, ce qui se calcule sur plan.',
     ['flux', 'autonomie', 'format', 'ip', 'pose', 'coloris']),

    ('secours', 'Éclairage de secours sur source centrale',
     ['industriel', 'tertiaire', 'tunnel'],
     'Alternative aux blocs autonomes : luminaires alimentés depuis une '
     'centrale. Choix structurant, qui se décide au stade de la conception '
     'électrique du bâtiment.',
     ['flux', 'puissance', 'tension', 'autonomie', 'ip', 'pose', 'pilotage']),

    ('secours', 'Blocs portables et projecteurs de secours',
     ['industriel', 'chantier', 'tunnel'],
     'Lampes portatives, projecteurs sur batterie et éclairage d’intervention. '
     'Se jugent sur l’autonomie réelle en usage continu et sur la tenue à la '
     'chute.',
     ['flux', 'puissance', 'autonomie', 'ip', 'ik', 'tension', 'materiau']),

    ('secours', 'Télécommandes et systèmes de test automatique',
     ['tertiaire', 'commerce', 'industriel'],
     'Mise au repos, test périodique et report de défaut des installations de '
     'sécurité. Ce qui fait gagner du temps n’est pas le test, c’est le '
     'rapport qu’il produit.',
     ['tension', 'pilotage', 'format', 'pose']),

    # --- Décoratif ----------------------------------------------------------
    ('decoratif', 'Guirlandes et cordons lumineux',
     ['evenementiel', 'commerce', 'residentiel'],
     'Guirlandes guinguette, cordons et rideaux lumineux, en intérieur comme '
     'en extérieur. La longueur raccordable en série est la limite pratique la '
     'plus souvent oubliée.',
     ['flux', 'puissance', 'temperature', 'ip', 'format', 'tension', 'coloris', 'pose']),

    ('decoratif', 'Décors lumineux de rue et motifs saisonniers',
     ['voirie', 'commerce', 'evenementiel'],
     'Motifs sur candélabre, traversées de rue et sujets de place. Le sujet '
     'principal est la fixation et la prise au vent, pas la lumière.',
     ['puissance', 'temperature', 'ip', 'format', 'support', 'vent', 'coloris', 'pose']),

    ('decoratif', 'Rubans LED et profilés d’intégration',
     ['commerce', 'residentiel', 'tertiaire'],
     'Rubans à couper, profilés aluminium et diffuseurs pour corniches, '
     'niches et mobilier. Se commandent avec leur alimentation : un ruban seul '
     'ne s’installe pas.',
     ['flux', 'puissance', 'temperature', 'irc', 'ip', 'tension', 'format', 'pilotage']),

    ('decoratif', 'Luminaires d’ambiance et lampes à poser',
     ['commerce', 'residentiel'],
     'Lampes de table, lampadaires sur pied et luminaires nomades sur '
     'batterie, pour l’hôtellerie et la restauration.',
     ['flux', 'puissance', 'temperature', 'irc', 'autonomie', 'materiau', 'coloris', 'pilotage']),

    ('decoratif', 'Éclairage de vitrine et de mobilier',
     ['commerce'],
     'Réglettes de tablette, spots de gondole et éclairage de présentoir. Le '
     'rendu des couleurs est le critère commercial : c’est lui qui fait ou '
     'défait la marchandise.',
     ['flux', 'puissance', 'temperature', 'irc', 'faisceau', 'format', 'tension', 'pose']),

    # --- Composants et pilotage ---------------------------------------------
    ('composants', 'Drivers et alimentations LED',
     ['industriel', 'tertiaire', 'commerce', 'residentiel'],
     'Alimentations à courant ou à tension constante, graduables ou non. Se '
     'choisissent sur la plage de sortie ET sur le protocole, jamais sur la '
     'seule puissance.',
     ['puissance', 'tension', 'ip', 'format', 'pilotage', 'duree', 'pose']),

    ('composants', 'Détecteurs de présence et de luminosité',
     ['tertiaire', 'industriel', 'residentiel', 'voirie'],
     'Détection infrarouge, hyperfréquence et crépusculaire. La zone de '
     'détection réelle dépend de la hauteur de pose, ce qui se règle sur site.',
     ['tension', 'ip', 'format', 'faisceau', 'pilotage', 'pose']),

    ('composants', 'Variateurs, interrupteurs et appareillage',
     ['tertiaire', 'residentiel', 'commerce'],
     'Commande murale, variation en coupure de phase ou par bus. La '
     'compatibilité variateur-source est la première cause de scintillement '
     'après installation.',
     ['tension', 'puissance', 'format', 'pilotage', 'coloris', 'pose']),

    ('composants', 'Systèmes de gestion d’éclairage de bâtiment',
     ['tertiaire', 'commerce', 'industriel'],
     'Passerelles, contrôleurs et capteurs pour la gestion adressée d’un '
     'bâtiment. La valeur est dans le paramétrage et la reprise des scénarios, '
     'pas dans le matériel.',
     ['tension', 'pilotage', 'format', 'pose']),

    ('composants', 'Télégestion de l’éclairage public',
     ['voirie', 'tunnel'],
     'Contrôleurs de point lumineux, armoires communicantes et supervision de '
     'parc. Permettent l’abaissement de nuit et la détection de panne à '
     'distance.',
     ['tension', 'ip', 'pilotage', 'support', 'format']),

    ('composants', 'Pupitres, contrôleurs DMX et splitters',
     ['evenementiel'],
     'Consoles, boîtiers d’adressage et amplificateurs de ligne pour '
     'installations scéniques. Le nombre d’univers disponibles borne la taille '
     'du plateau.',
     ['tension', 'pilotage', 'format', 'materiau', 'pose']),

    ('composants', 'Câbles, connecteurs et boîtiers de raccordement',
     ['industriel', 'voirie', 'chantier', 'evenementiel'],
     'Câblage, presse-étoupes, connecteurs étanches et boîtes de dérivation. '
     'C’est l’étanchéité du raccordement, pas celle du luminaire, qui lâche en '
     'premier sur un chantier extérieur.',
     ['tension', 'ip', 'materiau', 'format', 'pose']),

    # --- Signalisation verticale --------------------------------------------
    ('verticale', 'Panneaux de danger',
     ['voirie', 'chantier'],
     'Panneaux triangulaires annonçant un risque sur la voie. La gamme et la '
     'classe de rétroréflexion se choisissent selon la vitesse pratiquée et '
     'l’éclairage de la section.',
     ['gamme', 'retro', 'format', 'support', 'materiau', 'pose']),

    ('verticale', 'Panneaux d’interdiction et d’obligation',
     ['voirie', 'industriel', 'chantier'],
     'Panneaux circulaires de prescription. Ce sont les plus contestés en cas '
     'de litige, donc ceux dont la pose et la visibilité doivent être les plus '
     'soignées.',
     ['gamme', 'retro', 'format', 'support', 'materiau', 'pose']),

    ('verticale', 'Panneaux de priorité et d’intersection',
     ['voirie'],
     'Cédez-le-passage, stop et régimes de priorité. Leur lisibilité de nuit '
     'dépend entièrement du film rétroréfléchissant retenu.',
     ['gamme', 'retro', 'format', 'support', 'materiau', 'pose']),

    ('verticale', 'Panneaux de direction et jalonnement',
     ['voirie'],
     'Cartouches, flèches, panneaux de position et ensembles de jalonnement. '
     'Fabrication sur mesure : les mentions, la police et les hauteurs de '
     'lettre se valident avant découpe.',
     ['gamme', 'retro', 'format', 'support', 'materiau', 'coloris', 'vent']),

    ('verticale', 'Panneaux d’indication et de service',
     ['voirie', 'commerce', 'residentiel'],
     'Stationnement, services, équipements et informations locales, y compris '
     'la signalisation de parking privé et de zone d’activité.',
     ['gamme', 'retro', 'format', 'support', 'materiau', 'coloris', 'pose']),

    ('verticale', 'Panonceaux et compléments',
     ['voirie', 'chantier'],
     'Compléments placés sous un panneau pour en préciser la portée, la '
     'distance ou la catégorie de véhicule concernée. Se commandent avec le '
     'panneau qu’ils accompagnent.',
     ['gamme', 'retro', 'format', 'support', 'materiau']),

    ('verticale', 'Supports, mâts et colliers de fixation',
     ['voirie', 'chantier'],
     'Poteaux, massifs, brides et bracelets. Le support est dimensionné par la '
     'surface du panneau et par le vent, pas par le poids du panneau.',
     ['materiau', 'format', 'support', 'vent', 'coloris', 'pose']),

    ('verticale', 'Miroirs routiers et de sortie',
     ['voirie', 'industriel', 'residentiel'],
     'Miroirs de sortie de propriété, d’intersection sans visibilité et de '
     'quai industriel. Le diamètre se déduit de la distance d’observation.',
     ['format', 'support', 'materiau', 'vent', 'pose']),

    # --- Signalisation horizontale ------------------------------------------
    ('horizontale', 'Peintures routières et enduits',
     ['voirie', 'chantier'],
     'Produits appliqués pour le marquage au sol, en peinture, enduit à froid '
     'ou à chaud. Le choix dépend du trafic supporté et de la durée de '
     'service visée.',
     ['materiau', 'coloris', 'retro', 'pose', 'duree']),

    ('horizontale', 'Bandes préfabriquées thermocollantes',
     ['voirie', 'chantier', 'industriel'],
     'Marquages livrés prédécoupés — flèches, pictogrammes, passages piétons — '
     'appliqués au chalumeau. Pose rapide, sans temps de séchage.',
     ['materiau', 'coloris', 'retro', 'format', 'pose', 'duree']),

    ('horizontale', 'Microbilles et produits de saupoudrage',
     ['voirie'],
     'Billes de verre et charges antidérapantes ajoutées au marquage frais. '
     'C’est ce saupoudrage qui rend le marquage visible sous les phares la '
     'nuit.',
     ['materiau', 'retro', 'pose']),

    ('horizontale', 'Plots et clous de marquage rétroréfléchissants',
     ['voirie', 'tunnel'],
     'Dispositifs ponctuels collés ou ancrés, en version passive ou lumineuse. '
     'Utilisés en délinéation de virage, en tunnel et en séparation de voies.',
     ['retro', 'format', 'materiau', 'ip', 'autonomie', 'pose']),

    ('horizontale', 'Marquage de parking et de site logistique',
     ['industriel', 'commerce'],
     'Places, allées de circulation, zones de stockage et cheminements '
     'piétons en intérieur. Les produits d’intérieur et d’extérieur ne sont '
     'pas interchangeables.',
     ['materiau', 'coloris', 'format', 'pose', 'duree']),

    # --- Signalisation temporaire -------------------------------------------
    ('temporaire', 'Panneaux de chantier temporaires',
     ['chantier', 'voirie'],
     'Signalisation d’approche, de position et de fin de chantier, sur pied ou '
     'sur support mobile. Se dépose intégralement à la fin des travaux : '
     'l’oubli d’un panneau engage la responsabilité du maître d’ouvrage.',
     ['gamme', 'retro', 'format', 'support', 'materiau', 'vent', 'pose']),

    ('temporaire', 'Cônes et balises de chantier',
     ['chantier', 'voirie'],
     'Cônes, balises K5, chandelles et piquets. Le lestage et la hauteur '
     'décident de la tenue au souffle des poids lourds.',
     ['retro', 'format', 'materiau', 'coloris', 'vent', 'pose']),

    ('temporaire', 'Barrières et séparateurs modulaires',
     ['chantier', 'voirie', 'evenementiel'],
     'Barrières de police, barrières de chantier et séparateurs lestables à '
     'l’eau ou au sable. Servent aussi en canalisation de foule.',
     ['materiau', 'format', 'coloris', 'vent', 'pose']),

    ('temporaire', 'Lampes de balisage et feux de chantier',
     ['chantier', 'voirie'],
     'Feux clignotants, rampes lumineuses et lampes de balisage sur pile ou '
     'batterie. L’autonomie annoncée s’effondre par grand froid, ce qui se '
     'vérifie en conditions réelles.',
     ['flux', 'autonomie', 'ip', 'ik', 'coloris', 'support', 'pose']),

    ('temporaire', 'Panneaux à messages variables et flèches lumineuses',
     ['chantier', 'voirie'],
     'Remorques à message, flèches de rabattement et panneaux d’alerte '
     'mobiles. Le paramétrage du message et son horaire d’affichage font '
     'partie de la prestation.',
     ['flux', 'autonomie', 'ip', 'format', 'support', 'pilotage', 'coloris']),

    ('temporaire', 'Équipements de protection du personnel de chantier',
     ['chantier'],
     'Vêtements haute visibilité, gyrophares de véhicule et kits de '
     'signalisation embarqués. Complètent la signalisation fixe du chantier.',
     ['retro', 'format', 'coloris', 'materiau', 'tension']),

    # --- Équipements de sécurité routière -----------------------------------
    ('equipements', 'Dispositifs de retenue et glissières',
     ['voirie', 'tunnel'],
     'Glissières métalliques, séparateurs béton et extrémités de file. Le '
     'niveau de retenue se choisit sur étude d’accidentologie, jamais sur '
     'catalogue.',
     ['materiau', 'format', 'support', 'pose', 'vent']),

    ('equipements', 'Ralentisseurs et coussins',
     ['voirie', 'residentiel', 'industriel'],
     'Dos d’âne, coussins et plateaux modulaires. La géométrie détermine la '
     'vitesse effective de franchissement et la gêne pour les bus.',
     ['materiau', 'format', 'coloris', 'retro', 'pose']),

    ('equipements', 'Bornes, potelets et barrières anti-intrusion',
     ['voirie', 'commerce', 'residentiel'],
     'Potelets fixes, amovibles et escamotables, bornes de protection de '
     'façade et arceaux. Le niveau de protection réel dépend du massif, pas de '
     'la borne.',
     ['materiau', 'format', 'support', 'retro', 'coloris', 'pose']),

    ('equipements', 'Balises de virage et délinéateurs',
     ['voirie', 'tunnel'],
     'Balises latérales, délinéateurs de virage et bornes de guidage. Ils '
     'dessinent le tracé de la route avant que les phares n’atteignent la '
     'chaussée.',
     ['retro', 'format', 'materiau', 'support', 'coloris', 'pose']),

    ('equipements', 'Feux tricolores et signalisation lumineuse',
     ['voirie'],
     'Têtes de feux, feux piétons, répétiteurs et contrôleurs de carrefour. '
     'Se traitent en installation complète, contrôleur compris.',
     ['flux', 'puissance', 'tension', 'ip', 'ik', 'support', 'pilotage', 'format']),

    ('equipements', 'Radars pédagogiques et comptage',
     ['voirie', 'residentiel'],
     'Afficheurs de vitesse et compteurs de trafic sur mât ou candélabre. '
     'Leur intérêt principal est la donnée collectée, exploitable pour '
     'justifier un aménagement.',
     ['flux', 'autonomie', 'ip', 'format', 'support', 'pilotage', 'tension']),

    ('equipements', 'Protection des piétons et mobilier urbain de sécurité',
     ['voirie', 'residentiel', 'commerce'],
     'Barrières urbaines, garde-corps de trottoir et protections d’abords '
     'd’école. Mobilier de voirie dont la fonction première est la sécurité.',
     ['materiau', 'format', 'support', 'coloris', 'retro', 'pose']),
]

# ---------------------------------------------------------------------------
# Les deux blocs de texte honnetes en bas de page.
# ---------------------------------------------------------------------------
NOTE = (
    'Chaque carte est une CATÉGORIE de produit, pas une référence commerciale. '
    'Elle indique ce que la catégorie regroupe, les usages où elle intervient, '
    'et surtout la grille de caractéristiques sur laquelle deux produits de '
    'cette catégorie se comparent. C’est cette grille qui structure le '
    'catalogue : dès que les données fournisseur arrivent, chaque référence se '
    'range dans une catégorie et hérite de ses champs. La page est donc déjà '
    'la colonne vertébrale du catalogue définitif, pas une maquette à jeter.'
)

AVERTISSEMENT = (
    'Aucune valeur chiffrée n’est attribuée à un produit sur cette page : ni '
    'flux, ni indice de protection, ni classe photométrique, ni classe de '
    'rétroréflexion, ni prix. Les intitulés qui apparaissent sont des NOMS DE '
    'CHAMPS à renseigner, jamais des valeurs certifiées. Je n’ai mesuré aucun '
    'produit et aucune donnée fournisseur ne m’a été transmise — annoncer un '
    'indice d’étanchéité ou une classe de performance que personne n’a '
    'vérifiée exposerait le site sur le seul terrain où un acheteur '
    'professionnel ne pardonne pas. Aucune marque de fabricant n’est citée '
    'pour la même raison. Un test automatique refuse la page si une seule '
    'valeur chiffrée de ce type y apparaît, disclaimer compris.'
)
