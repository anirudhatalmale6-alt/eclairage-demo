# -*- coding: utf-8 -*-
"""Rend UNE page autonome : le catalogue éclairage + signalisation.

Le client a demandé « éclairage donc lampe inclus / tout les produits dérivés
de lumière / et éclairage et panneaux de signalisation ». Une page, deux
grandes familles qui se filtrent.

Comme sur le répertoire droits humains : tout tient dans un seul fichier, rien
n'est rechargé, et SANS JAVASCRIPT la liste complète est déjà dans le HTML.
Le script filtre ce qui est déjà là, il ne le fabrique pas — c'est ce qui rend
la page indexable, ce qui est tout l'intérêt d'un catalogue.
"""
import html, sys
import data as D

SORTIE = sys.argv[1] if len(sys.argv) > 1 else 'index.html'


# ---------------------------------------------------------------------------
# CONTROLE D'INTEGRITE. Une faute de frappe dans un code de famille ou d'usage
# ne casse rien : la carte s'affiche et ne sort plus jamais d'un filtre. C'est
# exactement le genre de bug qu'on ne voit pas. On refuse donc de construire.
# ---------------------------------------------------------------------------
def verifier():
    fam = {c: d for c, _, d in D.FAMILLES}
    us = {c for c, _ in D.USAGES}
    car = {c for c, _ in D.CARACS}
    dom = {c for c, _ in D.DOMAINES}
    err = []
    for c, nom, dm in D.FAMILLES:
        if dm not in dom:
            err.append('famille %s : domaine inconnu %r' % (c, dm))
    for i, (f, nom, usages, desc, caracs) in enumerate(D.CATEGORIES):
        if f not in fam:
            err.append('%s : famille inconnue %r' % (nom, f))
        if not usages:
            err.append('%s : aucun usage' % nom)
        for u in usages:
            if u not in us:
                err.append('%s : usage inconnu %r' % (nom, u))
        for k in caracs:
            if k not in car:
                err.append('%s : caractéristique inconnue %r' % (nom, k))
        if len(set(usages)) != len(usages):
            err.append('%s : usage en double' % nom)
        if len(set(caracs)) != len(caracs):
            err.append('%s : caractéristique en double' % nom)
    noms = [c[1] for c in D.CATEGORIES]
    for n in set(noms):
        if noms.count(n) > 1:
            err.append('catégorie en double : %s' % n)
    # Une famille vide laisse une entree morte dans le menu deroulant.
    for c, nom, _ in D.FAMILLES:
        if not any(x[0] == c for x in D.CATEGORIES):
            err.append('famille sans aucune catégorie : %s' % nom)
    # Un usage jamais utilise laisse un filtre qui ne renvoie rien.
    for c, nom in D.USAGES:
        if not any(c in x[2] for x in D.CATEGORIES):
            err.append('usage jamais employé : %s' % nom)
    for c, nom in D.CARACS:
        if not any(c in x[4] for x in D.CATEGORIES):
            err.append('caractéristique jamais employée : %s' % nom)
    if err:
        raise SystemExit('DONNEES INVALIDES :\n  - ' + '\n  - '.join(err))


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{--bg:__BG__;--c:__C__;--l:__L__;--e:__E__;--tx:__TX__;--mu:__MU__;
      --ac:__AC__;--acd:__ACD__}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--tx);
  font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
  "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--ac)}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
h1,h2,h3{color:var(--e);line-height:1.16;letter-spacing:-.02em;margin:0 0 12px;font-weight:800}

