---
marp: true
theme: default
class: invert
---

# Git

**Outil de collaboration**

Louvain-li-Nux

![bg right height:50%](img/git-icon.svg)

---

## Cette présentation est

- Sous license libre CC-BY 4.0
- Disponible en ligne : <https://wiki.louvainlinux.org/fr/training/git>
- N'hésitez pas à la suivre pendant la presentation !

---

### Git, c'est quoi ?

- Un système de gestion de versions distribué
- VCS (Version Control System), en Anglais

---

## Mise en place de l'environnement

---

Ouvrir votre émulateur de terminal, et ensuite :

### Linux

```sh
$ sudo apt update && sudo apt install git
```

### Windows

- `wsl --install`
- Ouvrir une session Linux.
- Cf. Linux.

### Mac

```sh
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install git
```

---

## La ligne de commande (CLI)

Des implémentations GUI existent, *mais* :

- Moins flexibles.
- Opaques.
- Souvent fermées.
- C'est juste plus facile de tous vous apprendre la même chose.

Donc $\rightarrow$ petit détour vers les bases du CLI !

---

## La Commande

```sh
$ echo "Hello world"  # <-- commande + argument
Hello world           # <-- sortie
```

![bg right width:100%](img/commande.png)

---

## Le Chemin (aka Path)

Soyez attentif ici, c'est là où les gens ont généralement le plus de mal !

TODO examples in a file manager side-by-side

---

## Le Chemin (aka Path)

Une liste de dossiers empruntés pour arriver à un dossier/fichier, séparés par des `/`. E.g. :

- Un fichier qui s'appelle "tux" : `tux`
- Ce dossier "super" : `super`
- Un fichier qui s'appelle "tux2" dans ce dossier "super" : `super/tux2`

Ce sont des chemins *relatifs* !

---

### `pwd`

**Q**: Relatifs à quoi ? **R**: Relatifs à nous.
**Q**: Comment savoir où nous sommes ? **R**:

```sh
$ pwd # "print working directory" ou "écrire le dossier de travail"
/home/beastie
```

Le "dossier de travail" ou "working directory" est le dossier dans lequel nous sommes actuellement.
Ceci est un chemin *absolu* !

---

### `pwd`

On peut trouver un chemin absolu d'un chemin relatif en ajoutant notre dossier de travail avant :

- Le fichier `tux` devient `/home/beastie/tux`.
- Le dossier `super` devient `/home/beastie/super`.
- Le fichier `super/tux2` devient `/home/beastie/super/tux2`.

---

### `ls`

On peut afficher tous les fichiers/dossiers dans notre dossier de travail :

```sh
$ ls
tux	super/
```

Ou dans un autre dossier :

```sh
$ ls super
tux2
```

---

### `cd`

On peut changer notre dossier de travail :

```sh
$ cd super
```

Et puis encore :

```sh
$ ls
tux2
```

---

### `cd`

On peut retourner un dossier en arrière :

```sh
$ pwd
/home/beastie/super
$ cd ..
$ pwd
/home/beastie
```

---

### Recap

- `pwd` : Afficher le dossier de travail.
- `ls` : Afficher le contenu d'un dossier.
- `cd` : Changer le dossier de travail.

---

## Concepts de base de git

---

### Le repo ("dépôt" en 🇫🇷)

- Endroit où notre code est stocké, ainsi que l'historique des versions et toutes les données relatives à `git`.
- Généralement, un projet == un repo.

---

### Le remote

- Emplacement distant qui sert de "source de vérité" à notre repo.
- Souvent sur un serveur externe (GitHub, Gitlab, etc.).
- Récupérer un repo c'est "clôner" un repo.

TODO drawing showing remotes

---

### Le remote

C'est aussi possible d'avoir plusieurs remotes à la fois !

TODO drawing showing multiple users with muliple remotes

On verra l'utilité de celà un peu plus tard...

---

## Mise en place de l'environnement pour la suite de cet atelier

Clôner votre repo :

```sh
$ git clone https://git.louvainlinux.org/repo69
```

Un dossier a été crée, `cd` dedans :

```sh
$ cd repo69
```

---

### Configuration de git

```sh
git config --global user.name “Tux”
git config --global user.email “info@louvainlinux.org”
git config --global pull.rebase false
```

---

## Le stage (== scène)

Espace de travail pour des changements.

TODO Drawing of an empty stage, with a bunch of changes around it.

---

### Diff (unstaged)

On peut voir les changements qui ne sont pas encore sur le stage ("unstaged") avec `git diff` :

TODO show command + drawing side-by-side

Dans ce cas ci, tous les changements sont unstaged.

---

### Ajout de changements

On peut faire monter des changements sur le stage avec `git add chemin/vers/mon/fichier` :

TODO: Drawing of stage with added changes

---

### Diff (staged)

On peut voir les changements sont sur le stage ("staged") avec `git diff --staged` :

TODO show command + drawing side-by-side

---

### Nettoyage du stage

On peut tout enlever du stage avec `git reset` :

