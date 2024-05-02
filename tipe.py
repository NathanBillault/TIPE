import matplotlib.pyplot as plt
import numpy as np

def temps_de_remboursement (cout_initial,type_de_panneau,surface):
    rendement_selon_type = {"PERC":0.25,"Monocrystallin":0.2,"Polycristallin":0.16}
    rendement = rendement_selon_type[type_de_panneau]
    prix_elec_par_kw = 0.2516
    irradiation_annuelle_moyenne_en_kwHm2 = 1300
    return int(cout_initial / ((irradiation_annuelle_moyenne_en_kwHm2)/365 * surface * rendement * prix_elec_par_kw))

cout = [20000,14500,9500]
type_de_panneau = ["PERC","Monocrystallin","Polycristallin"]
surface = [45,30,15]
tr = []

for i in range(3):
    tr.append(temps_de_remboursement(cout[i],type_de_panneau[i],surface[i]))
    print ("Vous serez rentables en",temps_de_remboursement(cout[i],type_de_panneau[i],surface[i]),"jours")

#P = puissance nominale en kWc = 1000w/m2 * rendement * 1.8 m2
#P/1.8 * x = 1000 <=> x = 1000 * 1.8/(1000 * 1.8 * r) = 1/r

print(1/0.18)

plt.bar(type_de_panneau,tr)
plt.ylabel("Temps de remboursement (en jours)")
plt.xlabel("Type de panneau photovoltaïque")
plt.show()
