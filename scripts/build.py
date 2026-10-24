#!/usr/bin/env python3
"""Génère l'édition web statique à partir des contenus vérifiés."""
from pathlib import Path
import html
import json
import math
import re
import unicodedata
from content import LESSONS, GLOSSARY

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
ORIGIN = 'https://christophegauld.github.io/classer-la-folie'
BOOK = 'https://www.editions-hermann.fr/livre/classer-la-folie-christophe-gauld'
BUY = 'https://www.amazon.fr/Classer-folie-philosophie-psychiatrie-pour/dp/B0GZMRQKKN'
REPO = 'https://github.com/ChristopheGauld/classer-la-folie'
e = html.escape
PARTS = [('fondements', 'I', 'Classer, penser, promettre, soigner'),
         ('ouvertures', 'II', 'Pour une science clinique de la complexité')]
AUTO = {
    'temps': {'attracteur': 'attracteur', 'multistabilité': 'multistabilite', 'hystérésis': 'hysteresis', 'données longitudinales': 'longitudinal'},
    'reseaux': {'variable latente': 'variable-latente', 'nomothétique': 'nomothetique', 'idiographique': 'idiographique', 'PECAN': 'pecan', 'centralité': 'centralite', 'anhédonie': 'anhedonie'},
    'prediction': {'codage prédictif': 'codage-predictif', 'bayésiennes': 'bayesien', 'erreur de prédiction': 'erreur-prediction', 'inférence active': 'inference-active', 'intéroception': 'interoception'},
    'raisonnement': {'heuristiques': 'heuristique', 'granularité': 'granularite', 'jumeau numérique': 'jumeau'},
}

def text(value):
    value = e(value)
    return re.sub(r'\[\[([^]|]+)\|([^]]+)\]\]', lambda m: f'<a class="term" data-term="{m[1]}" href="lexique.html#{m[1]}">{m[2]}</a>', value)

def slug(value):
    return re.sub('[^a-z0-9]+', '-', unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()).strip('-')

def quote(value, page):
    return f'<blockquote class="quote"><p>« {e(value)} »</p><cite>Christophe Gauld, <a href="livre.html#citations">Classer la folie ?</a>, p. {page}</cite></blockquote>'

def header(current):
    items = [('Sommaire', 'sommaire.html'), ('Lexique', 'lexique.html'), ('Références', 'sources.html'), ('L’ouvrage', 'livre.html')]
    nav = ''.join(f'<a href="{href}"'+(' aria-current="page"' if current == name else '')+f'>{name}</a>' for name, href in items)
    return f'''<a class="skip" href="#contenu">Aller au contenu</a>
    <header class="site-header"><div class="wrap header-inner">
      <a class="brand" href="index.html">Classer la folie ?<small>Christophe Gauld</small></a>
      <nav class="nav" id="main-nav" aria-label="Navigation principale">{nav}
        <button class="search-trigger" aria-label="Rechercher dans le site"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="10" cy="10" r="6"/><path d="m14.5 14.5 6 6"/></svg><span>Rechercher</span></button>
      </nav><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Ouvrir le menu">Menu</button>
    </div></header>'''

def footer():
    return f'''<footer class="footer"><div class="wrap footer-inner"><div><strong>Classer la folie ?</strong><br>Christophe Gauld · Hermann, 2026</div><div class="footer-links"><a href="livre.html#methode">À propos de cette édition web</a><a href="{BOOK}">Éditions Hermann</a><a href="{REPO}">Code source sur GitHub</a></div></div></footer>
    <dialog class="dialog" id="search-dialog" aria-labelledby="search-title"><button class="dialog-close" aria-label="Fermer la recherche">×</button><h2 id="search-title">Rechercher dans les textes</h2><label class="screenreader" for="site-search">Rechercher un concept ou un chapitre</label><input class="search-field" id="site-search" type="search" placeholder="Symptôme, classification, réseaux…" autocomplete="off"><div id="search-status" class="small muted" aria-live="polite"></div><div class="search-results" id="search-results"></div></dialog>
    <dialog class="dialog term-dialog" id="term-dialog" aria-labelledby="term-title"><button class="dialog-close" aria-label="Fermer la définition">×</button><span class="eyebrow">Définition</span><h2 id="term-title"></h2><p id="term-definition"></p><a id="term-link" href="lexique.html">Voir la définition et ses références</a></dialog>'''

