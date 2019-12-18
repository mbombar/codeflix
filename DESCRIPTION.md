# codeflix

## Idée générale

Créer un site qui aiderait les gens à s'améliorer en compétition d'algorithmique.


## Contexte

codeforces.com est un site russe (mais avec une interface disponible en anglais) qui propose régulièrement des compétitions d'algorithmique pour ses utilisateurs.
L'idée, c'est que chaque problème est aussi accessible a posteriori, ce qui est très pratique pour s'entraîner et progresser (en sélectionnant des vieux problèmes pertinents).
La question qui se pose alors est : comment choisir de façon pertinente les problèmes sur lesquels s'entraîner ?


## UX

Proposer aux utilisateurs un site web qu'iels pourront consulter pour se faire conseiller quelques problèmes pertinents à résoudre.

Plus exactement, un·e user peut accéder au site :

* soit de façon anonyme, en rentrant simplement un username codeforces, et on conseillerait alors les n problèmes qui nous paraissent les plus pertinents.

* soit en s'identifiant sur notre plateforme, sur laquelle iel aura rentré ses identifiants codeforces, on lui conseille alors des problèmes, et l'utilisateur peut en cocher certains pour s'en débarasser s'ils ne l'intéressent pas (évidemment, on n'oublie pas quels problèmes n'intéressent pas notre user, et iel pourrait même les gérer).


## Détails pratiques

Comment on conseillerait de tels problèmes :

* il y a déjà une API codeforces qui permet d'accéder facilement à la liste des problèmes, des users, de dire que tel user a résolu tels problèmes etc.

* on pourrait faire du ML sur le graphe "tel user (n')a (pas) résolu tel problème" pour être capable de calculer pour une paire (user, problem) la probabilité que user (ne) sache (pas) résoudre le problème problem.
    
* on conseillerait pour un user donné les problèmes avec un niveau inférieur ou proche à celui dudit user mais avec les probabilités de résolution les plus basses.

Comme il y a environ 57000 problèmes résolus et environ autant d'utilisateurs et que le problème sous-jacent (collaborative filtering) est déjà très étudié, on peut espérer que notre algorithme donne des résultats corrects.
On exporterait aussi notre API, ce qui pourrait être utile à d'autres.

Enfin, on ferait tout ceci en Django.
