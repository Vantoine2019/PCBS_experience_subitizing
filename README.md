Introduction
------------

L’objectif de ce projet est de créer une tâche de détermination
numérique pendant laquelle le participant devra déterminer la numérosité
d’une image (à savoir le nombre de points qu’il perçoit). Les
différentes images présentent un nombre de points allant de 1 à 10
points - ceux-ci sont soit disposés aléatoirement, soit disposés selon
une forme dite “configurationnelle”. Une disposition configurationnelle
est une disposition qui facilite la quantification par le participant
(alignements, formes géométriques classiques, etc). Dans cette
expérience, on utilisera des formes de dés pour les dispositions
configurationnelles.

On appelle classiquement “subitizing” la capacité chez un individu de
déterminer de manière précise la numérosité d’une quantité faible, même
avec un temps de présentation très court. Cette capacité permet en
général chez l’adulte d’évaluer des quantités allant de 1 à 4 (voire 5)
de manière précise sans avoir besoin de compter les différents éléments.
Néanmoins, au-delà de 5, l’individu est normalement obligé de dénombrer
les éléments (ie les compter) pour rester précis.

Néanmoins, lorsque les différents éléments sont placés de manière
organisée (sous forme de configurations), la capacité de quantification
rapide et précise (“subitizing”) peut considérablement augmenter.
L’objectif de cette expérience est de montrer l’impact de la
configuration sur le subitizing. On distinguera alors 2 variables
indépendantes : le nombre de points affichés (de 1 à 5 points vs de 6 à
10 points) et leur disposition (aléatoire vs configurationnelle). Chaque
participant sera testé sur 60 trials (15 x 4 conditions). En théorie, on
prédit que lorsque la numérosité est inférieure à 5, les performances
devraient être bonnes (car peu importe la disposition, le subitizing
sera efficace). Néanmoins, ces performances devraient chuter lorsque la
numérosité augmente (images de 6 à 10 points), mais uniquement dans la
disposition aléatoire (car la disposition configurationnelle devrait
faciliter la quantification par le participant). On attend alors une
interaction.

### Contenu du répertoire

