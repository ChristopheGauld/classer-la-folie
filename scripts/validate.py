#!/usr/bin/env python3
"""Vérifications du site statique sans dépendances tierces."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
import sys
ROOT=Path(__file__).resolve().parents[1]/'site'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.links=[];self.headings=0;self.lang=None;self.title=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.headings+=1
  if tag=='html':self.lang=a.get('lang')
  if tag=='title':self.title=True
  for attr in ('href','src'):
   if attr in a:self.links.append(a[attr])
pages={}
errors=[]
for path in ROOT.glob('*.html'):
 p=Page();p.feed(path.read_text());pages[path.name]=p
 if p.headings!=1:errors.append(f'{path.name}: {p.headings} H1')
 if p.lang!='fr':errors.append(f'{path.name}: langue incorrecte')
 if not p.title:errors.append(f'{path.name}: titre manquant')
 duplicates=[id for id,n in Counter(p.ids).items() if n>1]
 if duplicates:errors.append(f'{path.name}: IDs dupliqués {duplicates}')
 if '[[' in path.read_text():errors.append(f'{path.name}: balisage de lexique non résolu')
for name,p in pages.items():
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or name
  if not (ROOT/target).is_file():errors.append(f'{name}: fichier manquant {href}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{name}: ancre manquante {href}')
assert not errors,'\n'.join(errors)
print(f'OK : {len(pages)} pages, titres, langue, identifiants, ressources, liens et ancres internes.')
