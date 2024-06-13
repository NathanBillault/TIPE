
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

##Réduction des paramètres

def parametre_to_c (Ul,Ac,p,c,Vc,v,n0,Tce,Tcold,Ic,Vs,As,Ks,vl,Tse):
    c1 = Ul*Ac/p*c*Vc + v/Vc
    c2 = Ac*n0*Ic/p*c*Vc + Ul*Ac*Tce/p*c*Vc + v*Tcold/Vc
    c3 = v/Vc
    c4 = Ac*n0*Ic/p*c*Vc + Ul*Ac*Tce/p*c*Vc
    c5 = v/Vs
    c6 = v/Vs + vl/Vs + As*Ks/p*c*Vs
    c7 = vl*Tcold/Vs + As*Ks*Tse/p*c*Vs
    c = [0,c1,c2,c3,c4,c5,c6,c7]
    return c


## Fonctions pour solutions analytiques

def c_to_lambda_sol(c):
    lambda1 = (-c[1] - c[6] - np.sqrt((c[1]-c[6])**2 + 4*c[3]*c[5]))/2
    lambda2 = (-c[1] - c[6] + np.sqrt((c[1]-c[6])**2 + 4*c[3]*c[5]))/2
    s11 = -(c[1] - c[6] - np.sqrt((c[1]-c[6])**2 + 4*c[3]*c[5]))/(2*c[5])
    s21 = -(c[1] - c[6] + np.sqrt((c[1]-c[6])**2 + 4*c[3]*c[5]))/(2*c[5])
    return lambda1,lambda2,s11,s21

def lambda_sol_to_TcTs(lambda1,lambda2,s11,s21,Tc0,Ts0,c):
    def Tc(t):
        return 1/(s11 - s21) * (s11*np.exp(lambda1*t)-s21*np.exp(lambda2*t))*Tc0 - s11*s21*(np.exp(lambda1*t)-np.exp(lambda2*t))*Ts0 + s11(c[4]-c[7]*s21)/lambda1*np.exp(lambda1*t) + (c[6]*c[4]+c[3]*c[7])/(c[1]*c[6]-c[3]*c[5]) -s21(c[4]-c[7]*s11)/lambda2*np.exp(lambda2 * t)
    def Ts(t):
         return 1/(s11 - s21) * (s11*np.exp(lambda1*t)-s21*np.exp(lambda2*t))*Ts0 + (np.exp(lambda1*t)-np.exp(lambda2*t))*Tc0 + (c[4]-c[7]*s21)/lambda1*np.exp(lambda1*t) + (c[5]*c[4]+c[1]*c[7])/(c[1]*c[6]-c[3]*c[5])-(c[4]-c[7]*s11)/lambda2*np.exp(lambda2 * t)
    return Tc,Ts

## Fonction pour solution approchée avec odeint

def pend(y,t,c):
    Tc,Ts = y
    dydt = [-c[1]*Tc + c[3]*Ts + c4, c[5]*Tc - c[6]*Ts + c7]
    return dydt

##Graphes
#paramètres : valeurs numériques de l'exemple


Ul = 4.4 #coefficient de perte de chaleur globale du collecteur (W/m2K)
Ac = 2.2 #Aire du collecteur (m2)
p= 1000 #kg/m3
c= 4200 #J/(kgK)
Vc =  0.01 #volume du collecteur
v = 2/60000 #debit volumétrique de la pompe (m3/s)
n0 = 0.63 #efficacité optique du collecteur
Tce  = 293
Tcold = 288 # 15 °C

Vs = 0.3
As = 2.3 #m2
Ks = 7.2  #coefficient de deperdition thermique du stockage (W/m2K)
vl = 0.#débit volumétrique de la charge de consommation m3/s
# on considere un syteme sans douche ici

Tse = 293  #temperature ambiante


#inclinaison 40°
#inclinaison sud
#Pour une journée à Paris entre 6h et 21h 
#IC en W/m2 
IcParisjournee = np.array([1,77,220,2318,321,180,359,520,638,699,697,634,518,371,208,59])
arrayh = np.array([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])


#irradiation, 12 valeurs pour les 12 mois de l'annee
arraymois = np.array(["janvier", "février", "mars ","avril ", "mai ", "juin", "juillet ", "aout ", "septembre", "octobre", "novembre", "décembre"])
IcParis  =np.array([1.3,2.,3.49, 4.05,4.72,5.04,4.9,4.44,3.91,2.66,1.44,1.14,3.268]) *(10**3)/12
IcBordeaux = np.array[( 	1.93 	,2.71, 	3.62 ,	4.99 	,5.45 ,	5.85 	,6.11 ,	5.23 	,4.78 ,	3.5 	,2.25, 	1.75, 	4.02)]
IcBrest =np.array([1.56 	,2. ,	3.65 ,	4.5 	,5.09, 	5.08 ,	5.04 	,4.42 ,	3.36 ,	3.07, 	1.87 	,1.29 ,	3.42])
IcStrasbourg =np.array([1.1 ,	2.06 ,	3.03, 	3.93, 	4.54, 	4.78, 	5.07 ,	4.65 ,	3.77, 	2.35, 	1.51 ,	1 ,	3.15])
IcCorse = np.array([2.98,	3.38 	,4.46 ,	5.3 	,5.48 ,	6.1, 	6.44 ,	5.87 	,5.41, 	4.99 ,	3.48 ,	2.92 	,4.74])*(10**3)




#t = np.linspace(0,3600,60) #Créer un np.array de 60 valeurs espacées d'un meme écart entre 0 et 3600 (s)
c = parametre_to_c(Ul,Ac,p,c,Vc,v,n0,Tce,Tcold,Ic,Vs,As,Ks,vl,Ts)
#Tc0,Ts0 = "A compléter"
#y0 = [Tc0,Ts0]
#sol = odeint(pend,y0,t,args = (c))
#Tc_An,Ts_An = lambda_sol_to_TcTs(c_to_lambda_sol(c),Tc0,Ts0,t,c)

#plt.plot(t,sol[:,1],'b',label='Solution approchée') #sol[:,1] récupère Ts
#plt.plot(t,Ts_An,'b',label='Solution analytique')
#plt.xlabel("Température du stockage (en °C)")
#plt.ylabel("Temps en secondes")
#plt.show()