Ce répertoire Github comprend normalement :  
\* un dossier pictures avec deux-sous dossiers : les images présentées
pendant l’expérience y seront stockées. Il contient déjà des images
générées par un script (présenté plus tard) pour donner un exemple.  
\* un script python “create\_pictures.py” ; qui servira à créer les
images pour l’expérience  
\* un script python “experience\_subitizing.py” ; qui permet d’effectuer
la passation  
\* un script python “result.py” ; qui permet d’afficher un graphique des
résultats pour un sujet donné  
\* *deux dossiers contenant les données de l’expérience seront créés
automatiquement pendant la passation : /data/ et /events/*

### Lancement des scripts

Afin d’utiliser l’expérience correctement :  
1. Lancer d’abord le script “create\_pictures.py” afin de créer les
images  
2. Puis lancer le script “experience\_subitizing.py” pour faire
l’expérience  
3. Enfin utiliser le script “result.py” pour visualiser les résultats
(Attention, ce script nécessite de donner le numéro du participant dans
le terminal - Usage : result.py subject\_number - par exemple, si vous
souhaitez afficher les résultats du participant n°4, utilisez dans votre
terminal “python result.py 4”)

Création des images
-------------------

**create\_pictures.py**

Le premier script permet de créer les images utilisées pendant
l’expérience. Il comprend globalement 2 parties : une pour créer des
images avec une disposition aléatoire et une pour des images en position
configurationnelle.

    import pygame
    from random import sample
    from numpy import random, sort
    from os import path
    from itertools import product

    W, H = 960, 540

    pygame.init()
    screen = pygame.display.set_mode((W, H), pygame.DOUBLEBUF)
    screen.fill((0, 0, 0))

On importe d’abord les différents fonctions et modules qu’on va
utiliser. On définit ensuite une zone (hauteur et longueur) qui servira
pour créer les images avec pygame.

### Création des images aléatoires

    origin_x, origin_y = random.randint(50, 910), random.randint(50, 490)
    list_coord_random_x = list_coords_random_y = []

    def create_liste_coord_random(axe, origin):
        coord1 = coord2 = origin
        liste = []
        liste.append(origin)
        while coord1 <= axe - 160:
            coord1 += 80
            liste.append(coord1)    
        while coord2 >= 110:
            coord2 -= 80
            liste.append(coord2)    
        liste = list(sort(liste))
        return liste

    list_coord_random_x = create_liste_coord_random(W, origin_x)
    list_coord_random_y = create_liste_coord_random(H, origin_y)
    system_coord_random = list(product(list_coord_random_x, list_coord_random_y))

Afin de créer les images aléatoires, on détermine d’abord 2 variables
aléatoires qui serviront de base pour créer le système de coordonnées.
On définit ensuite une fonction qui permettra d’obtenir une liste de
points espacés de manière égale - fonction qu’on applique ensuite à nos
2 variables aléatoires pour avoir 2 listes distinctes (qui seront nos
coordonnées en x et en y). Afin de créer les couples de coordonnées, on
utilise enfin une fonction `product` : nous venons de construire un
système de coordonnées de points également espacés sur notre écran.

    for version in list(range(1, 11)):
        for points_number in list(range(1, 11)):
            screen.fill((0, 0, 0))
            for (x, y) in sample(system_coord_random, points_number):
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 30, 0)    
            pygame.image.save(screen, path.join("pictures", "random", \
                              str(points_number) + "_" + str(version) + ".png"))

Une fois ce système de coordonnées obtenues, il ne reste plus qu’à créer
les images. Pour se faire, on va créer un nombre de cercles égal au
nombre de points voulus sur l’image ; mais on les sélectionne de manière
aléatoire parmi notre système de coordonnées (fonction `sample`
appliquée à la variable `system_coord_random`). On va effectuer cette
opération 10 fois pour chaque nombre ; ce qui va nous créer un total de
100 images. *Ces images seront sélectionnées aléatoirement pendant
l’expérience afin que le sujet ne perçoive pas à chaque fois la même
disposition pour la disposition non configurationnelle.*

### Création des images en position configurationnelle

    def create_slot_coord_config(top, left):
        liste_coord = []
        for position in [(1, 1), (3, 1), (2, 2), (1, 3), (3, 3)]:
            liste_coord.append((top + position[0] * ((W - 270)/8),\
                               left + position[1] * ((H - 270)/4)))
        return liste_coord

    coord_left_side = create_slot_coord_config(130, 130)
    coord_mid_side = create_slot_coord_config(303, 130)
    coord_right_side = create_slot_coord_config(475, 130)

Pour créer les images avec les points disposés en forme de dés, on va
dans un premier temps créer les coordonnées qu’on va utiliser
postérieurement. L’idée est de définir une fonction qui à partir des
coordonnées qu’on donne (*celles du premier point*) va créer une liste
avec les coordonnées d’une face de dé avec 5 points (*imaginez la face 5
d’un dé, si vous donnez la position du point en haut à gauche, la
fonction vous donnera les positions des 4 autres points en plus*).

On utilisera alors cette fonction sur 3 coordoonées initiales
différentes afin d’obtenir 3 listes. Ces 3 listes contiennent chacune
les positions de la face 5 d’un dé, mais à des endroits différents de
l’écran : une qui s’affichera au milieu de l’écran (*pour les nombres de
1 à 5*), une qui s’affichera à gauche, et une à droite (*on utilisera
ces deux listes pour les nombres de 6 à 10*).

    system_coord_config = []
    position = [[2], [1, 3], [1, 2, 3], [0, 1, 3, 4], [0, 1, 2, 3, 4]]

    for number in range(1, 11):
        list_coord = []
        
        if number <= 5:
            positions = position[number-1]
            for circle in positions:
                list_coord.append(coord_mid_side[circle])
            system_coord_config.append(list_coord)
            
        else:
            for circle in position[4]:
                list_coord.append(coord_left_side[circle])
            positions = position[number-6]
            for circle in positions:
                list_coord.append(coord_right_side[circle])
            system_coord_config.append(list_coord)

Ensuite, il est nécessaire de créer les coordonnées pour chaque nombre.
On initie alors une liste vide `system_coord_config`. Le principe va
être d’ajouter à cette liste globale la liste de coordonnées pour un
nombre donné. Pour se faire, on va aller chercher pour chaque nombre les
points qu’on a défini précédemment : pour les nombres de 1 à 5 on va
utiliser les points qui s’affichent au centre l’écran ; pour les nombres
de 6 à 10, on va utiliser les points à gauche et droite.

    number_index = 1
    for number in system_coord_config:
        screen.fill((0, 0, 0))
        for (x, y) in number:
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 30, 0)
        pygame.image.save(screen, path.join("pictures", "config", \
                                               str(number_index) + ".png"))
        number_index += 1

Il ne reste alors plus qu’à créer les images. Pour chaque nombre, on va
afficher un cercle pour chaque coordonnée définie dans
`system_coord_config`. L’image sera enregistrée dans un répertoire
différent des images aléatoires pour pouvoir y accéder plus facilement.

Description de l’expérience
---------------------------

**experience\_subitizing.py**

Nos images qu’on souhaite afficher sont maintenant créées. Le principe
de l’expérience sera le suivant : on va afficher une image puis demander
au participant combien de points celui-ci a perçu. Cette opération sera
répétée avec des groupes de 4 blocks ; cela 3 fois.

<table>
<thead>
<tr class="header">
<th style="text-align: center;">Block</th>
<th style="text-align: center;">Disposition</th>
<th style="text-align: center;">Nombre</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: center;">1</td>
<td style="text-align: center;">Aléatoire</td>
<td style="text-align: center;">1 à 5</td>
</tr>
<tr class="even">
<td style="text-align: center;">2</td>
<td style="text-align: center;">Aléatoire</td>
<td style="text-align: center;">6 à 10</td>
</tr>
<tr class="odd">
<td style="text-align: center;">3</td>
<td style="text-align: center;">Configuration</td>
<td style="text-align: center;">1 à 5</td>
</tr>
<tr class="even">
<td style="text-align: center;">4</td>
<td style="text-align: center;">Configuration</td>
<td style="text-align: center;">6 à 10</td>
</tr>
</tbody>
</table>

Dans chaque block, l’ordre des trials sera aléatoire. L’ordre des blocks
sera aussi aléatoire. On va répéter cette opération 3 fois : soit 3
groupes de 4 blocs randomisés.

    import os.path
    from numpy import random
    from expyriment import design, stimuli, control, io, misc

On importe tout d’abord les différents modules et fonctions nécessaires.
Cette expérience utilisera notamment expyriment.

### Instructions & Design

    #instructions
    instructions1 = """ Vous allez observer un certain nombre de points pendant un\
     court instant. \n \n \n Vous devrez ensuite indiquer le nombre de points que\
     vous avez perçus. \n \n \n Le temps n'est pas comptabilisé pendant cette\
     tâche.\n \n \n Appuyer sur ESPACE pour continuer"""
     
    instructions2 = """ Pour indiquer le nombre de points que vous avez vu, \
    utilisez le clavier, \n puis appuyez sur ENTRER pour passer à l'image \
    suivante. \n \n \n Appuyer sur ESPACE pour commencer la tâche"""

On détermine tout d’abord les instructions qu’on souhaite afficher et
donner au participant.

    exp = design.Experiment(name="Subitizing  Experiment")

    def create_block(block_name, disposition, dot_class):
        
        block_name = design.Block()
        block_name.set_factor("disposition", disposition)
        if block_name.get_factor("disposition") == "random":
            path_disposition = "random"
            path_random = "_" + str(random.randint(1, 11))
        else:
            path_disposition = "config"
            path_random = ""
        
        block_name.set_factor("dot_class", dot_class)
        if block_name.get_factor("dot_class") == "1-5":
            dot_list = list(range(1, 6))
        else:
            dot_list = list(range(6, 11))
        
        for dot_number in dot_list:
            t = design.Trial()
            t.set_factor("dot_number", dot_number)
            s = stimuli.Picture(os.path.join("pictures", \
            path_disposition, str(dot_number) + path_random + ".png"))
            t.add_stimulus(s)
            block_name.add_trial(t)
        block_name.shuffle_trials()
        exp.add_block(block_name)

    for _ in range(3):
        for carac_block in [["b1","random", "1-5"], ["b2","random", "6-10"], \
        ["b3","configurational", "1-5"], ["b4","configurational", "6-10"]]:
            create_block(carac_block[0], carac_block[1], carac_block[2])

    exp.data_variable_names = ["disposition", "dot_class", "dot_number", "response"]
    design.randomize.shuffle_list(exp.blocks, n_segments=3)

La première étape consiste à créer le design souhaité dans expyriment.
On va alors définir une fonction pour créer lesdits blocks. Cette
fonction va simplement assigner 2 informations au block : la disposition
des points (aléatoire ou en forme de dé) et le nombre (de 1 à 5 ou de 6
à 10). En fonction de ces informations, on va définir des variables qui
vont permettre d’aller chercher correctement les images dans les
dossiers correspondants. Ensuite, cette fonction va ajouter au block un
trial pour chaque nombre et on créé un stimulus par trial (*chaque block
contient donc 5 stimuli*). Enfin, cette fonction randomise l’ordre des
différents trials.

On va donc appliquer cette fonction à nos 4 types de blocks ; et cela 3
fois d’affilée - *on crée donc 12 blocks*. Enfin, on randomise l’ordre
des blocks dans des groupes de 4 pour terminer la mise en place de notre
design.

### Initialisation

    control.initialize(exp)

    instructions_1 = stimuli.TextScreen("Instructions", text=instructions1)
    instructions_2 = stimuli.TextScreen("Instructions", text=instructions2)
    question = io.TextInput(message = "Combien de points avez-vous vu ?", \
                            message_colour = (211, 211, 211), message_italic = True)
    fs = stimuli.FixCross(size=(35, 35), line_width= 5, colour = (255, 20, 147))
    kb = exp.keyboard

On initialise l’expérience et on définit certaines variables qu’on
utilisera après ; notamment nos différents stimuli (dont nos
instructions et notre question).

### Start & End

    control.start(exp)

    instructions_1.present()
    kb.wait(misc.constants.K_SPACE)
    instructions_2.present()
    kb.wait(misc.constants.K_SPACE)
        
    for block in exp.blocks:
        for trial in block.trials:
            fs.present()
            exp.clock.wait(1500)
            trial.stimuli[0].present()
            exp.clock.wait(400)
            fs.present()
            exp.clock.wait(250)
            response = question.get()
            response = response.strip()     
            exp.data.add([block.get_factor("disposition"), block.get_factor("dot_class"),\
                          trial.get_factor("dot_number"), response])

Reste alors à déterminer la passation de chaque stimulus. On présente
d’abord nos instructions puis on va venir afficher nos différents
trials. Pour chaque trial, on affichera une croix puis notre image
pendant un instant court (400 ms) avant de demander au participant de
nous donner une réponse. Chaque réponse sera ajoutée au fichier
contenant les données de la passation.

    exp.data.rename("experience_subitizing_" + str(exp.subject) + ".xpd")
    control.end(goodbye_text= "Merci pour votre participation !", goodbye_delay = 3000)

Enfin, on termine l’expérience ; en renommant auparavant notre fichier
de données (*cela va permettre d’y accéder plus facilement avec le
script suivant*).

Affichage des résultats
-----------------------

**result.py**

    from pandas import read_csv
    import matplotlib.pyplot as plt
    from numpy import logical_and, sum
    from sys import argv, exit
    import os.path

    if len(argv) != 2:
        print("Usage : result_exp_subitizing subject_number")
        print("subject_number est le numero du sujet attribue pour la tache")
        exit()
        
    subject_number = argv[1]

Comme précedemment, on commence par importer nos fonctions et modules ;
mais on va en plus imposer à l’utilisateur de nous donner le numéro du
participant pendant l’expérience. Le principe va être d’utiliser cette
information pour ensuite ouvrir notre ficher stocké dans le dossier
/data/. Si l’utilisateur ne nous donne pas cette information, le script
s’arrêtera en donnant des indications sur le lancement du script.

### Ouverture et correction du dataset

    df = read_csv(os.path.join("data", "experience_subitizing_" + \
                                  str(subject_number) + ".xpd"), skiprows = 10 + 6*12)
    df["correction"] = (df.dot_number == df.response)

    results = []
    def get_result(disposition, dot_class):
        result = sum(logical_and(logical_and(df.disposition == disposition,\
                 df.dot_class == dot_class), df.correction == 1))
        return result

    for group in [["random", "1-5"], ["random", "6-10"], \
                  ["configurational", "1-5"], ["configurational", "6-10"]]:
        result_group = get_result(group[0], group[1])
        print("Disposition : " + str(group[0]) + " ,Nombre entre : " + str(group[1])\
        + " - Resultat : " + str(result_group) + "/" + str(15))
        results.append(result_group)

On ouvre tout d’abord notre fichier de résultats en prenant soin de ne
pas prendre en compte certaines lignes (*elles indiquent la description
des blocks, qui ne nous intéressent plus à présent*). On va ensuite
ajouter une colonne supplémentaire à notre dataset en corrigeant les
réponses du participant.

Ensuite, on définit une fonction qui va permettre de compter le nombre
de bonnes réponses pour une disposition et une numérosité donnée. En
l’appliquant alors nos 4 différents cas possibles (2 dispositions \* 2
types de numérosité), on obtient donc 4 résultats ; que l’on affiche.

### Création du graphique

Afin d’avoir une idée visuelle de la possible intéraction (*pour rappel,
on attend des performances plus faibles pour une disposition aléatoire
avec de grandes numérosités (6-10)*), le script va permettre de créer un
graphique des résultats.

    x = ["1-5", "6-10"]
    y = [3*number for number in range(6)]
    xn = range(len(x))
    yn = range(len(y))
    y_random = [results[0], results[1]]
    y_config = [results[2], results[3]]

    randomplot = plt.plot(xn, y_random, linewidth = 1, color = "b", label = "Aléatoire")
    plt.plot(xn, y_random, color = "b", marker = "v", markersize = 10)
    configplot = plt.plot(xn, y_config, linewidth = 1, color = "m", label = "Configurationnelle")
    plt.plot(xn, y_config, color = "m", marker = "^", markersize = 10)
    plt.xlabel("Disposition")
    plt.xticks(xn, x)
    plt.xlim(-0.5 , 1.5)
    plt.ylabel("Nombre de bonnes réponses")
    plt.ylim(0, 12*5/4 + 1)
    plt.yticks(y, y)
    plt.gca().grid(which='major', axis='both', linestyle='--')
    plt.legend(loc=3, fontsize="small")
    plt.show()

Basiquement, on va fixer nos numérosités (petites vs grandes) en
abscisse ; et nos résultats en ordonnée. On affiche alors 2 lignes
différentes ; une pour chaque type de disposition. Afin d’avoir un
rappel direct de notre prédiction, des marqueurs différents sont
utilisés :  
- les données pour la disposition **configurationnelle** (dés) sont
présentées avec un triangle avec le **sommet en haut** car on attend des
**performances qui se maintiennent**  
- les données pour la disposition **aléatoire** sont présentées avec un
triangle avec le **sommet en bas** car on attend des **performances qui
chutent**

Retour sur expérience
---------------------

N’ayant absolument aucune idée de l’aspect informatique de la
sémantique du mot “python” auparavant, cette expérience fut intéressante
dans la mesure où elle offre une porte d’entrée à la programmation
nécessaire en sciences cognitives. La combinaison entre ce cours et
celui utilisant DataCamp permet d’aborder certaines bases essentielles.
Néanmoins, la structure actuelle du cours reste selon moi confuse -
certaines notions sont directement abordées mais sont trop complexes
pour des personnes qui n’ont jamais fait de programmation ; mais
paraissent évidentes pour d’autres personnes (l’écart s’étant
probablement creusé avec la suppression du mois de rentrée et le nombre
moins important d’heures en PCBS). Un système de groupes de niveaux
pourrait paraître pertinent car en plus du meilleur suivi pendant les
cours, il pourrait aussi permettre de donner des exercices plus
adapatées aux besoins de chacun (même les premiers exercices sont
difficiles pour des débutants).
