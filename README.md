# Éclairage & signalisation routière — page unique

Maquette de démonstration. Une seule page, deux domaines qui se filtrent :
l'éclairage au sens large (lampes, luminaires intérieurs et extérieurs,
éclairage public, industriel, projecteurs, éclairage de sécurité, décoratif,
composants et pilotage) et la signalisation routière (verticale, horizontale,
temporaire de chantier, équipements de sécurité routière).

En ligne : https://anirudhatalmale6-alt.github.io/eclairage-demo/

## Ce que la page est

Le **squelette d'un catalogue**. Chaque carte est une *catégorie* de produit,
pas une référence commerciale. Elle porte trois choses :

1. ce que la catégorie regroupe ;
2. les usages où elle intervient (voirie, tunnel, industrie, tertiaire,
   commerce, résidentiel, événementiel, chantier) ;
3. la **grille de caractéristiques** sur laquelle deux produits de cette
   catégorie se comparent.

C'est la grille qui a de la valeur. Une lanterne routière ne se choisit pas
sur une photo : elle se choisit sur le flux, l'étanchéité, la classe
photométrique et la température de couleur. Un panneau se choisit sur la
classe de rétroréflexion, la gamme et le support. Dès que les données
fournisseur arrivent, chaque référence se range dans une catégorie et hérite
de ses champs — la page est donc déjà la colonne vertébrale du catalogue
définitif.

## Ce que la page n'affiche pas, volontairement

Aucune valeur chiffrée attribuée à un produit : ni flux, ni indice
d'étanchéité, ni classe photométrique, ni classe de rétroréflexion, ni prix,
ni délai, ni stock. Les intitulés visibles sont des **noms de champs à
renseigner**, jamais des valeurs certifiées. Aucun nom de fabricant non plus.

Ce n'est pas une précaution de façade : `tests.py` fait échouer la
construction si une seule valeur de ce type apparaît dans le texte rendu,
y compris à l'intérieur de l'avertissement lui-même.

## Technique

* Une page autonome, sans dépendance, sans requête réseau.
* **Sans JavaScript, le catalogue entier est déjà dans le HTML.** Le script
  filtre ce qui est là, il ne le fabrique pas — c'est ce qui rend la page
  indexable, ce qui est tout l'intérêt d'un catalogue.
* Tous les compteurs sont dérivés des données. Aucun nombre n'est écrit à la
  main dans le HTML.

## Regénérer

```
cd src
python3 build.py ../index.html    # refuse de construire si les données sont incohérentes
python3 tests.py                  # 68 contrôles dans un vrai navigateur
```

`src/build.py` contient un contrôle d'intégrité : famille inconnue, usage
inconnu, champ inconnu, doublon, famille vide, usage jamais employé — la
construction s'arrête. Une faute de frappe dans un code de filtre ne casse
rien visuellement, elle rend simplement une carte introuvable ; c'est le genre
de défaut qu'on ne voit jamais à l'œil.
