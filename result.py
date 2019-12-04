
"""

Affichage des résultats pour un sujet donné
(Tâche de détermination numérique pour évaluer l'impact
de la configuration sur le subitizing)
Victor ANTOINE - victor.antoine@ens.fr 

"""

from pandas import read_csv
import matplotlib.pyplot as plt
from numpy import logical_and, sum
from sys import argv, exit
import os.path

if len(argv) != 2:
    print("Usage : result_exp_subitizing subject_number")
    print("subject_number est le numero du sujet attribue pour la tache")
    exit()

#ouverture, lecture et correction du dataset
subject_number = argv[1]
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

#création du graphique
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
