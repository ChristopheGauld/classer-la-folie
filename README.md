# Classer la folie ?

Site de découverte de la philosophie de la psychiatrie à partir de l’ouvrage de Christophe Gauld, **Classer la folie ? Une philosophie de la psychiatrie pour le soin**, préface de Bruno Falissard, Hermann, 2026.

**Site : https://christophegauld.github.io/classer-la-folie/**

Le parcours commence par l’expérience vécue et le symptôme, puis explore les classifications, le pluralisme et les promesses de précision. La deuxième partie développe les systèmes dynamiques, les réseaux, le codage prédictif et le raisonnement clinique en dialogue avec l’IA. La dernière étape reprend l’ouverture sociale, culturelle et environnementale de la conclusion.

## Contenu

- Neuf articles pédagogiques, environ 7 500 mots
- 56 définitions, consultables dans le lexique et depuis les textes
- Quatre parcours : découverte, internes, professionnels de santé, journalistes
- Citations du livre avec pages, et correspondance des chapitres sur la page Sources
- Comparaison de quatre approches et quatre explorations pédagogiques
- Recherche locale dans les textes et définitions, progression enregistrée sur l’appareil
- Pages lisibles sur mobile et imprimables

Les textes sont des adaptations pédagogiques. Les extraits littéraux sont distincts et paginés. Les modèles interactifs sont fictifs ou conceptuels, avec leurs hypothèses explicites. Le manuscrit intégral et les notes de lecture de travail ne sont pas inclus.

## Modifier les textes

1. Modifier `scripts/content.py` pour les articles et le lexique
2. Modifier `scripts/build.py` pour l’accueil, les parcours, le livre, les sources et la structure des pages
3. Modifier `scripts/labs.py` pour le texte et la structure des explorations
4. Lancer `python3 scripts/build.py`, puis `python3 scripts/validate.py`

Le dossier `site/` contient le site généré. Éviter de modifier directement ses fichiers HTML : ils seront régénérés. Les fichiers CSS et JavaScript dans `site/assets/` sont les sources et peuvent être modifiés directement.

## Voir le site localement

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m http.server 8000 --directory site
```

Ouvrir `http://localhost:8000`. Le générateur utilise uniquement la bibliothèque standard de Python, sans installation de paquets. Le site fonctionne avec des fichiers HTML, CSS et JavaScript, sans serveur applicatif ni base de données.

## Publication

GitHub Pages est configuré pour GitHub Actions. Le workflow `.github/workflows/pages.yml` régénère le site, vérifie ses liens internes et publie le dossier `site/` après chaque modification de la branche `main`. Il peut également être lancé manuellement depuis l’onglet Actions.

Pour changer de dépôt ou de domaine, modifier `ORIGIN` et `REPO` dans `scripts/build.py`, puis reconstruire. Les liens de navigation sont relatifs et compatibles avec une publication dans un sous-répertoire GitHub Pages.

## Vérifications

- Citations contrôlées contre le texte fourni, avec normalisation des seules césures et espaces de composition
- Vérification automatique des liens, ancres, ressources, identifiants et titres
- Recherche, définitions, progression et explorations testées dans le navigateur
- Absence de débordement horizontal vérifiée à 320 pixels sur les quinze pages
- Mise à jour bayésienne et deux bassins d’attraction vérifiés avec leurs hypothèses

Les contrôles de structure s’exécutent avec `python3 scripts/validate.py`. Les citations restent à vérifier éditorialement en cas de modification de leur texte ou de leur pagination.

## Confidentialité et droits

Aucun suivi d’audience, formulaire, compte utilisateur ou appel à une IA. La recherche et les explorations fonctionnent dans le navigateur. La progression utilise seulement `localStorage` et peut être effacée depuis la page Explorer. GitHub Pages assure l’hébergement.

Les citations renvoient à l’ouvrage © Hermann Éditeurs, 2026. La publication des sources ne leur attribue pas automatiquement une licence libre. La police Literata est distribuée sous licence SIL Open Font License, incluse dans `site/assets/FONT-LICENSE.txt`. Les schémas et la composition typographique du livre ont été créés pour ce site ; cette dernière n’est pas la couverture éditoriale.
