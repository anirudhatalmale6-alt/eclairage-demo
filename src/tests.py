# -*- coding: utf-8 -*-
"""Presse le catalogue eclairage/signalisation dans un vrai navigateur.

Ce qui compte sur cette page, dans cet ordre :

  1. AUCUNE VALEUR TECHNIQUE INVENTEE. C'est la promesse centrale : pas d'IP,
     pas de flux, pas de classe, pas de prix. Un test le verifie sur le texte
     REELLEMENT AFFICHE, pas sur le fichier source.
  2. LE CATALOGUE ENTIER EST DANS LE HTML SERVI. Un catalogue fabrique par
     JavaScript n'est pas indexable, et un catalogue non indexable ne sert a
     rien. Le script FILTRE ce qui est deja la — verifie sans JavaScript.
  3. Les deux axes se croisent et le compte affiche suit ce qui est visible.
  4. Le menu « Famille » se restreint au domaine choisi, sans laisser une
     selection orpheline derriere lui.
  5. Rien ne deborde, NI A DROITE NI A GAUCHE. Un debordement a gauche ne cree
     aucune barre de defilement : il clippe en silence.

Usage :  python3 tests.py
"""
import os, re, sys
from playwright.sync_api import sync_playwright
import data as D

ICI = os.path.dirname(os.path.abspath(__file__))
# Le depot range les sources dans src/ et la page a la racine ; en local les
# deux sont cote a cote. On cherche donc aux deux endroits plutot que de
# tester un fichier qui n'existe pas et de conclure que la page est cassee.
PAGE = os.path.join(ICI, 'index.html')
if not os.path.exists(PAGE):
    PAGE = os.path.join(os.path.dirname(ICI), 'index.html')
if not os.path.exists(PAGE):
    raise SystemExit('index.html introuvable — lancer build.py d’abord')
URL = 'file://' + PAGE
ok = ko = 0

FDOM = dict((f[0], f[2]) for f in D.FAMILLES)


def t(nom, cond, detail=''):
    global ok, ko
    if cond:
        ok += 1; print('  OK    %s' % nom)
    else:
        ko += 1; print('  ECHEC %s   %s' % (nom, detail))