.demo{background:var(--e);color:#dfe4ec;font-size:12.5px;padding:9px 16px;text-align:center}
.demo b{color:#ffc98a}

header.top{background:var(--c);border-bottom:1px solid var(--l);position:sticky;top:0;z-index:30}
/* padding:15px 22px, PAS 15px 0. Le meme <div> porte « wrap » et « tbar » :
   un raccourci « padding:15px 0 » ici efface le padding horizontal de .wrap
   (meme specificite, declaree plus bas) et colle le logo au bord gauche de
   l'ecran. Rien ne deborde, donc aucun test de debordement ne le voit — la
   barre est simplement desalignee de 22px avec le reste de la page. */
.tbar{display:flex;align-items:center;gap:20px;padding:15px 22px;flex-wrap:wrap}
.logo{font-weight:800;font-size:16px;letter-spacing:.04em;color:var(--e)}
.tbar nav{margin-left:auto;display:flex;gap:20px;font-size:14.5px}
.tbar nav a{color:var(--mu);text-decoration:none}
.tbar nav a:hover{color:var(--ac)}

.hero{background:var(--c);border-bottom:1px solid var(--l);padding:44px 0 38px}
.hero h1{font-size:clamp(27px,4vw,42px);max-width:21ch}
.hero p{font-size:17.5px;color:var(--mu);max-width:68ch;margin:0 0 20px}
.kpi{display:flex;flex-wrap:wrap;gap:10px 34px;margin-top:22px}
.kpi div b{display:block;font-size:26px;font-weight:800;color:var(--e);
  font-variant-numeric:tabular-nums;line-height:1.1}
.kpi div span{font-size:13px;color:var(--mu)}

main{padding:26px 0 60px}

/* Le sommaire des familles. Il sert deux publics : le visiteur, qui voit d'un
   coup ce que couvre la page, et le moteur de recherche, qui lit un plan
   complet en texte meme si le JavaScript ne s'execute jamais. */
.plan{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 0 22px}
.plan section{background:var(--c);border:1px solid var(--l);border-radius:12px;padding:16px 18px}
.plan h2{font-size:15px;margin:0 0 11px;letter-spacing:.02em;text-transform:uppercase}
.plan ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.plan button{font:inherit;font-size:13.5px;cursor:pointer;background:#f6f7f9;
  border:1px solid var(--l);border-radius:99px;padding:6px 12px;color:var(--tx);text-align:left}
.plan button:hover{border-color:var(--ac);color:var(--acd)}
.plan button b{font-variant-numeric:tabular-nums;color:var(--mu);font-weight:600}

.filtres{background:var(--c);border:1px solid var(--l);border-radius:12px;
  padding:16px;margin:0 0 18px;display:grid;grid-template-columns:repeat(4,1fr);gap:13px}
.f{display:flex;flex-direction:column;gap:6px;min-width:0}
.f label{font-size:12.5px;font-weight:700;color:var(--e);letter-spacing:.02em}
.f select,.f input{width:100%;min-width:0;font:inherit;font-size:15px;color:var(--e);
  background:#fff;border:1px solid var(--l);border-radius:8px;padding:10px 11px}
.f select:focus,.f input:focus{outline:2px solid var(--ac);outline-offset:1px}
.barre{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:0 0 14px}
.compte{font-size:16px;font-weight:700;color:var(--e)}
.raz{font:inherit;font-size:14px;cursor:pointer;background:transparent;color:var(--ac);
  border:1px solid var(--l);border-radius:8px;padding:7px 13px}
.raz:hover{border-color:var(--ac)}

.liste{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.o{background:var(--c);border:1px solid var(--l);border-radius:12px;padding:17px 18px;
  display:flex;flex-direction:column;gap:9px;min-width:0}
/* « hidden » vaut display:none dans la feuille du navigateur, mais cette
   regle vient d'une selection d'element et « .o{display:flex} » la bat. Sans
   la ligne ci-dessous le filtre pose bien hidden et les cartes restent
   AFFICHEES : le compteur dit 6, la page en montre 84. */
.o[hidden]{display:none}
.o h3{font-size:16.5px;margin:0;line-height:1.3}
.o .ou{font-size:13px;color:var(--mu);margin:0;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.o .ou .fam{font-weight:600;color:var(--tx)}
.o p.d{font-size:14.5px;color:var(--tx);margin:0;flex:1 1 auto}

.dm{font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;
  padding:3px 9px;border-radius:99px;white-space:nowrap;
  background:#fbf0e2;color:#7a4300;border:1px solid #efdcc2}
.dm-signalisation{background:#e9eff7;color:#1b3f6b;border-color:#ccdbec}

.tags{display:flex;flex-wrap:wrap;gap:5px;margin:0}
.tags span{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:99px;
  background:#eef1f6;color:#2b3d57;border:1px solid #d9e0ea;white-space:nowrap}

.car{margin:0;border-top:1px dashed var(--l);padding-top:9px}
.car b{display:block;font-size:11px;font-weight:800;letter-spacing:.04em;
  text-transform:uppercase;color:var(--mu);margin:0 0 6px}
.car ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:5px}
.car li{font-size:11.5px;padding:3px 9px;border-radius:6px;background:#f5f6f8;
  color:var(--tx);border:1px solid var(--l);white-space:nowrap}

.vide{grid-column:1/-1;background:var(--c);border:1px dashed var(--l);border-radius:12px;
  padding:26px;color:var(--mu);margin:0}

.note{background:var(--c);border:1px solid var(--l);border-left:4px solid var(--ac);
  border-radius:0 10px 10px 0;padding:15px 18px;margin:24px 0 0;font-size:14.5px;color:var(--tx)}
.note b{display:block;color:var(--e);margin-bottom:4px}
.avert{background:#fdf8ec;border:1px solid #e8d9b0;border-left:4px solid #8a6410;
  border-radius:0 10px 10px 0;padding:15px 18px;margin:14px 0 0;font-size:14px;color:#54400f}
.avert b{display:block;margin-bottom:4px}

footer{border-top:1px solid var(--l);background:var(--c);padding:22px 0 44px;
  color:var(--mu);font-size:13.5px}

@media (max-width:980px){
  .filtres{grid-template-columns:1fr 1fr}
  .liste{grid-template-columns:1fr}
  .plan{grid-template-columns:1fr}
}
@media (max-width:560px){
  .filtres{grid-template-columns:1fr}
  .kpi{gap:10px 22px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

JS = """
const $ = s => document.querySelector(s);

/* On enleve les accents pour que « eclairage » trouve « éclairage » et
   « retroreflexion » trouve « rétroréflexion ». Sur un catalogue technique
   francais, personne ne tape les accents dans un champ de recherche. */
const plat = s => (s || '').toLowerCase()
  .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');

/* Le menu « Famille » est range par domaine. Quand on choisit un domaine, les
   familles de l'autre n'ont plus rien a faire dans la liste : on les retire.
   On met hidden ET disabled — hidden sur <optgroup> n'est pas honore partout,
   disabled l'est toujours. */
function majFamilles(){
  const dom = $('#f-dom').value;
  let perdu = false;
  document.querySelectorAll('#f-fam optgroup').forEach(g => {
    const off = !!dom && g.dataset.dom !== dom;
    g.hidden = off; g.disabled = off;
    if (off && g.contains($('#f-fam').selectedOptions[0] || null)) perdu = true;
  });
  if (perdu) $('#f-fam').value = '';
}

function filtrer(){
  const dom = $('#f-dom').value, fam = $('#f-fam').value,
        us = $('#f-us').value, q = plat($('#f-q').value.trim());
  let n = 0;
  document.querySelectorAll('.o').forEach(el => {
    const d = el.dataset;
    let ok = true;
    if (dom && d.dom !== dom) ok = false;
    if (ok && fam && d.fam !== fam) ok = false;
    /* Une categorie porte PLUSIEURS usages : on teste l'appartenance, pas
       l'egalite, avec des espaces autour pour que « industriel » ne soit pas
       trouve dans un hypothetique « agro-industriel ». */
    if (ok && us && !(' ' + d.us + ' ').includes(' ' + us + ' ')) ok = false;
    if (ok && q && !plat(d.rech).includes(q)) ok = false;
    el.hidden = !ok;
    if (ok) n++;
  });
  const c = $('#compte');
  c.textContent = n === 0 ? 'Aucune catégorie ne correspond'
    : n === 1 ? '1 catégorie' : n + ' catégories';
  $('#vide').hidden = n !== 0;
}

$('#f-dom').addEventListener('change', () => { majFamilles(); filtrer(); });
['#f-fam', '#f-us'].forEach(s => $(s).addEventListener('change', filtrer));
$('#f-q').addEventListener('input', filtrer);

/* Les puces du sommaire pilotent le meme filtre : c'est le meme etat, pas une
   deuxieme mecanique a maintenir. */
document.querySelectorAll('.plan button').forEach(b => {
  b.addEventListener('click', () => {
    $('#f-dom').value = b.dataset.dom;
    majFamilles();
    $('#f-fam').value = b.dataset.fam;
    $('#f-us').value = ''; $('#f-q').value = '';
    filtrer();
    document.getElementById('catalogue').scrollIntoView({block: 'start'});
  });
});

$('#raz').addEventListener('click', () => {
  $('#f-dom').value = ''; $('#f-fam').value = '';
  $('#f-us').value = ''; $('#f-q').value = '';
  majFamilles(); filtrer();
});
majFamilles(); filtrer();
"""


def e(s):
    return html.escape(str(s), quote=True)


def options(paires, vide):
    o = ['<option value="">%s</option>' % e(vide)]
    for code, nom in paires:
        o.append('<option value="%s">%s</option>' % (e(code), e(nom)))
    return ''.join(o)


def options_familles():
    """Le menu des familles, groupe par domaine."""
    o = ['<option value="">Toutes les familles</option>']
    for dcode, dnom in D.DOMAINES:
        o.append('<optgroup data-dom="%s" label="%s">' % (e(dcode), e(dnom)))
        for fcode, fnom, fdom in D.FAMILLES:
            if fdom == dcode:
                o.append('<option value="%s">%s</option>' % (e(fcode), e(fnom)))
        o.append('</optgroup>')
    return ''.join(o)


def carte(cat):
    fam, nom, usages, desc, caracs = cat
    lfam = {c: (n, d) for c, n, d in D.FAMILLES}
    lus = dict(D.USAGES)
    lcar = dict(D.CARACS)
    fnom, dom = lfam[fam]
    dnom = dict(D.DOMAINES)[dom]

    tags = ''.join('<span>%s</span>' % e(lus[u]) for u in usages)
    champs = ''.join('<li>%s</li>' % e(lcar[k]) for k in caracs)
    # La recherche balaie tout ce qui est visible sur la carte, y compris les
    # noms de champs : « rétroréflexion » doit ramener les panneaux.
    rech = ' '.join([nom, fnom, dnom, desc]
                    + [lus[u] for u in usages] + [lcar[k] for k in caracs])

    return (
      '<article class="o" data-dom="%s" data-fam="%s" data-us="%s" data-rech="%s">'
      '<p class="ou"><span class="dm dm-%s">%s</span>'
      '<span class="fam">%s</span></p>'
      '<h3>%s</h3>'
      '<p class="d">%s</p>'
      '<p class="tags">%s</p>'
      '<div class="car"><b>Caractéristiques à renseigner</b><ul>%s</ul></div>'
      '</article>'
      % (e(dom), e(fam), e(' '.join(usages)), e(rech),
         e(dom), e(dnom), e(fnom), e(nom), e(desc), tags, champs))


def plan():
    """Le sommaire : une colonne par domaine, une puce par famille."""
    out = []
    for dcode, dnom in D.DOMAINES:
        puces = []
        for fcode, fnom, fdom in D.FAMILLES:
            if fdom != dcode:
                continue
            n = sum(1 for c in D.CATEGORIES if c[0] == fcode)
            puces.append(
                '<li><button type="button" data-dom="%s" data-fam="%s">%s '
                '<b>%d</b></button></li>' % (e(dcode), e(fcode), e(fnom), n))
        nd = sum(1 for c in D.CATEGORIES
                 if dict((f[0], f[2]) for f in D.FAMILLES)[c[0]] == dcode)
        out.append('<section><h2>%s &mdash; %d catégories</h2><ul>%s</ul></section>'
                   % (e(dnom), nd, ''.join(puces)))
    return ''.join(out)


def page():
    css = (CSS.replace('__BG__', D.FOND).replace('__C__', D.CARTE)
              .replace('__L__', D.LIGNE).replace('__E__', D.ENCRE)
              .replace('__TX__', D.TEXTE).replace('__MU__', D.MUET)
              .replace('__AC__', D.ACCENT).replace('__ACD__', D.ACCENT_D))

    cartes = '\n'.join(carte(c) for c in D.CATEGORIES)
    # Tous les compteurs sont DERIVES. Un nombre recopie a la main est faux des
    # la ligne suivante — c'est deja arrive sur la page 8jet, ou « 6 modèles »
    # est reste affiche au-dessus d'une flotte de 8.
    n_cat = len(D.CATEGORIES)
    n_fam = len(D.FAMILLES)
    n_us = len(D.USAGES)
    n_car = len(D.CARACS)

    return """<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(m)s — %(t)s</title>
<meta name="description" content="Catalogue technique éclairage et signalisation routière : lampes, luminaires intérieurs et extérieurs, éclairage public et industriel, projecteurs, éclairage de sécurité, panneaux de signalisation, marquage au sol et équipements de sécurité routière. Filtrable par famille et par usage.">
<meta name="robots" content="noindex,nofollow">
<style>%(css)s</style>
</head><body>

<div class="demo">Maquette de démonstration &mdash; <b>%(m)s</b> est un intitulé
provisoire. Aucune valeur technique et aucun prix ne figurent sur cette page.</div>

<header class="top"><div class="wrap tbar">
  <span class="logo">%(m)s</span>
  <nav>
    <a href="#catalogue">Catalogue</a>
    <a href="#methode">Méthode</a>
  </nav>
</div></header>

<section class="hero"><div class="wrap">
  <h1>Éclairage et signalisation routière, par famille et par usage</h1>
  <p>Un seul catalogue, deux domaines. De la lampe à visser au panneau de
  direction, en passant par l&rsquo;éclairage public, l&rsquo;éclairage
  industriel, les projecteurs, l&rsquo;éclairage de sécurité, le marquage au
  sol et les équipements de voirie. Filtrez par famille et par usage&nbsp;;
  chaque catégorie annonce la grille de caractéristiques sur laquelle deux
  produits se comparent.</p>
  <div class="kpi">
    <div><b>%(n)d</b><span>catégories de produits</span></div>
    <div><b>%(nf)d</b><span>familles</span></div>
    <div><b>%(nu)d</b><span>usages</span></div>
    <div><b>%(nc)d</b><span>champs techniques</span></div>
  </div>
</div></section>

<main class="wrap">

  <div class="plan">%(plan)s</div>

  <div id="catalogue"></div>

  <div class="filtres">
    <div class="f"><label for="f-dom">Domaine</label>
      <select id="f-dom">%(odom)s</select></div>
    <div class="f"><label for="f-fam">Famille</label>
      <select id="f-fam">%(ofam)s</select></div>
    <div class="f"><label for="f-us">Usage</label>
      <select id="f-us">%(ous)s</select></div>
    <div class="f"><label for="f-q">Recherche</label>
      <input id="f-q" type="search" placeholder="lampe, tunnel, IP, panneau&hellip;"></div>
  </div>

  <div class="barre">
    <span class="compte" id="compte">%(n)d catégories</span>
    <button class="raz" id="raz" type="button">Tout afficher</button>
  </div>

  <div class="liste">
%(cartes)s
    <p class="vide" id="vide" hidden>Aucune catégorie ne correspond à ces
    critères. Élargissez la famille ou l&rsquo;usage.</p>
  </div>

  <div class="note" id="methode"><b>Comment lire ce catalogue</b>
  %(note)s</div>

  <div class="avert"><b>Ce que la page n&rsquo;affiche pas, volontairement</b>
  %(avert)s</div>

</main>

<footer><div class="wrap">%(m)s &mdash; maquette de démonstration. Les
caractéristiques listées sont des champs à renseigner, pas des valeurs
mesurées.</div></footer>

<script>%(js)s</script>
</body></html>""" % {
        'm': e(D.MARQUE), 't': e(D.TITRE), 'css': css, 'js': JS,
        'n': n_cat, 'nf': n_fam, 'nu': n_us, 'nc': n_car,
        'odom': options(D.DOMAINES, 'Les deux domaines'),
        'ofam': options_familles(),
        'ous': options(D.USAGES, 'Tous les usages'),
        'plan': plan(), 'cartes': cartes,
        'note': e(D.NOTE), 'avert': e(D.AVERTISSEMENT),
    }


if __name__ == '__main__':
    verifier()
    with open(SORTIE, 'w', encoding='utf-8') as f:
        f.write(page())
    par_dom = {}
    fdom = dict((f[0], f[2]) for f in D.FAMILLES)
    for c in D.CATEGORIES:
        par_dom[fdom[c[0]]] = par_dom.get(fdom[c[0]], 0) + 1
    print('%d categories (%s), %d familles, %d usages, %d champs -> %s'
          % (len(D.CATEGORIES),
             ', '.join('%s %d' % (k, v) for k, v in par_dom.items()),
             len(D.FAMILLES), len(D.USAGES), len(D.CARACS), SORTIE))