TODO: show command (`git diff --staged`) + drawing of empty stage side-by-side

---

### Effaçage des changements

On peut tout enlever du stage et en dehors du stage avec `git restore chemin/vers/mon/fichier` :

TODO: show command (`git diff --staged`/`git diff`) + drawing of empty everything side-by-side

---

## Mais que fait-on avec le stage ?

---

### Le commit

- Un peu comme une photo de ce qu'il y a sur le stage avec un petit message.
- (Normalement) immuable.
- Représente une unité de changement.
- Exemple de commit avec comme message "ui: Add random button" :

```sh
$ git commit -m "ui: Add random button"
```

---

### Le log

- Au final, notre code est une superposition de ces changements (commits) en ordre chronologique.
- Un peu comme un album photo.
- On peut voir toutes les photos de cet "album photo" avec `git log`.

---

### Le push

Le fait de mettre à jour le remote avec nos changements :

```sh
$ git push
```

---

### Le pull

Le fait de nous mettre à jour par rapport au changements sur le remote :

```sh
$ git push
```

---

### Recap

- Stage : Endroit où on prépare les changements à être ajoutés à un commit.
- Commit : L'acte de prendre une "photo" des changements sur le stage et mettre un nom dessus.
- Log : La liste de tous les commits.

---

## Un exemple concret !

---

### Recap

- Stage : Endroit où on prépare les changements à être ajoutés à un commit.
- Commit : L'acte de prendre une "photo" des changements sur le stage et mettre un nom dessus.
- Log : La liste de tous les commits.

---

## Exercices git

Avant de commencer, cloner la repo avec votre numéro :

```sh
$ git clone https://git.louvainlinux.org/repo69
```

Et entrez dedans :

```sh
$ cd repo69
$ pwd
/home/tux/repo69
```

---

### Exercice 1 : Les bases

- Modifier le fichier `README.md`.
- "Stage" les changements : `git add -p .`.
- "Commit" les changements : `git commit -m "descriptif de mes changements"`.
- "Push" les changements : `git push`.

---

## Exercices sur la collaboration

### Merges, conflits, résolutions

---

### Exercice 2 : Changements remote

Passer au prochain exercice en faisant un commit avec "exercice 2" dans le titre :

```sh
$ git commit --allow-empty -m "exercice 2"
$ git push
```

---

### Exercice 2 : Changements remote

*Contexte* : quelqu'un a push des changements après toi.
Essayez de faire un nouveau commit.

---

### Exercice 2 : Changements remote

```sh
$ git push
[main 7c64a36] test
To https://git.louvainlinux.org/repo-69
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://git.louvainlinux.org/repo-69'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

---

### Exercice 2 : Changements remote

- "Pull" les changements du remote : `git pull`.
- Vous verrez un nouveau fichier en faisant `ls`.
- Faites un `git log` et vous verrez qu'un commit a été ajouté avant le votre.
- "Push" votre commit et ça marchera : `git push`.

---

### Exercice 3 : Conflits de merge

Passer au prochain exercice en faisant un commit avec "exercice 3" dans le titre :

```sh
$ git commit --allow-empty -m "exercice 3"
$ git push
```

---

### Exercice 3 : Conflits de merge

*Contexte* : quelqu'un a push un commit qui a modifié quelque chose qu'un commit à vous a aussi modifié.

---

### Exercice 3 : Conflits de merge

- Changez la première ligne de `README.md` vers ce que vous voulez.
- Committez ce changement.
- "Pull" ces changements du remote :

```sh
$ git pull
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

---

### Exercice 3 : Conflits de merge

- Ouvrez `README.md` et gardez ce que vous voulez :

```md
<<<<<<< HEAD
# Mon nouveau titre
=======
# Le titre conflictuel
>>>>>>> main
```

---

### Exercice 3 : Conflits de merge

- Committez la resolution de merge :

```sh
git add README.md
git commit -m "merge: Merge from main"
git push
```

---

## Travail de groupe

Pour cette partie de la presentation, mettez vous en groupes de 2.
Choisissez le repo que vous préférez - vous allez à présent tous les deux travailler dessus.
Assurez-vous d'avoir tous les deux clone ce repo.

---

### Exercice 4 : Générer un merge conflict

TODO faire en sorte qu'il y ait un merge conflict et que l'un d'entre vous le fix
Ensuite, que l'autre fasse pareil.

---

### Branches

TODO

---

### Exercice 5 : Branches

TODO

---

## Contribution à un repo Open Source

TODO part 1

- Create github account
- SSH keys setup
- Create git repo
- add your repo as a remote (quick quick recap on remotes, or should the second on remotes be here anyway?)
- `git push origin github`

TODO part 2

- Fork https://github.com/user/first-contributions
- clone
- cd
- make changes
- add/commit/push
- create PR on github

---

## Git etiquette

TODO be very brief here

---

## Tips and tricks

- `git add -p`
- tags
- idea behind refs
- git hooks (pre-commit.com)
- git commit --amend
- git push remote branch
