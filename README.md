# Classer la folie ?

Présentation clinique et scientifique de l’ouvrage de Christophe Gauld, **Classer la folie ? Une philosophie de la psychiatrie pour le soin**, préface de Bruno Falissard, Hermann, 2026.

**Site : https://christophegauld.github.io/classer-la-folie/**

La structure suit le livre : introduction, huit chapitres répartis en deux parties, conclusion. Les textes présentent les classifications, les pluralismes, la psychiatrie de précision, la sémiologie, les systèmes dynamiques, les réseaux de symptômes, le codage prédictif et le raisonnement clinique en relation avec l’intelligence artificielle.

## Contenu éditorial

- Dix textes de présentation, environ 7 400 mots
- 56 définitions, accessibles dans le lexique et depuis les chapitres
- Citations littérales avec pagination
- Tableau des quatre formes d’humilité clinique reproduit d’après la page 83
- Références par chapitre et sélection bibliographique
- Liens vers la fiche des éditions Hermann et l’achat sur Amazon

Les textes hors citations sont des reformulations pédagogiques. Les exemples cliniques proviennent de l’ouvrage. Le site ne propose pas de graphiques ou de simulations ajoutés. Le manuscrit intégral et les notes de lecture de travail ne sont pas inclus.

## Fonctionnement

HTML statique, CSS et JavaScript, sans dépendance applicative. Les textes sont accessibles sans JavaScript. La recherche, les définitions contextuelles et le filtrage du lexique fonctionnent dans le navigateur. Une indication de lecture peut être enregistrée sur l’appareil et effacée depuis le sommaire.

Le site s’adapte aux petits écrans et possède une feuille de style d’impression. Les anciennes adresses `explorer.html` et `parcours.html` affichent le sommaire pour conserver l’accès depuis les liens déjà publiés.

## Modifier le site

1. Modifier `scripts/content.json` pour les chapitres et les définitions
2. Modifier `scripts/references.json` pour la sélection bibliographique
3. Modifier `scripts/build.py` pour les pages de présentation et la structure HTML
4. Modifier `site/assets/style.css` ou `site/assets/app.js` pour la présentation et les interactions
5. Lancer `python3 scripts/build.py`, puis `python3 scripts/validate.py`

`scripts/content.py` charge le contenu JSON. Les fichiers HTML dans `site/` sont générés ; ne pas les modifier directement.

## Vérification locale

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check site/assets/app.js
python3 -m http.server 8000 --directory site
```

Ouvrir `http://localhost:8000`. Le générateur utilise la bibliothèque standard de Python. Le validateur contrôle les liens, ancres, ressources, identifiants, titres et balises de définition. Toute modification d’une citation doit être contrôlée contre la page correspondante du livre.

## Publication

Le workflow `.github/workflows/pages.yml` reconstruit et vérifie le site avant de le publier sur GitHub Pages après chaque modification de `main`. Il peut aussi être lancé depuis l’onglet Actions.

Pour changer de dépôt ou de domaine, modifier `ORIGIN` et `REPO` dans `scripts/build.py`, puis reconstruire. La navigation relative fonctionne dans un sous-répertoire GitHub Pages.

## Confidentialité et droits

Aucun suivi d’audience, formulaire, compte utilisateur ou appel à une IA. L’état de lecture utilise uniquement `localStorage`. GitHub Pages assure l’hébergement.

Ouvrage et citations : Christophe Gauld, © Hermann Éditeurs, 2026. Préface : Bruno Falissard. La publication des fichiers du site ne leur attribue pas automatiquement une licence libre. La typographie utilise les polices système Arial/Helvetica.
