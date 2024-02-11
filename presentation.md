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

---

## Table des matières

<!-- TODO -->
<!-- pas moyen de gen ça automatiquement avec MARP? -->

---

### Git, c'est quoi ?

- Un système de gestion de versions distribué
- VCS (Version Control System), en Anglais

---

## Mise en place de l'environnement

---

Ouvrir votre émulateur de terminal, et ensuite :

### Linux

```console
$ sudo apt update && sudo apt install git
```

### Windows

- `wsl --install`
- Ouvrir une session Linux.
- Cf. Linux.

### Mac

```console
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

```console
$ echo "Hello world"  # <-- commande + argument
Hello world           # <-- sortie
```

![bg right width:100%](img/commande.png)

---

## Le Chemin (aka Path)

Soyez attentif ici, c'est là où les gens ont généralement le plus de mal !

---

## Le Chemin (aka Path)

Une liste de dossiers empruntés pour arriver à un dossier/fichier, séparés par des `/`. E.g. :

- Un fichier qui s'appelle "tux" : `tux`
- Ce dossier "super" : `super`
- Un fichier qui s'appelle "tux2" dans ce dossier "super" : `super/tux2`

Ce sont des chemins *relatifs* !

---

## Le Chemin (aka Path) : `pwd`

**Q**: Relatifs à quoi ? **R**: Relatifs à nous.
**Q**: Comment savoir où nous sommes ? **R**:

```console
$ pwd # "print working directory" ou "écrire le dossier de travail"
/home/beastie
```

Le "dossier de travail" ou "working directory" est le dossier dans lequel nous sommes actuellement.
Ceci est un chemin *absolu* !

---

## Le Chemin (aka Path) : `pwd`

On peut trouver un chemin absolu d'un chemin relatif en ajoutant notre dossier de travail avant :

- Le fichier `tux` devient `/home/beastie/tux`.
- Le dossier `super` devient `/home/beastie/super`.
- Le fichier `super/tux2` devient `/home/beastie/super/tux2`.

---

## Le Chemin (aka Path) : `ls`

On peut afficher tous les fichiers/dossiers dans notre dossier de travail :

```console
$ ls
tux	super/
```

Ou dans un autre dossier :

```console
$ ls super
tux2
```

---

## Le Chemin (aka Path) : `cd`

On peut changer notre dossier de travail :

```console
$ cd super
```

Et puis encore :

```console
$ ls
tux2
```

---

## Le Chemin (aka Path) : `cd`

On peut retourner un dossier en arrière :

```console
$ pwd
/home/beastie/super
$ cd ..
$ pwd
/home/beastie
```

---

## Le Chemin (aka Path)

Pour résumer :

- `pwd` : Afficher le dossier de travail.
- `ls` : Afficher le contenu d'un dossier.
- `cd` : Changer le dossier de travail.

---

### Configurer `git`

```sh
git config --global user.name Theo
git config --global user.email theo@louvainlinux.org
```