with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # ---------------------------------------------------------------- 1
    print('\n1. Sans JavaScript, le catalogue est entier')
    sansjs = nav.new_context(java_script_enabled=False)
    p0 = sansjs.new_page()
    p0.set_viewport_size({'width': 1280, 'height': 900})
    p0.goto(URL, wait_until='load')
    n0 = len(p0.query_selector_all('.o'))
    t('les %d categories sont dans le HTML servi' % len(D.CATEGORIES),
      n0 == len(D.CATEGORIES), '%d rendues' % n0)
    caches = p0.evaluate("""() => [...document.querySelectorAll('.o')]
        .filter(e => e.hidden || getComputedStyle(e).display === 'none').length""")
    t('aucune n’est masquee au chargement', caches == 0, str(caches))
    t('le sommaire des familles est en texte, lisible sans script',
      len(p0.query_selector_all('.plan button')) == len(D.FAMILLES),
      str(len(p0.query_selector_all('.plan button'))))
    sansjs.close()

    pg = nav.new_page()
    err = []
    pg.on('pageerror', lambda e: err.append(str(e)))
    pg.on('console', lambda m: err.append(m.text) if m.type == 'error' else None)
    pg.set_viewport_size({'width': 1280, 'height': 900})
    pg.goto(URL, wait_until='load')

    corps = pg.eval_on_selector('body', 'e=>e.innerText')

    # ---------------------------------------------------------------- 2
    print('\n2. Aucune valeur technique, aucune norme, aucun prix')
    INTERDITS = [
        ('un indice de protection chiffre', r'\bIP\s?[0-9]{2}\b'),
        ('une resistance aux chocs chiffree', r'\bIK\s?[0-9]{2}\b'),
        ('une valeur avec unite photometrique ou electrique',
         r'[0-9][0-9\s.,]*\s?(lm/W|lm|lumens|lux|kWh|kW|W|kV|V|K|mA)\b'),
        ('une classe de retroreflexion chiffree', r'\b(classe\s+)?R?A[123]\b|\bclasse\s+[MCS][0-9]\b'),
        ('un prix', r'[0-9][0-9\s.,]*\s?(€|\$|EUR|USD|CAD|DZD|MAD)\b'),
        ('un delai de livraison', r'\b(livr[ée]|d[ée]lai)[^.]{0,20}\b[0-9]+\s?(jours?|semaines?|h)\b'),
        ('un stock', r'\b(en stock|stock\s*:\s*[0-9])'),
        ('une garantie chiffree', r'\bgarantie[^.]{0,20}\b[0-9]+\s?(ans?|mois)\b'),
    ]
    for nom, rx in INTERDITS:
        m = re.search(rx, corps, re.I)
        t('la page n’affiche jamais %s' % nom, m is None,
          repr(corps[max(0, m.start() - 40):m.end() + 20]) if m else '')

    t('aucun classement ni superlatif',
      not re.search(r'\b(top\s*\d|le meilleur|classement|n°\s*1|leader)\b', corps, re.I))
    t('la page dit elle-meme ce qu’elle n’affiche pas',
      'volontairement' in corps.lower())
    t('chaque carte annonce sa grille de champs, pas des valeurs',
      len(pg.query_selector_all('.o .car b')) == len(D.CATEGORIES),
      str(len(pg.query_selector_all('.o .car b'))))

    # ---------------------------------------------------------------- 3
    print('\n3. Les compteurs sont derives des donnees')
    kpi = pg.eval_on_selector_all('.kpi b', 'e=>e.map(x=>x.textContent)')
    t('le bandeau annonce le nombre reel de categories',
      kpi[0] == str(len(D.CATEGORIES)), str(kpi))
    t('le nombre de familles est calcule', kpi[1] == str(len(D.FAMILLES)), str(kpi))
    t('le nombre d’usages est calcule', kpi[2] == str(len(D.USAGES)), str(kpi))
    t('le nombre de champs techniques est calcule',
      kpi[3] == str(len(D.CARACS)), str(kpi))
    txt = pg.eval_on_selector('#compte', 'e=>e.textContent')
    t('le compte de depart vaut le nombre reel',
      str(len(D.CATEGORIES)) in txt, txt)

    print('\n   ... y compris dans le sommaire, famille par famille')
    for fcode, fnom, fdom in D.FAMILLES:
        att = sum(1 for c in D.CATEGORIES if c[0] == fcode)
        lu = pg.eval_on_selector(
            '.plan button[data-fam="%s"] b' % fcode, 'e=>e.textContent')
        t('sommaire : %s' % fnom, lu == str(att), '%s vs %d' % (lu, att))

    # ---------------------------------------------------------------- 4
    print('\n4. Les filtres filtrent, et le compte suit ce qui est visible')

    def visibles():
        # On mesure ce que le navigateur AFFICHE, pas l'attribut qu'on vient de
        # poser. Mesurer l'attribut revient a se demander a soi-meme si on a
        # bien fait ce qu'on vient de faire.
        return pg.evaluate("""() => [...document.querySelectorAll('.o')]
            .filter(e => e.getClientRects().length > 0).length""")

    for dcode, dnom in D.DOMAINES:
        pg.select_option('#f-dom', dcode); pg.wait_for_timeout(120)
        att = sum(1 for c in D.CATEGORIES if FDOM[c[0]] == dcode)
        t('domaine « %s » : %d categories' % (dnom, att),
          visibles() == att, '%d vs %d' % (visibles(), att))
        mauvais = pg.evaluate("""(d) => [...document.querySelectorAll('.o')]
            .filter(e => e.getClientRects().length > 0 && e.dataset.dom !== d)
            .map(e => e.querySelector('h3').textContent)""", dcode)
        t('  aucune carte hors domaine n’est affichee', not mauvais, str(mauvais[:3]))
    pg.click('#raz'); pg.wait_for_timeout(120)
    t('« tout afficher » remet tout',
      visibles() == len(D.CATEGORIES), str(visibles()))

    print('\n   ... sur chaque usage')
    for ucode, unom in D.USAGES:
        pg.select_option('#f-us', ucode); pg.wait_for_timeout(110)
        att = sum(1 for c in D.CATEGORIES if ucode in c[2])
        t('usage « %s » : %d categories' % (unom, att),
          visibles() == att, '%d vs %d' % (visibles(), att))
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 5
    print('\n5. Croiser les deux axes ne rend jamais un compte faux')
    for fcode, ucode in (('exterieur', 'voirie'), ('verticale', 'chantier'),
                         ('secours', 'tunnel'), ('composants', 'evenementiel')):
        pg.click('#raz'); pg.wait_for_timeout(80)
        pg.select_option('#f-fam', fcode)
        pg.select_option('#f-us', ucode); pg.wait_for_timeout(140)
        att = sum(1 for c in D.CATEGORIES if c[0] == fcode and ucode in c[2])
        aff = pg.eval_on_selector('#compte', 'e=>e.textContent')
        t('%s + %s : %d visible(s)' % (fcode, ucode, att),
          visibles() == att, '%d vs %d' % (visibles(), att))
        t('  le compte affiche correspond',
          (str(att) in aff) if att else ('Aucune' in aff), '%s / %d' % (aff, att))
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 6
    print('\n6. Le menu Famille se restreint au domaine choisi')
    pg.select_option('#f-dom', 'signalisation'); pg.wait_for_timeout(140)
    dispo = pg.evaluate("""() => [...document.querySelectorAll('#f-fam optgroup')]
        .filter(g => !g.disabled).flatMap(g => [...g.children].map(o => o.value))""")
    att = sorted(f[0] for f in D.FAMILLES if f[2] == 'signalisation')
    t('seules les familles de signalisation restent selectionnables',
      sorted(dispo) == att, str(sorted(dispo)))

    # Le piege : choisir une famille, PUIS changer de domaine. Si la selection
    # n'est pas remise a zero, le croisement devient impossible a satisfaire et
    # la page se vide sans que rien ne l'explique.
    pg.click('#raz'); pg.wait_for_timeout(80)
    pg.select_option('#f-fam', 'sources'); pg.wait_for_timeout(100)
    pg.select_option('#f-dom', 'signalisation'); pg.wait_for_timeout(140)
    t('une famille devenue hors domaine est relachee',
      pg.eval_on_selector('#f-fam', 'e=>e.value') == '',
      pg.eval_on_selector('#f-fam', 'e=>e.value'))
    att = sum(1 for c in D.CATEGORIES if FDOM[c[0]] == 'signalisation')
    t('la page ne se vide pas pour autant',
      visibles() == att, '%d vs %d' % (visibles(), att))
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 7
    print('\n7. Le sommaire pilote le meme filtre, pas un deuxieme')
    pg.click('.plan button[data-fam="temporaire"]'); pg.wait_for_timeout(200)
    att = sum(1 for c in D.CATEGORIES if c[0] == 'temporaire')
    t('cliquer une puce du sommaire filtre la liste',
      visibles() == att, '%d vs %d' % (visibles(), att))
    t('  et les deux menus refletent ce choix',
      pg.eval_on_selector('#f-dom', 'e=>e.value') == 'signalisation'
      and pg.eval_on_selector('#f-fam', 'e=>e.value') == 'temporaire')
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 8
    print('\n8. La recherche ignore les accents et balaie les champs')
    pg.fill('#f-q', 'retroreflexion'); pg.wait_for_timeout(160)
    att = sum(1 for c in D.CATEGORIES if 'retro' in c[4])
    t('« retroreflexion » sans accent trouve les %d categories concernees' % att,
      visibles() == att, '%d vs %d' % (visibles(), att))
    pg.fill('#f-q', 'tunnel'); pg.wait_for_timeout(160)
    t('« tunnel » ramene des resultats', visibles() > 0, str(visibles()))
    pg.fill('#f-q', 'zzzzzz'); pg.wait_for_timeout(160)
    t('une recherche sans resultat le dit', visibles() == 0 and
      pg.eval_on_selector('#vide', 'e=>e.getClientRects().length > 0'))
    pg.click('#raz'); pg.wait_for_timeout(120)

    # ---------------------------------------------------------------- 9
    print('\n9. Rendu : les deux bords, a trois largeurs')
    # scrollWidth - clientWidth ne voit QUE le bord droit. Un element qui sort
    # a gauche ne cree aucune barre de defilement, il est clippe en silence.
    JS_BORDS = """
    () => {
      const w = document.documentElement.clientWidth, out = [];
      document.querySelectorAll('body *').forEach(e => {
        if (e.hidden) return;
        const cs = getComputedStyle(e);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        const r = e.getBoundingClientRect();
        if (r.width < 1 && r.height < 1) return;
        if (r.left < -1) out.push(['gauche', Math.round(r.left), e.className || e.tagName]);
        else if (r.right > w + 1) out.push(['droite', Math.round(r.right - w), e.className || e.tagName]);
      });
      return out.slice(0, 4);
    }"""
    # Un debordement se voit. UN DESALIGNEMENT NE SE VOIT PAS : rien ne sort de
    # l'ecran, la barre du haut est juste decalee par rapport au reste de la
    # page. On mesure donc aussi la colonne, pas seulement les bords.
    JS_ALIGN = """
    () => {
      const b = s => { const e = document.querySelector(s);
        const r = e.getBoundingClientRect(); return [r.left, r.right]; };
      const logo = b('.logo'), titre = b('.hero h1'),
            nav = b('.tbar nav a:last-child');
      return {gauche: Math.abs(logo[0] - titre[0]),
              droite: Math.abs((document.documentElement.clientWidth - nav[1]) - titre[0])};
    }"""
    for w in (390, 768, 1280):
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.wait_for_timeout(180)
        bords = pg.evaluate(JS_BORDS)
        t('aucun debordement a %d px, ni a gauche ni a droite' % w,
          not bords, str(bords))
        al = pg.evaluate(JS_ALIGN)
        t('  la barre du haut est alignee sur la colonne a %d px' % w,
          al['gauche'] <= 1 and al['droite'] <= 1, str(al))
    pg.set_viewport_size({'width': 1280, 'height': 900})
    pg.wait_for_timeout(150)

    JS_CONTRASTE = """
    () => {
      const lum = c => { const f = v => { v/=255; return v<=0.03928 ? v/12.92
        : Math.pow((v+0.055)/1.055, 2.4); };
        return 0.2126*f(c[0]) + 0.7152*f(c[1]) + 0.0722*f(c[2]); };
      const parse = s => { const m = s.match(/[\\d.]+/g); return m ? m.slice(0,3).map(Number) : null; };
      const alpha = s => { const m = s.match(/[\\d.]+/g); return m && m.length>3 ? parseFloat(m[3]) : 1; };
      const bg = el => { let e = el;
        while (e) { const c = getComputedStyle(e).backgroundColor;
          if (c && alpha(c) > 0.85) return parse(c); e = e.parentElement; }
        return [255,255,255]; };
      const bas = [];
      document.querySelectorAll('body *').forEach(el => {
        if (el.hidden) return;
        const txt = [...el.childNodes].filter(n => n.nodeType === 3)
          .map(n => n.textContent.trim()).join(' ').trim();
        if (!txt) return;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return;
        const fg = parse(cs.color), b = bg(el);
        if (!fg || !b) return;
        const l1 = lum(fg), l2 = lum(b);
        const ratio = (Math.max(l1,l2)+0.05) / (Math.min(l1,l2)+0.05);
        const px = parseFloat(cs.fontSize);
        const gros = px >= 24 || (px >= 18.66 && parseInt(cs.fontWeight,10) >= 700);
        if (ratio < (gros ? 3 : 4.5)) bas.push([txt.slice(0,36), ratio.toFixed(2), px]);
      });
      return bas;
    }"""
    bas = pg.evaluate(JS_CONTRASTE)
    t('contraste : 0 element sous le seuil', not bas, str(bas[:3]))
    t('aucune erreur JS', not err, str(err[:3]))

    pg.evaluate('() => window.scrollTo(0, 0)'); pg.wait_for_timeout(250)
    pg.screenshot(path='ec_1_haut.png')
    pg.eval_on_selector('.plan', 'e=>e.scrollIntoView({block:"start"})')
    pg.wait_for_timeout(300)
    pg.screenshot(path='ec_2_plan.png')
    pg.select_option('#f-dom', 'signalisation'); pg.wait_for_timeout(200)
    pg.eval_on_selector('.filtres', 'e=>e.scrollIntoView({block:"start"})')
    pg.wait_for_timeout(300)
    pg.screenshot(path='ec_3_signalisation.png')
    pg.click('#raz'); pg.wait_for_timeout(150)
    pg.select_option('#f-us', 'tunnel'); pg.wait_for_timeout(200)
    pg.eval_on_selector('.filtres', 'e=>e.scrollIntoView({block:"start"})')
    pg.wait_for_timeout(300)
    pg.screenshot(path='ec_4_usage.png')
    pg.set_viewport_size({'width': 390, 'height': 820})
    pg.click('#raz'); pg.wait_for_timeout(350)
    pg.screenshot(path='ec_5_mobile.png')
    nav.close()

print('\n%d OK, %d ECHEC' % (ok, ko))
sys.exit(1 if ko else 0)
