
"""

Tâche de détermination numérique pour évaluer l'impact
de la configuration sur le subitizing
Victor ANTOINE - victor.antoine@ens.fr 

"""

import os.path
from numpy import random
from expyriment import design, stimuli, control, io, misc

#instructions
instructions1 = """ Vous allez observer un certain nombre de points pendant un\
 court instant. \n \n \n Vous devrez ensuite indiquer le nombre de points que\
 vous avez perçus. \n \n \n Le temps n'est pas comptabilisé pendant cette\
 tâche.\n \n \n Appuyer sur ESPACE pour continuer"""
 
instructions2 = """ Pour indiquer le nombre de points que vous avez vu, \
utilisez le clavier, \n puis appuyez sur ENTRER pour passer à l'image \
suivante. \n \n \n Appuyer sur ESPACE pour commencer la tâche"""

#design
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

#initialize
control.initialize(exp)

instructions_1 = stimuli.TextScreen("Instructions", text=instructions1)
instructions_2 = stimuli.TextScreen("Instructions", text=instructions2)
question = io.TextInput(message = "Combien de points avez-vous vu ?", \
                        message_colour = (211, 211, 211), message_italic = True)
fs = stimuli.FixCross(size=(35, 35), line_width= 5, colour = (255, 20, 147))
kb = exp.keyboard

#start
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

#end
exp.data.rename("experience_subitizing_" + str(exp.subject) + ".xpd")
control.end(goodbye_text= "Merci pour votre participation !", goodbye_delay = 3000)