def page(filename, title, desc, body, current='', article=False):
    markup = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#ffffff">
<title>{e(title)} · Classer la folie ?</title><meta name="description" content="{e(desc,quote=True)}"><link rel="canonical" href="{ORIGIN}/{filename}">
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(desc,quote=True)}"><meta property="og:url" content="{ORIGIN}/{filename}"><meta property="og:locale" content="fr_FR"><meta name="author" content="Christophe Gauld">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/data.js" defer></script><script src="assets/app.js" defer></script></head>
<body>{header(current)}{'<div class="progress-strip" aria-hidden="true"><span id="reading-progress"></span></div>' if article else ''}{body}{footer()}</body></html>'''
    (SITE / filename).write_text(markup, encoding='utf-8')

def chapter_link(lesson, compact=False):
    number = lesson['number']
    label = lesson['chapter'] if not number else number
    if compact:
        return f'<a href="{lesson["slug"]}.html"><span>{label}</span>{e(lesson["short"])}</a>'
    return f'''<a class="chapter-row" data-lesson-row="{lesson['slug']}" href="{lesson['slug']}.html">
    <span class="chapter-number">{label if number else '—'}</span><div><span class="chapter-field">{e(lesson['kicker'])}</span><h3>{e(lesson['title'])}</h3><p>{e(lesson['summary'])}</p></div><span class="chapter-pages">p. {lesson['pages']}<small class="read-mark" hidden>Lu</small></span></a>'''

def contents():
    intro = LESSONS[0]
    sections = f'<div class="contents-prelude"><a href="introduction.html">Introduction — {e(intro["title"])}</a><span>p. 13–17</span></div>'
    for group, number, title in PARTS:
        sections += f'<section class="contents-part" id="partie-{number.lower()}"><div class="part-heading"><span>Partie {number}</span><h2>{title}</h2></div><div class="chapter-list">'+''.join(chapter_link(l) for l in LESSONS if l['group']==group)+'</div></section>'
    sections += '<div class="contents-prelude conclusion-link"><a href="mondes.html">Conclusion — La psychiatrie environnementale</a><span>p. 131–133</span></div>'
    return sections

summaries = {
    'classer': 'Catégories, stadification, HiTOP et RDoC : objectifs, usages et limites des classifications.',
    'pluralisme': 'Pluralismes non intégratifs et intégratifs ; articulation des explications et expérience vécue.',
    'promesses': 'Psychiatrie personnalisée et de précision : attentes scientifiques, résultats et conditions d’usage.',
    'ecouter': 'Le symptôme comme concept épais, les formes d’humilité clinique et la place de l’incertitude.',
    'temps': 'Évolution des symptômes, attracteurs, multistabilité, transitions et données longitudinales.',
    'reseaux': 'Interactions entre symptômes, réseaux de groupe et individuels, associations et causalité.',
    'prediction': 'Croyances, erreurs de prédiction, précision et inférence active : hypothèses et limites.',
    'raisonnement': 'Recueil des données, apprentissage, heuristiques et comparaison des raisonnements clinique et informatique.',
    'introduction': 'L’articulation entre manifestations cliniques, catégories diagnostiques et contexte social.',
    'mondes': 'Santé mentale publique, psychiatrie transculturelle, exposomique, écologie et One Health.',
}
for lesson in LESSONS:
    lesson['summary'] = summaries[lesson['slug']]

home = f'''<main id="contenu" class="wrap">
<section class="book-heading"><div><p class="eyebrow">Philosophie de la psychiatrie</p><h1>Classer la folie ?</h1><p class="subtitle">Une philosophie de la psychiatrie pour le soin</p><p class="byline">Christophe Gauld</p><p class="book-details">Préface de Bruno Falissard · Hermann, 2026</p></div>
<aside class="edition-note"><span class="eyebrow">L’ouvrage</span><p>154 pages<br>ISBN 9791037048516</p><a href="{BOOK}">Éditions Hermann</a><a href="{BUY}">Acheter sur Amazon</a></aside></section>
<section class="introduction-block"><h2>Des mots de la clinique aux questions philosophiques</h2><div><p>Qu’est-ce qu’un symptôme ? Pourquoi plusieurs classifications peuvent-elles coexister ? Comment distinguer une explication, une preuve et une promesse ? La philosophie de la psychiatrie aide à formuler ces questions, à examiner les réponses et à comprendre leurs conséquences pour le soin.</p><p>Cette présentation reprend les deux parties de l’ouvrage : les fondements conceptuels de la psychiatrie, puis les modèles de la complexité clinique. Elle s’adresse aux internes, aux professionnels de santé et aux journalistes. Les notions sont définies dans les textes et dans le lexique ; les citations renvoient aux pages du livre.</p></div></section>
<section class="contents-section" aria-labelledby="contents-heading"><div class="section-label"><h2 id="contents-heading">Sommaire</h2><span>Introduction · 8 chapitres · Conclusion</span></div>{contents()}</section>
<div class="editorial-note"><p>Les textes de cette édition web sont des reformulations à partir de l’ouvrage. Les citations et le tableau reproduit sont signalés et paginés.</p><a href="livre.html#methode">Présentation éditoriale et sources</a></div></main>'''
page('index.html', 'Philosophie de la psychiatrie pour le soin', 'Classer la folie ? de Christophe Gauld : classifications, pluralismes, sémiologie et modèles de la complexité clinique.', home)

body = f'''<main id="contenu" class="wrap"><header class="page-heading"><p class="eyebrow">Classer la folie ?</p><h1>Sommaire</h1><p class="lead">Les chapitres sont présentés dans l’ordre de l’ouvrage. La pagination renvoie au livre publié chez Hermann.</p></header>{contents()}<div class="reading-tools"><p id="reading-counter">L’état de lecture est enregistré sur cet appareil.</p><button class="reset-progress" id="reset-progress">Effacer les indications de lecture</button></div></main>'''
page('sommaire.html', 'Sommaire', 'Les deux parties et les huit chapitres de Classer la folie ?, avec leur pagination.', body, 'Sommaire')
# Keep previously published addresses usable, without retaining the old presentation.
for filename in ('explorer.html', 'parcours.html'):
    page(filename, 'Sommaire', 'Sommaire des chapitres de Classer la folie ?', body, 'Sommaire')

def sidebar(current):
    links = '<a class="sidebar-home" href="sommaire.html">Sommaire de l’ouvrage</a>'
    for group, label in [('introduction',''),('fondements','I. Classer, penser, promettre, soigner'),('ouvertures','II. Pour une science clinique de la complexité'),('conclusion','')]:
        if label: links += f'<div class="sidebar-part">{label}</div>'
        for item in LESSONS:
            if item['group'] != group: continue
            num = f'<span class="sidebar-number">{item["number"]}</span>' if item['number'] else ''
            short = item['short'] if item['number'] else item['chapter']
            links += f'<a class="sidebar-chapter" href="{item["slug"]}.html"'+(' aria-current="page"' if current==item['slug'] else '')+f'>{num}{e(short)}</a>'
    return f'<aside class="article-aside"><nav aria-label="Chapitres de l’ouvrage">{links}</nav></aside>'

search = []
for index, lesson in enumerate(LESSONS):
    sections, toc, raw = [], [], []
    auto = dict(AUTO.get(lesson['slug'], {}))
    for section in lesson['sections']:
        if 'title' in section:
            sid = slug(section['title'])
            toc.append((sid, section['title']))
            paras = []
            for paragraph in section['paragraphs']:
                raw.append(paragraph)
                # Explicit glossary links take priority over automatic first-occurrence links.
                for word, term_id in list(auto.items()):
                    pat = re.compile(r'(?<!\w)' + re.escape(word) + r'(?!\w)', re.I)
                    parts = re.split(r'(\[\[[^]]+\]\])', paragraph)
                    found = False
                    for j in range(0,len(parts),2):
                        if pat.search(parts[j]):
                            parts[j] = pat.sub(lambda m:'[['+term_id+'|'+m[0]+']]', parts[j], count=1)
                            found = True
                            break
                    if found: paragraph=''.join(parts); del auto[word]
                paras.append('<p>' + text(paragraph) + '</p>')
            sections.append(f'<section class="article-section" id="{sid}"><h2>{e(section["title"])}</h2>'+''.join(paras)+'</section>')
        elif 'quote' in section:
            sections.append(quote(section['quote'],section['page']))
        elif 'note' in section:
            sections.append(f'<aside class="note"><h3>{e(section["note"])}</h3><p>{text(section["text"])}</p></aside>')
        elif 'table' in section:
            table = section['table']
            head = ''.join(f'<th scope="col">{e(c)}</th>' for c in table['columns'])
            rows = ''.join('<tr><th scope="row">'+e(row[0])+'</th>'+''.join('<td>'+e(c)+'</td>' for c in row[1:])+'</tr>' for row in table['rows'])
            sections.append(f'<figure class="book-table"><table><caption>{e(table["caption"])}</caption><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table><figcaption>Reproduction du tableau de l’ouvrage, p. {table["page"]}</figcaption></figure>')
    lesson['words'] = len(re.findall(r'\w+', ' '.join(raw)))
    lesson['minutes'] = math.ceil(lesson['words'] / 190)
    toc_html = ''.join(f'<li><a href="#{sid}">{e(title)}</a></li>' for sid, title in toc)
    previous = LESSONS[index-1] if index else None
    following = LESSONS[index+1] if index+1 < len(LESSONS) else None
    previous_link = f'<a href="{previous["slug"]}.html"><span>Précédent</span>{e(previous["short"])}</a>' if previous else '<a href="sommaire.html"><span>Sommaire</span>Les chapitres de l’ouvrage</a>'
    next_link = f'<a href="{following["slug"]}.html"><span>Suivant</span>{e(following["short"])}</a>' if following else '<a href="sources.html"><span>Références</span>Sources et bibliographie</a>'
    part = 'Partie I' if lesson['group']=='fondements' else 'Partie II' if lesson['group']=='ouvertures' else 'L’ouvrage'
    context = lesson['kicker'] if lesson['number'] else ''
    body = f'''<main id="contenu" data-article="{lesson['slug']}" class="wrap article-layout">{sidebar(lesson['slug'])}<article class="reading">
    <header class="article-heading"><div class="breadcrumb"><a href="sommaire.html">Sommaire</a><span aria-hidden="true">/</span>{part}</div><p class="eyebrow">{e(lesson['chapter'])}{' · '+e(context) if context else ''}</p><h1>{e(lesson['title'])}</h1><div class="article-meta"><span>Pages {lesson['pages']}</span><span>{lesson['minutes']} min de lecture</span></div><p class="article-intro">{e(lesson['intro'])}</p></header>
    <details class="chapter-toc" open><summary>Contenu de cette section</summary><ol>{toc_html}</ol></details>
    {''.join(sections)}<div class="source-note"><strong>Référence dans l’ouvrage</strong><p>Christophe Gauld, <i>Classer la folie ? Une philosophie de la psychiatrie pour le soin</i>, Hermann, 2026. {e(lesson['chapter'])}, p. {lesson['pages']}. Texte de présentation ; les citations sont indiquées entre guillemets et paginées.</p><a href="sources.html#{lesson['slug']}">Références et pagination</a></div>
    <div class="article-tools"><button class="complete-button" data-complete="{lesson['slug']}" aria-pressed="false">Marquer cette section comme lue</button><a href="#contenu">Haut de page ↑</a></div><nav class="next-prev" aria-label="Sections précédente et suivante">{previous_link}{next_link}</nav></article></main>'''
    page(lesson['slug']+'.html', lesson['title'], lesson['intro'], body, 'Sommaire', True)
    search.append(dict(title=lesson['title'],kind=lesson['chapter'],url=lesson['slug']+'.html',text=lesson['intro']+' '+' '.join(raw),excerpt=lesson['summary']))

GLOSSARY.sort(key=lambda g: unicodedata.normalize('NFKD',g['term']).casefold())
definitions=''.join(f'<section class="definition" id="{g["id"]}" data-definition="{e(g["term"],quote=True)}"><h2>{e(g["term"])}</h2><p>{e(g["definition"])}</p><div class="definition-reference"><a href="{g["lesson"]}.html">Voir le chapitre</a><span>Ouvrage, p. {g["pages"]}</span></div></section>' for g in GLOSSARY)
body=f'''<main id="contenu" class="wrap"><header class="page-heading"><p class="eyebrow">Définitions</p><h1>Lexique</h1><p class="lead">{len(GLOSSARY)} notions de philosophie de la psychiatrie, de sémiologie et de modélisation. Chaque définition renvoie au chapitre concerné et aux pages de l’ouvrage.</p></header><div class="glossary-toolbar"><label for="glossary-search">Rechercher une notion</label><input class="search-field" type="search" id="glossary-search" placeholder="Ex. : nosologie, attracteur, pluralisme"><span class="small muted" id="glossary-count" aria-live="polite">{len(GLOSSARY)} notions</span></div><div class="glossary-grid">{definitions}</div><p id="glossary-empty" class="empty-state" hidden>Aucune définition ne correspond à cette recherche.</p></main>'''
page('lexique.html','Lexique','Définitions des notions de philosophie de la psychiatrie, de complexité et de raisonnement clinique.',body,'Lexique')
for item in GLOSSARY:
    search.append(dict(title=item['term'],kind='Définition',url='lexique.html#'+item['id'],text=item['term']+' '+item['definition'],excerpt=item['definition']))

body=f'''<main id="contenu" class="wrap document-page"><header class="page-heading"><p class="eyebrow">Christophe Gauld</p><h1>L’ouvrage</h1><p class="lead">Classer la folie ?<br>Une philosophie de la psychiatrie pour le soin</p></header><div class="reading">
<section class="bibliographic-record"><h2>Informations bibliographiques</h2><dl><div><dt>Auteur</dt><dd>Christophe Gauld</dd></div><div><dt>Préface</dt><dd>Bruno Falissard</dd></div><div><dt>Éditeur</dt><dd>Hermann</dd></div><div><dt>Parution</dt><dd>3 juin 2026</dd></div><div><dt>Pagination</dt><dd>154 pages</dd></div><div><dt>ISBN</dt><dd>9791037048516</dd></div></dl><div class="book-links"><a href="{BOOK}">Présentation chez Hermann ↗</a><a href="{BUY}">Acheter sur Amazon ↗</a></div></section>
<section class="article-section"><h2>Objet du livre</h2><p>L’ouvrage examine les classifications psychiatriques, la pluralité des modèles explicatifs, les promesses de la médecine de précision et le rôle de la sémiologie. Sa seconde partie traite des systèmes dynamiques, des réseaux de symptômes, du codage prédictif et de l’intelligence artificielle dans leurs rapports à la clinique.</p><p>La conclusion situe ces questions dans les dimensions sociales, culturelles et environnementales de la psychiatrie. <a href="sommaire.html">Consulter le sommaire</a>.</p></section>
<section class="article-section" id="methode"><h2>Présentation éditoriale</h2><p>Cette édition web présente les concepts du livre aux internes, aux professionnels de santé et aux journalistes qui ne disposent pas nécessairement d’une formation en philosophie ou en modélisation. Elle suit l’ordre des deux parties et des huit chapitres, précédés de l’introduction et suivis de la conclusion.</p><p>Les textes sont des reformulations pédagogiques à partir de l’ouvrage. Ils ne constituent pas une reproduction intégrale. Les exemples cliniques mentionnés proviennent du livre ; les pages d’appui permettent de les replacer dans leur argumentation. Les définitions du lexique explicitent les termes employés.</p><p>Le tableau des quatre formes d’humilité clinique est reproduit d’après la page 83. Les textes distinguent les propositions théoriques, les applications envisagées et les limites discutées dans l’ouvrage.</p></section>
<section class="article-section" id="citations"><h2>Citations et pagination</h2><p>Les citations sont placées entre guillemets, attribuées à Christophe Gauld et accompagnées de leur page. Elles ont été vérifiées dans le texte fourni par l’auteur. Les césures de mise en page ont été réunies sans changer les mots des extraits. La pagination est celle de l’ouvrage.</p><p>Les textes hors guillemets et les définitions sont des reformulations. Les références de chaque chapitre et une sélection de la bibliographie figurent sur la <a href="sources.html">page Références</a>.</p></section>
<section class="article-section"><h2>L’auteur</h2><p>Christophe Gauld est pédopsychiatre. Sa présentation et les informations éditoriales de l’ouvrage sont disponibles sur le <a href="{BOOK}">site des éditions Hermann</a>.</p></section>
<section class="article-section" id="confidentialite"><h2>Fonctionnement du site</h2><p>La recherche et les définitions fonctionnent dans le navigateur. L’indication des sections lues est enregistrée sur cet appareil ; elle peut être effacée depuis le <a href="sommaire.html">sommaire</a>. Le site ne comporte ni compte utilisateur, ni formulaire, ni outil de suivi d’audience.</p><p>Le site est hébergé sur GitHub Pages. Ses fichiers sont disponibles dans le <a href="{REPO}">dépôt GitHub du projet</a>. Les requêtes d’accès relèvent du fonctionnement de l’hébergeur.</p></section>
<section class="article-section"><h2>Crédits</h2><p>Ouvrage et citations : Christophe Gauld, © Hermann Éditeurs, 2026. Préface : Bruno Falissard. La publication des fichiers du site ne leur attribue pas automatiquement une licence de réutilisation.</p></section></div></main>'''
page('livre.html','L’ouvrage','Informations bibliographiques, liens Hermann et Amazon, méthode éditoriale et citations.',body,'L’ouvrage')

refs=json.loads((ROOT/'scripts/references.json').read_text())
ref_html=''.join(f'<li class="reference-item"><p class="eyebrow">{e(title)}</p><h3>{e(ref)}</h3><p>{e(desc)}</p>'+(f'<a href="{url}">Consulter la référence ↗</a>' if url else '<small>Référence de la bibliographie de l’ouvrage</small>')+'</li>' for title,ref,desc,url in refs)
mapping=''.join(f'<tr id="{l["slug"]}"><th scope="row"><a href="{l["slug"]}.html">{e(l["chapter"])}</a></th><td>{e(l["title"])}</td><td>{l["pages"]}</td></tr>' for l in LESSONS)
body=f'''<main id="contenu" class="wrap document-page"><header class="page-heading"><p class="eyebrow">Sources et bibliographie</p><h1>Références</h1><p class="lead">Les textes du site s’appuient sur l’ouvrage. La table indique les pages de chaque chapitre ; la bibliographie donne quelques références pour leur étude.</p></header><div class="reading"><h2>Source principale</h2><p>Christophe Gauld, <i>Classer la folie ? Une philosophie de la psychiatrie pour le soin</i>, préface de Bruno Falissard, Hermann, 2026, 154 pages. ISBN 9791037048516. <a href="{BOOK}">Fiche de l’éditeur</a>.</p><p>Les citations sont littérales et paginées. Les autres textes sont des reformulations. Les définitions du lexique renvoient également aux pages de l’ouvrage.</p><div class="table-scroll"><table class="source-table"><caption>Correspondance avec les chapitres de l’ouvrage</caption><thead><tr><th scope="col">Section</th><th scope="col">Objet</th><th scope="col">Pages</th></tr></thead><tbody>{mapping}</tbody></table></div><section class="article-section"><h2>Sélection bibliographique</h2><p>Les références sans lien sont données d’après la bibliographie de l’ouvrage. La présentation institutionnelle de RDoC complète les références du chapitre I.</p><ol class="reference-list">{ref_html}</ol></section></div></main>'''
page('sources.html','Références','Correspondance entre les chapitres et leurs pages, citations et sélection bibliographique.',body,'Références')

(SITE/'assets/data.js').write_text('window.SITE_DATA='+json.dumps({'lessons':[{k:l[k] for k in ['slug','title','short','minutes']} for l in LESSONS],'glossary':GLOSSARY,'search':search},ensure_ascii=False)+';\n')
(SITE/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="4" fill="#243e58"/><text x="32" y="41" text-anchor="middle" font-family="Arial,sans-serif" font-weight="bold" font-size="27" fill="white">CF</text></svg>')
(SITE/'.nojekyll').write_text('')
urls=[p.name for p in SITE.glob('*.html') if p.name not in ('explorer.html','parcours.html')]
(SITE/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}/{u}</loc></url>' for u in sorted(urls))+'</urlset>')
(SITE/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
print(f'{len(urls)} pages principales ; {len(GLOSSARY)} définitions ; {sum(l["words"] for l in LESSONS)} mots dans les articles')
